# 04 - 基础规则编写

## 概述

在掌握了Cursor Rules的基本概念、设置和组件后，本章将指导您开始编写自己的规则。我们将从简单的规则开始，逐步引导您理解常见的规则模式，并介绍规则的测试和调试方法。

## 学习目标

- 编写并理解基本的Cursor规则
- 掌握常见的规则模式和使用场景
- 学习测试和调试规则的方法
- 应用规则优化日常工作流程

## 编写第一个规则

### 基本规则结构回顾

在开始之前，让我们回顾一下规则文件的基本结构：

```
---
description: 规则简短描述
globs: **/*.js,**/*.ts  # 适用的文件模式
---
# 规则标题

<rule>
name: rule_name
description: 规则详细描述

filters:
  - type: filter_type
    pattern: "匹配模式"

actions:
  - type: action_type
    content: "动作内容"

metadata:
  priority: medium
  version: 1.0.0
  tags: ["tag1", "tag2"]
</rule>
```

### 简单规则示例：代码格式提示

让我们从一个简单的规则开始，该规则会在JavaScript/TypeScript文件中提示使用更现代的语法：

```
# 创建一个简单的JavaScript语法提示规则
# 保存到 .cursor\rules\code_standards\js_syntax.mdc

---
description: JavaScript语法现代化提示
globs: **/*.js,**/*.ts
---
# JavaScript语法现代化提示

<rule>
name: modern_js_syntax
description: 提示使用更现代的JavaScript语法和特性

filters:
  - type: content
    pattern: "var\\s+\\w+"

actions:
  - type: suggest
    message: "考虑使用`const`或`let`替代`var`，以使用更现代和安全的变量声明方式。"

metadata:
  priority: medium
  version: 1.0.0
  tags: ["javascript", "syntax", "best-practices"]
</rule>
```

在Windows环境中创建此规则：

1. 使用Windows资源管理器导航到你的项目目录
2. 创建目录结构 `.cursor\rules\code_standards`（如果不存在）
3. 在该目录中创建文件 `js_syntax.mdc`
4. 将上面的规则内容复制到文件中并保存

> **注意**：在Windows环境中，你也可以使用PowerShell命令创建目录和文件：
> ```powershell
> New-Item -Path ".cursor\rules\code_standards" -ItemType Directory -Force
> New-Item -Path ".cursor\rules\code_standards\js_syntax.mdc" -ItemType File -Force
> ```

### 简单规则解析

让我们来分析这个规则的组成部分：

1. **Header**：包含规则的基本描述和适用的文件模式（`**/*.js,**/*.ts`表示适用于所有JS和TS文件）
2. **name & description**：规则的唯一标识符和详细描述
3. **filters**：设置了一个内容过滤器，会匹配包含`var`声明的代码
4. **actions**：当过滤器匹配成功时，会显示一条建议消息
5. **metadata**：包含规则的优先级、版本和标签信息

## 常见规则模式

下面介绍几种常见的规则模式，您可以将它们用作自己规则的模板。

### 1. 代码检查规则

这种规则用于检查代码中的问题或不符合最佳实践的地方：

```
# 代码检查规则示例
# 保存到 .cursor\rules\code_quality\error_handling.mdc

---
description: 检查代码中的错误处理
globs: **/*.js,**/*.ts
---
# 错误处理检查

<rule>
name: error_handling_check
description: 检查是否正确处理了Promise错误

filters:
  - type: content
    pattern: "\\w+\\.then\\(.*\\)(?!\\s*\\.catch)"

actions:
  - type: suggest
    message: "检测到未处理的Promise链。考虑添加.catch()处理潜在错误，或使用try/catch与async/await模式。"

  - type: edit
    description: "添加catch处理程序"
    template: "{{match}}.catch(error => console.error('Error:', error))"

metadata:
  priority: high
  version: 1.0.0
  tags: ["error-handling", "promises", "best-practices"]
</rule>
```

### 2. 自动化工作流规则

这种规则用于自动化重复性的工作流任务：

```
# 自动化工作流规则示例
# 保存到 .cursor\rules\workflow\react_component.mdc

---
description: 快速创建React组件
globs: **/*.jsx,**/*.tsx
---
# React组件创建

<rule>
name: create_react_component
description: 快速创建React函数组件模板

filters:
  - type: command
    pattern: "newcomp|newreactcomp"

actions:
  - type: generate
    template: |
      import React from 'react';
      
      interface {{componentName}}Props {
        // 在此处定义组件props
      }
      
      export const {{componentName}}: React.FC<{{componentName}}Props> = (props) => {
        return (
          <div>
            {/* 组件内容 */}
          </div>
        );
      };
      
      export default {{componentName}};

  - type: prompt
    questions:
      - id: "componentName"
        question: "组件名称："
        placeholder: "MyComponent"

metadata:
  priority: medium
  version: 1.0.0
  tags: ["react", "template", "component"]
</rule>
```

### 3. 代码文档规则

这种规则帮助确保代码有适当的文档：

```
# 代码文档规则示例
# 保存到 .cursor\rules\documentation\function_docs.mdc

---
description: 检查函数文档
globs: **/*.js,**/*.ts
---
# 函数文档检查

<rule>
name: function_docs_check
description: 检查函数是否有适当的JSDoc文档

filters:
  - type: content
    pattern: "function\\s+\\w+\\s*\\([^)]*\\)|const\\s+\\w+\\s*=\\s*\\([^)]*\\)\\s*=>"
  - type: negation
    subfilters:
      - type: content
        pattern: "/\\*\\*[\\s\\S]*?\\*/"
        lookbehind: 10

actions:
  - type: suggest
    message: "为此函数添加JSDoc文档以提高可读性和可维护性。包括参数描述、返回值和示例。"

  - type: edit
    description: "添加JSDoc模板"
    template: |
      /**
       * 函数描述
       * @param {类型} 参数名 - 参数描述
       * @returns {类型} 返回值描述
       */
      {{match}}

metadata:
  priority: medium
  version: 1.0.0
  tags: ["documentation", "jsdoc", "best-practices"]
</rule>
```

## 规则测试和调试

### 测试规则的方法

1. **创建测试文件**：创建一个包含应该触发规则的内容的测试文件

2. **手动测试**：在文件上手动触发规则并验证结果
   - 在Windows环境中，你可以通过Cursor IDE中的命令面板（按下`Ctrl+Shift+P`）
   - 选择"Cursor: Run Rule"或使用规则中定义的命令触发规则

3. **使用示例**：在规则文件中添加`examples`部分，定义输入和预期输出

```
examples:
  - input: |
      var x = 10;
      var y = 20;
    output: |
      const x = 10;
      const y = 20;
```

### 调试技巧

1. **规则日志**：使用执行动作中的`echo`命令打印调试信息

```
- type: execute
  command: |
    echo "DEBUG: 规则已触发"
    echo "匹配内容: {{match}}"
```

2. **临时文件**：将中间结果保存到临时文件中进行检查

```
- type: execute
  command: |
    echo "{{match}}" > .cursor/tmp/debug.txt
```

3. **增量开发**：从简单规则开始，逐步添加更复杂的功能
   - 先创建只有一个简单过滤器和动作的规则
   - 测试它是否按预期工作
   - 然后逐步添加更复杂的过滤器和动作

4. **使用Windows的PowerShell**：在Windows环境中，可以在规则的执行动作中使用PowerShell命令

```
- type: execute
  command: |
    powershell -Command "Write-Host 'DEBUG: 规则已触发' -ForegroundColor Green"
```

## 实践示例：创建Git提交辅助规则

下面是一个实际的例子，创建一个帮助格式化Git提交消息的规则：

```
# Git提交辅助规则
# 保存到 .cursor\rules\workflow\git_commit.mdc

---
description: Git提交消息格式化辅助
globs: **/*
---
# Git提交消息格式化辅助

<rule>
name: git_commit_format
description: 帮助创建符合约定式提交规范的Git提交消息

filters:
  - type: command
    pattern: "commit|gc"

actions:
  - type: prompt
    questions:
      - id: "type"
        question: "提交类型："
        options: ["feat", "fix", "docs", "style", "refactor", "perf", "test", "chore"]
        placeholder: "请选择提交类型"
      
      - id: "scope"
        question: "影响范围（可选）："
        placeholder: "例如：auth, ui, api"
      
      - id: "description"
        question: "提交描述："
        placeholder: "简要描述此次提交的内容"
      
      - id: "body"
        question: "详细说明（可选）："
        placeholder: "提供更详细的更改说明"
        multiline: true

  - type: execute
    command: |
      # 构建提交消息
      COMMIT_MSG="${type}"
      if [ -n "${scope}" ]; then
        COMMIT_MSG="${COMMIT_MSG}(${scope})"
      fi
      COMMIT_MSG="${COMMIT_MSG}: ${description}"
      
      if [ -n "${body}" ]; then
        COMMIT_MSG="${COMMIT_MSG}
      
      ${body}"
      fi
      
      # 执行提交
      git add .
      git commit -m "${COMMIT_MSG}"
      
      echo "已创建提交: ${COMMIT_MSG}"

  - type: suggest
    message: |
      ## 约定式提交格式
      
      格式: <type>([scope]): <description>
      
      type:
      - feat: 新功能
      - fix: 修复bug
      - docs: 文档更改
      - style: 不影响代码含义的更改
      - refactor: 重构（不是新功能也不是bug修复）
      - perf: 性能改进
      - test: 添加或修正测试
      - chore: 构建过程或辅助工具的变动

metadata:
  priority: high
  version: 1.0.0
  tags: ["git", "commit", "workflow"]
</rule>
```

### Windows适配注意事项

在Windows环境中使用上述规则时，请注意以下几点：

1. **路径分隔符**：Windows使用反斜杠（`\`）作为路径分隔符，但在规则文件中建议统一使用正斜杠（`/`）

2. **Shell命令**：上述规则中的shell命令在Windows中可能无法直接运行，需要替换为PowerShell命令：

```
- type: execute
  command: |
    # Windows PowerShell版本
    $commitMsg = "$type"
    if (-not [string]::IsNullOrEmpty($scope)) {
      $commitMsg = "${commitMsg}(${scope})"
    }
    $commitMsg = "${commitMsg}: ${description}"
    
    if (-not [string]::IsNullOrEmpty($body)) {
      $commitMsg = "${commitMsg}`n`n${body}"
    }
    
    git add .
    git commit -m "$commitMsg"
    
    Write-Host "已创建提交: $commitMsg"
```

3. **命令调用**：在Windows中，可能需要显式指定使用PowerShell执行命令：

```
- type: execute
  command: |
    powershell -Command "..."
```

## 规则优化技巧

1. **使用精确的过滤器**：尽量使用精确的过滤器模式，避免误触发

2. **组合多个过滤器**：使用多个过滤器组合以提高精确度
   ```
   filters:
     - type: content
       pattern: "var\\s+\\w+"
     - type: context
       pattern: "function\\s+\\w+"
       lookbehind: 5
   ```

3. **添加否定过滤器**：使用否定过滤器排除不需要匹配的情况
   ```
   filters:
     - type: content
       pattern: "import .*"
     - type: negation
       subfilters:
         - type: content
           pattern: "import type"
   ```

4. **使用条件动作**：基于条件执行不同的动作
   ```
   actions:
     - type: conditional
       conditions:
         - validation: "{{match.length > 100}}"
           actions:
             - type: suggest
               message: "考虑将这个长函数拆分为小函数"
         - validation: "{{match.length <= 100}}"
           actions:
             - type: suggest
               message: "函数长度合适"
   ```

## 总结

在本章中，我们学习了如何编写基本的Cursor规则，包括规则的结构、常见模式和测试调试方法。通过实际示例，我们展示了如何创建代码检查规则、自动化工作流规则和文档规则，并提供了Windows环境下的特定注意事项。

通过掌握这些基础知识，你现在可以开始创建自己的规则来自动化日常工作流程和提高代码质量。记住，规则开发是一个渐进的过程，从简单开始，然后随着经验的积累逐步构建更复杂的规则系统。

## 下一步

在下一章中，我们将深入探讨高级规则技术，包括复杂规则构建、条件逻辑和分支以及高级过滤器和动作。这将帮助你构建更强大和灵活的规则系统。

## 练习

1. 创建一个检查代码中TODO注释的规则，并提示添加日期和责任人
2. 创建一个帮助生成标准API文档的规则
3. 修改本章中的Git提交辅助规则，使其适应你的项目需求
4. 创建一个规则来检测和修复常见的代码性能问题 
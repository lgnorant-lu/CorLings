# Cursor Rules 核心组件详解

规则的强大能力来源于其三个核心组件：**过滤器**、**动作**和**元数据**。理解这些组件的工作方式是创建有效规则的基础。本章将深入探讨每个组件的功能、类型和使用技巧。

## 过滤器 (Filters)

过滤器决定何时触发规则，类似于"条件检测器"。它们通过各种条件匹配文件、内容或事件，只有当所有过滤器都匹配时，规则才会被触发。

### 常用过滤器类型

#### 1. 文件类型过滤器

这类过滤器根据文件特性进行匹配：

```rule
filters:
  # 匹配文件扩展名
  - type: file_extension
    pattern: "\\.(js|ts|jsx|tsx)$"
    
  # 匹配文件名
  - type: file_name
    pattern: "^(index|main|app)"
    
  # 匹配文件路径
  - type: file_path
    pattern: "src/components/"
```

#### 2. 内容过滤器

根据文件内容进行匹配：

```rule
filters:
  # 匹配文件内容
  - type: content
    pattern: "import\\s+React"
    
  # 匹配代码结构
  - type: content
    pattern: "function\\s+\\w+\\s*\\(\\s*\\)"
```

#### 3. 事件过滤器

根据用户操作或系统事件触发：

```rule
filters:
  # 匹配文件创建事件
  - type: event
    pattern: "file_create"
    
  # 匹配文件修改事件
  - type: event
    pattern: "file_modify"
    
  # 匹配构建成功事件
  - type: event
    pattern: "build_success"
```

#### 4. 意图过滤器

根据检测到的用户意图触发：

```rule
filters:
  # 匹配用户创建组件的意图
  - type: intent
    pattern: "create_component"
    
  # 匹配用户添加测试的意图
  - type: intent
    pattern: "add_test"
```

### 高级过滤器技术

#### 1. 组合过滤器

使用逻辑操作符组合多个过滤器：

```rule
filters:
  # 使用AND组合（默认行为 - 所有过滤器必须匹配）
  - type: file_extension
    pattern: "\\.js$"
  - type: content
    pattern: "import\\s+React"
    
  # 使用OR显式组合
  - type: OR
    filters:
      - type: file_name
        pattern: "test"
      - type: file_path
        pattern: "/__tests__/"
        
  # 使用NOT否定
  - type: NOT
    filter:
      type: file_name
      pattern: "legacy"
```

#### 2. 上下文敏感过滤器

考虑文件上下文或开发环境：

```rule
filters:
  # 基于项目类型过滤
  - type: project_type
    pattern: "react"
    
  # 基于分支名称过滤
  - type: git_branch
    pattern: "^(dev|feature)"
```

#### 3. 正则表达式技巧

在 Windows 环境中编写正则表达式时的注意事项：

```rule
filters:
  # Windows路径匹配（注意双反斜杠）
  - type: file_path
    pattern: "src\\\\components"
    
  # 非贪婪匹配
  - type: content
    pattern: "function\\s+\\w+?\\s*\\("
```

## 动作 (Actions)

动作定义了规则触发后执行的操作，可以是建议、验证、执行命令或修改文件等。

### 常用动作类型

#### 1. 建议动作

向用户提供信息或建议：

```rule
actions:
  # 简单建议
  - type: suggest
    message: "考虑添加类型注释来提高代码可维护性。"
    
  # 多行详细建议
  - type: suggest
    message: |
      请确保你的React组件遵循以下规范：
      1. 使用函数组件而非类组件
      2. 使用解构接收props
      3. 为props定义明确的类型
      4. 使用合适的hooks管理状态
```

#### 2. 检查动作

验证文件内容是否符合特定条件：

```rule
actions:
  # 使用review检查多个条件
  - type: review
    criteria:
      - pattern: "import\\s+React"
        message: "✓ 已正确导入React"
        not_found_message: "✗ 缺少React导入"
        
      - pattern: "interface\\s+\\w+Props"
        message: "✓ 已定义Props接口"
        not_found_message: "✗ 缺少Props类型定义"
```

#### 3. 执行动作

执行系统命令：

```rule
actions:
  # 执行命令
  - type: execute
    command: "npx prettier --write \"$FILE\""
    
  # 条件执行
  - type: execute
    conditions:
      - validation: "[ -f package.json ]"
    command: "npm test"
```

#### 4. 强制动作

对文件内容应用强制性检查：

```rule
actions:
  # 强制特定条件
  - type: enforce
    conditions:
      - pattern: "^import React"
        message: "React必须是第一个导入项"
        
      - pattern: "export default"
        message: "组件必须使用默认导出"
```

### 高级动作技术

#### 1. 条件动作

基于条件选择不同动作：

```rule
actions:
  # 根据文件内容选择动作
  - type: conditional
    condition:
      type: content
      pattern: "class\\s+\\w+\\s+extends\\s+Component"
    then:
      type: suggest
      message: "推荐将类组件转换为函数组件。"
    else:
      type: suggest
      message: "很好，你正在使用函数组件！"
```

#### 2. 模板动作

使用模板生成代码或内容：

```rule
actions:
  # 生成代码模板
  - type: generate
    template: |
      import React from 'react';
      
      interface {{ComponentName}}Props {
        // 在此定义props
      }
      
      export function {{ComponentName}}(props: {{ComponentName}}Props) {
        return (
          <div>
            {/* 组件内容 */}
          </div>
        );
      }
      
      export default {{ComponentName}};
```

#### 3. 循环反馈动作

允许规则在特定情况下重新评估：

```rule
actions:
  # 改进后再次评估
  - type: loopback
    iterations: 3
    prompt: |
      你刚刚生成的代码不符合我们的标准。
      请修改以满足以下条件：
      1. 使用函数组件
      2. 添加TypeScript类型
      3. 确保变量命名遵循camelCase
```

## 元数据 (Metadata)

元数据提供关于规则的附加信息，如优先级、版本、标签和依赖关系等。

### 基本元数据字段

```rule
metadata:
  # 规则优先级(low, medium, high, critical)
  priority: high
  
  # 规则版本
  version: 1.2
  
  # 规则标签
  tags: ["react", "typescript", "component"]
  
  # 规则作者
  author: "Your Name"
  
  # 最后更新日期
  last_updated: "2023-03-13"
```

### 高级元数据配置

#### 1. 依赖关系

```rule
metadata:
  # 依赖其他规则
  dependencies: [
    "typescript_standards",
    "react_conventions"
  ]
  
  # 与其他规则的关系
  conflicts: [
    "legacy_component_format"
  ]
```

#### 2. 触发条件配置

```rule
metadata:
  # 应用规则的条件
  apply_when:
    project_type: "react"
    typescript: true
    
  # 禁用规则的条件
  disable_when:
    legacy_mode: true
    file_path: "vendor/**/*"
```

#### 3. 性能优化

```rule
metadata:
  # 执行优先级
  execution_order: 5
  
  # 缓存策略
  caching: true
  
  # 资源限制
  resource_limits:
    max_file_size: "1MB"
    timeout: "5s"
```

## 实际示例：构建完整规则

让我们结合前面学到的内容，创建一个完整的规则示例。这个规则用于确保 React 组件遵循团队约定：

```rule
---
description: React组件规范检查
globs: src/components/**/*.tsx
---
# React组件规范

<rule>
name: react_component_standards
description: 确保React组件遵循团队约定的编码规范和最佳实践

# 过滤器部分
filters:
  # 匹配tsx文件
  - type: file_extension
    pattern: "\\.tsx$"
    
  # 匹配components目录
  - type: file_path
    pattern: "src/components/"
    
  # 匹配看起来像React组件的内容
  - type: content
    pattern: "(?:export|function)\\s+\\w+\\s*\\(\\s*(?:props|\\{).*\\)"
    
  # 匹配文件创建或修改事件
  - type: event
    pattern: "file_create|file_modify"

# 动作部分
actions:
  # 检查组件是否符合规范
  - type: review
    criteria:
      - pattern: "import\\s+React.*?from\\s+['\"]react['\"]"
        message: "✓ 已正确导入React"
        not_found_message: "✗ 缺少React导入"
        
      - pattern: "interface\\s+\\w+Props"
        message: "✓ 已定义Props接口"
        not_found_message: "✗ 缺少Props类型定义"
        
      - pattern: "function\\s+\\w+\\s*\\(\\s*\\{.*?\\}\\s*:\\s*\\w+Props\\)"
        message: "✓ 使用解构接收已类型化的Props"
        not_found_message: "✗ 应使用解构方式接收Props并添加类型"
        
      - pattern: "export\\s+default\\s+\\w+"
        message: "✓ 使用默认导出"
        not_found_message: "✗ 组件应使用默认导出"
  
  # 提供改进建议
  - type: suggest
    conditions:
      - pattern: "class\\s+\\w+\\s+extends\\s+React\\.Component"
        not_match: true
    message: |
      您的React组件应遵循以下规范：
      
      ## 文件结构
      ```tsx
      import React, { useState, useEffect } from 'react';
      
      interface MyComponentProps {
        // props类型定义
      }
      
      function MyComponent({ prop1, prop2 }: MyComponentProps) {
        // hooks
        
        // 辅助函数
        
        // 返回JSX
        return (
          <div>
            {/* 组件内容 */}
          </div>
        );
      }
      
      export default MyComponent;
      ```
      
      ## 主要规范
      1. 使用TypeScript + 函数组件
      2. Props使用interface定义，并用解构接收
      3. 使用hooks而非生命周期方法
      4. 组件使用默认导出
      5. 文件名与组件名保持一致

  # 执行格式化
  - type: execute
    conditions:
      - validation: "which npx > /dev/null"
    command: "npx prettier --write \"$FILE\""

# 元数据
metadata:
  priority: high
  version: 1.0
  tags: ["react", "typescript", "component", "standards"]
  author: "Your Team"
  last_updated: "2023-03-13"
</rule>
```

## 组件选择指南

### 过滤器选择指南

| 场景 | 推荐过滤器 | 说明 |
|------|------------|------|
| 特定文件类型 | `file_extension` | 使用正则匹配文件扩展名 |
| 特定目录 | `file_path` | 匹配文件路径 |
| 代码模式 | `content` | 查找特定代码模式 |
| 用户操作 | `event` | 响应创建、修改等事件 |
| 开发意图 | `intent` | 检测用户的编码意图 |

### 动作选择指南

| 目的 | 推荐动作 | 说明 |
|------|----------|------|
| 提供建议 | `suggest` | 向用户提供信息或建议 |
| 检查规范 | `review` | 验证代码是否符合标准 |
| 执行命令 | `execute` | 运行系统命令 |
| 强制准则 | `enforce` | 强制应用编码准则 |
| 代码生成 | `generate` | 生成符合标准的代码 |

## 组件调试技巧

### 过滤器调试

1. **逐步添加过滤器**：从单个过滤器开始，确认其工作后再添加更多
2. **检查正则表达式**：使用在线工具测试正则表达式
3. **打印匹配结果**：使用 `console.log` 或类似机制验证匹配

### 动作调试

1. **使用suggest验证**：添加 `suggest` 动作打印调试信息
2. **检查条件**：使用 `conditions` 验证条件逻辑
3. **测试命令**：在执行 `execute` 动作前单独测试命令

## 小结

本章详细介绍了Cursor Rules的三个核心组件：过滤器、动作和元数据。掌握这些组件的功能和使用方法是创建有效规则的基础。记住：

- **过滤器**决定何时触发规则
- **动作**定义规则触发后执行的操作
- **元数据**提供规则的附加信息

通过组合这些组件，您可以创建从简单到复杂的各种规则，满足特定项目需求。

## 下一步

现在您已经了解了规则的核心组件，接下来我们将学习如何编写实用的基础规则，并了解常见的规则模式。

请继续阅读 [基础规则编写](04-BasicRules.md) 章节！ 
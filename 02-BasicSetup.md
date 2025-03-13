# Cursor Rules 基础设置与环境

在开始使用 Cursor Rules 之前，我们需要正确设置环境和理解规则文件的基本组织结构。本章将指导您完成这些初始步骤，为成功创建和应用规则奠定基础。

## 环境准备

### 1. Cursor IDE 安装

要使用 Cursor Rules，首先需要安装 Cursor IDE。Cursor 是一个基于 AI 的代码编辑器，支持规则系统。

1. 访问 [Cursor 官网](https://cursor.sh/) 下载适合您操作系统的版本
2. 在 Windows 上运行安装程序：
   ```bash
   # 下载后双击安装程序或使用命令行
   installer.exe
   ```
3. 启动 Cursor 并确保您已登录

### 2. 规则功能检查

确认您的 Cursor 版本支持规则功能：

1. 打开 Cursor IDE
2. 使用快捷键 `Ctrl+Shift+J` 或手动打开 Settings
3. 点击 `General` -> `Project Rules` -> `+ Add new rule` 以创建新规则
4. 如果没有看到规则相关设置，请更新到较新版本

## 规则目录结构

Cursor Rules 遵循特定的目录结构，这有助于组织和管理规则文件。

### 1. 标准目录结构

在项目中创建标准的规则目录结构：

```
PROJECT_ROOT/
├── .cursor/
│   ├── rules/           # 规则文件目录
│   │   ├── meta/        # 元规则（关于规则本身的规则）
│   │   ├── infra/       # 基础设施规则
│   │   ├── lang/        # 语言特定规则
│   │   ├── arch/        # 架构规则
│   │   ├── workflow/    # 工作流规则
│   │   └── business/    # 业务领域特定规则
│   ├── specs/           # 功能规格说明
│   └── scripts/         # 辅助脚本
└── ...
```

### 2. 在 Windows 上创建目录结构

在 Windows 上，您可以使用命令提示符或 PowerShell 创建这些目录：

```powershell
# 进入项目根目录
cd 您的项目路径

# 创建规则目录结构
mkdir -p .cursor\rules\meta
mkdir -p .cursor\rules\infra
mkdir -p .cursor\rules\lang
mkdir -p .cursor\rules\arch
mkdir -p .cursor\rules\workflow
mkdir -p .cursor\rules\business
mkdir -p .cursor\specs
mkdir -p .cursor\scripts
```

### 3. 规则文件放置

规则文件（`.mdc` 文件）应放在适当的子目录中：

- **meta/**：放置关于规则管理的规则
- **infra/**：放置项目基础设施的规则
- **lang/**：放置特定编程语言的规则
- **arch/**：放置架构和设计模式的规则
- **workflow/**：放置开发工作流的规则
- **business/**：放置业务逻辑的规则

## 规则文件基本结构

每个规则文件（`.mdc`）都有一个标准的结构，包含前置元数据、说明和规则定义。

### 1. 规则文件模板

以下是一个基本的规则文件模板：

```rule
---
description: 规则简短描述
globs: 适用文件范围（如 *.js, *.ts）
---
# 规则标题

详细描述文本，解释规则的用途和使用方法。

<rule>
name: rule_name
description: 规则的详细描述

# 过滤器部分 - 定义规则的触发条件
filters:
  - type: filter_type
    pattern: "pattern_string"
  - type: another_filter_type
    pattern: "another_pattern"

# 动作部分 - 定义规则触发时执行的操作
actions:
  - type: action_type
    message: |
      详细信息或建议

# 示例部分 - 提供规则使用的示例
examples:
  - input: |
      输入示例
    output: "期望输出"

# 元数据部分 - 提供规则的附加信息
metadata:
  priority: 优先级 (low, medium, high, critical)
  version: 版本号 (如 1.0)
</rule>
```

### 2. 文件命名约定

遵循一致的文件命名约定有助于管理和查找规则：

- 使用 kebab-case 命名文件 (如 `file-naming-rule.mdc`)
- 文件名应描述性地表达规则的用途
- 相关规则可使用相同前缀分组

## 创建您的第一个规则文件

让我们通过创建一个简单的规则文件来实践这些概念。此规则将确保所有规则文件都位于正确的目录中。

### 步骤 1: 创建文件

在 `.cursor/rules/meta/` 目录中创建 `rules-location.mdc` 文件：

```powershell
# 创建目录（如果尚未创建）
mkdir -p .cursor\rules\meta

# 创建文件
notepad .cursor\rules\meta\rules-location.mdc
```

### 步骤 2: 编写规则内容

将以下内容粘贴到文件中：

```rule
---
description: Cursor Rules Location
globs: *.mdc
---
# Cursor Rules Location

<rule>
name: cursor_rules_location
description: 规定Cursor规则文件的存放位置标准
filters:
  # 匹配任何.mdc文件
  - type: file_extension
    pattern: "\\.mdc$"
  # 匹配看起来像Cursor规则的文件
  - type: content
    pattern: "(?s)<rule>.*?</rule>"
  # 匹配文件创建事件
  - type: event
    pattern: "file_create"

actions:
  - type: reject
    conditions:
      - pattern: "^(?!\\.\\/\\.cursor\\/rules\\/.*\\.mdc$)"
        message: "Cursor规则文件(.mdc)必须放在.cursor/rules目录中"

  - type: suggest
    message: |
      创建Cursor规则时：

      1. 始终将规则文件放在PROJECT_ROOT/.cursor/rules/中：
         ```
         .cursor/rules/
         ├── your-rule-name.mdc
         ├── another-rule.mdc
         └── ...
         ```

      2. 遵循命名约定：
         - 使用kebab-case命名文件
         - 始终使用.mdc扩展名
         - 名称应描述规则的用途

      3. 目录结构：
         ```
         PROJECT_ROOT/
         ├── .cursor/
         │   └── rules/
         │       ├── your-rule-name.mdc
         │       └── ...
         └── ...
         ```

      4. 不要将规则文件放在：
         - 项目根目录
         - .cursor/rules外的子目录
         - 任何其他位置

metadata:
  priority: high
  version: 1.0
</rule>
```

### 步骤 3: 保存并验证

1. 保存文件
2. 在 Cursor IDE 中打开文件以验证语法正确性
3. 确认规则已被 Cursor 识别

## 规则管理最佳实践

在开始创建更多规则之前，让我们了解一些管理规则的最佳实践：

### 1. 版本控制

- 将规则文件纳入项目的版本控制系统
- 为规则文件创建 `.gitignore` 例外，确保它们被跟踪：
  ```
  # .gitignore
  !.cursor/
  !.cursor/rules/
  ```

### 2. 文档和注释

- 每个规则都应有清晰的描述和文档
- 使用详细注释解释复杂的模式或逻辑
- 提供示例说明规则的用途

### 3. 规则组织

- 将相关规则分组在同一目录中
- 使用命名约定标识相关规则
- 创建 `INDEX.md` 文件记录目录中的规则

### 4. 规则测试

- 在应用前测试规则
- 创建测试用例验证规则行为
- 逐步引入规则，确保它们按预期工作

## 常见问题与解决方案

### 问题：规则不被触发

**解决方案**：
- 检查过滤器配置是否正确
- 确认文件路径匹配规则中的 globs
- 验证事件类型是否正确（如 file_create, file_modify）

### 问题：规则文件不被识别

**解决方案**：
- 确认文件有 `.mdc` 扩展名
- 验证文件位于 `.cursor/rules/` 目录下
- 检查文件格式是否正确

### 问题：规则动作不执行

**解决方案**：
- 检查条件语法是否正确
- 确认动作类型支持（suggest, reject, enforce 等）
- 查看 Cursor 日志中的错误信息

## 设置小结

恭喜！您现在已经了解了 Cursor Rules 的基础设置和环境配置。您已经：

1. 了解了如何安装和配置 Cursor IDE
2. 学会了创建标准的规则目录结构
3. 掌握了规则文件的基本结构
4. 创建了您的第一个规则文件
5. 了解了规则管理的最佳实践

## 下一步

现在您已经设置好环境并创建了第一个规则文件，接下来我们将深入探讨规则的核心组件：过滤器、动作和元数据。这些组件是构建有效规则的基础。

请继续阅读 [规则组件详解](03-RuleComponents.md) 章节！ 
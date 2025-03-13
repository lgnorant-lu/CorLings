# CorLings 贡献指南

感谢您考虑为 CorLings (Cursor Rules Learnings) 教程系列做出贡献！社区的参与对于保持教程的更新、精确和全面至关重要。本指南将帮助您了解如何有效地参与项目，包括报告问题、提交改进和贡献新内容。

## 目录

- [参与方式](#参与方式)
- [报告问题](#报告问题)
- [提交内容改进](#提交内容改进)
- [贡献新内容](#贡献新内容)
- [本地测试](#本地测试)
- [风格指南](#风格指南)
- [审核流程](#审核流程)
- [贡献者行为准则](#贡献者行为准则)

## 参与方式

您可以通过多种方式为 CorLings 做出贡献：

1. **报告问题**：发现错误、过时的信息或不清晰的说明
2. **改进现有内容**：更新示例、修复错误、提高内容质量
3. **贡献新内容**：添加新的章节、附录或示例
4. **翻译**：将内容翻译成其他语言
5. **文档美化**：改进格式、添加图表或图像
6. **测试示例**：验证规则示例在不同环境中的工作情况

## 报告问题

如果您发现任何问题，请使用以下步骤报告：

1. 检查现有的 Issues，确保没有重复报告
2. 创建一个新的 Issue，使用提供的模板
3. 包含以下信息：
   - 问题发生的章节和页面
   - 详细描述问题
   - 可能的解决方案（如果有）
   - 环境信息（如操作系统、Cursor 版本等）
   - 截图（如果适用）

**问题报告模板**：

```markdown
## 问题描述
[清晰、简洁地描述问题]

## 发生位置
- 章节: [例如：第5章 - 高级规则技术]
- 文件: [例如：05-AdvancedRules.md]
- 行号: [例如：125-140]

## 预期行为
[描述您期望看到的内容]

## 实际行为
[描述实际显示的内容]

## 可能的解决方案
[如果您有建议的修复方法，请在此说明]

## 环境信息
- 操作系统: [例如：Windows 10]
- Cursor版本: [例如：3.2.0]
- 其他相关软件版本:

## 其他信息
[任何可能有助于理解或修复问题的信息]
```

## 提交内容改进

要提交对现有内容的改进，请按照以下步骤操作：

1. Fork 项目仓库
2. 创建一个新的分支（`fix/chapter-2-examples`）
3. 进行必要的更改
4. 验证更改（确保内容准确且遵循风格指南）
5. 提交 Pull Request（PR）

**提交规范**：
- 使用明确的提交消息，简要说明更改内容
- 遵循格式：`[章节编号] 更改类型: 简短描述`
  - 例如：`[04] fix: 修复JavaScript示例中的语法错误`
  - 更改类型：`fix`（修复错误）、`update`（更新内容）、`improve`（改进格式等）

## 贡献新内容

如果您想贡献新章节或重要内容，建议先创建一个 Issue 讨论您的想法，以确保它符合项目的总体方向。

贡献新内容的步骤：

1. 创建一个 Issue 描述您计划添加的内容
2. 获得项目维护者的反馈和批准
3. Fork 项目并创建一个新分支
4. 按照项目的结构和风格创建新内容
5. 提交 Pull Request

**新内容提案模板**：

```markdown
## 内容提案

### 标题
[例如：Cursor Rules与CI/CD集成最佳实践]

### 内容类型
- [ ] 新章节
- [ ] 现有章节的子部分
- [ ] 附录
- [ ] 案例研究
- [ ] 其他: _____________

### 概述
[简要描述您计划添加的内容]

### 大纲
[提供内容的详细大纲]

### 相关资源
[列出您将使用的任何资源或参考]

### 预计完成时间
[您计划何时完成这项贡献]
```

## 本地测试

在提交贡献之前，请确保在本地测试您的更改：

1. 确保所有Markdown格式正确
2. 验证所有链接都正确指向目标
3. 测试代码示例确保它们能够正常工作
4. 使用Markdown预览工具检查格式

**PowerShell 测试脚本示例**：

```powershell
# 检查Markdown语法
if (Get-Command markdownlint -ErrorAction SilentlyContinue) {
    Write-Host "正在检查Markdown语法..."
    markdownlint *.md
} else {
    Write-Host "未安装markdownlint，跳过Markdown语法检查"
}

# 检查规则示例语法
$ruleExamples = Select-String -Path *.md -Pattern "```rule" -Context 0,50
foreach ($example in $ruleExamples) {
    $ruleContent = $example.Context.PostContext -join "`n"
    $ruleContent = $ruleContent.Substring(0, $ruleContent.IndexOf("```"))
    
    # 这里可以添加规则语法验证逻辑
    Write-Host "验证规则示例: $($example.Filename):$($example.LineNumber)"
}

# 检查链接有效性
$mdFiles = Get-ChildItem -Filter "*.md"
foreach ($file in $mdFiles) {
    $content = Get-Content $file -Raw
    $links = [regex]::Matches($content, '\[.*?\]\((.*?)\)')
    
    foreach ($link in $links) {
        $linkUrl = $link.Groups[1].Value
        # 处理相对链接
        if (-not $linkUrl.StartsWith("http")) {
            # 验证本地文件链接
            $targetPath = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine([System.IO.Path]::GetDirectoryName($file.FullName), $linkUrl))
            if (-not (Test-Path $targetPath)) {
                Write-Host "警告: 在文件 $($file.Name) 中发现无效链接: $linkUrl"
            }
        }
    }
}
```

## 风格指南

为确保教程内容的一致性，请遵循以下风格指南：

### Markdown格式

- 使用 ATX 风格的标题（`#` 符号）
- 嵌套标题应当遵循层级（不跳过级别）
- 代码块使用三个反引号和语言标识符（```javascript）
- 使用无序列表时，统一使用 `-` 符号
- 使用有序列表时，所有数字使用 `1.` （Markdown会自动编号）

### 内容风格

- 使用简洁、明确的语言
- 避免使用过于口语化的表达
- 保持专业术语的一致性
- 提供足够的上下文和解释
- 每个章节应有明确的学习目标和小结
- 代码示例应当完整且可执行
- 包含注释以解释复杂的代码
- 同时提供Windows和Unix/Linux的命令示例

### 文件组织

- 遵循既定的文件命名约定：`章节序号-主题名[-Part部分号].md`
- 新增章节或部分应遵循现有的编号系统
- 图像文件放在 `images` 目录，按章节组织

### 规则示例风格

所有Cursor Rules示例应遵循以下格式：

```rule
<rule>
name: descriptive_rule_name
description: 清晰的中文描述

filters:
  - type: filter_type
    pattern: "正则表达式模式"

actions:
  - type: action_type
    parameter: value

metadata:
  priority: medium
  version: 1.0.0
  tags: ["tag1", "tag2"]
</rule>
```

## 审核流程

所有贡献都将经过以下审核流程：

1. 自动化检查：确保符合基本格式要求
2. 初步审核：项目维护者进行初步评估
3. 详细审核：内容、技术准确性和风格审核
4. 反馈和修订：可能需要进行修改
5. 最终审核和合并：通过所有检查后合并到主分支

**审核标准**：
- 技术准确性：内容是否正确
- 完整性：是否包含必要信息
- 清晰度：是否易于理解
- 一致性：是否与现有内容风格一致
- 实用性：示例是否实用且可行

## 贡献者行为准则

作为 CorLings 的贡献者，我们希望您：

- 尊重所有参与者，不分背景和经验水平
- 接受建设性的批评和反馈
- 专注于项目的最佳利益
- 展示同理心和理解
- 避免攻击性或贬低性语言

不当行为可能导致暂时或永久禁止参与项目。

---

再次感谢您为 CorLings 做出贡献！您的帮助对于使这个教程系列成为 Cursor Rules 学习的全面资源至关重要。如果您有任何问题或需要帮助，请随时联系项目维护者。

祝您贡献愉快！ 
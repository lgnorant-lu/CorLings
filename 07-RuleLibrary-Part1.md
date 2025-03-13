# 规则库管理（第一部分）

## 概述

随着您创建的规则数量增加，有效管理这些规则变得至关重要。规则库是规则的集合，经过良好组织和管理，可以提高规则的可重用性、可维护性和共享性。本章将探讨如何创建、组织、分类和维护规则库，帮助您实现规则资产的最大价值。

## 学习目标

- 了解规则库的概念和结构
- 学习创建个人规则库的方法和最佳实践
- 掌握规则组织和分类的策略
- 了解规则版本控制和维护的技术

## 规则库基础

### 什么是规则库

规则库（Rule Library）是一组有组织的规则集合，它们按照特定的结构和分类进行管理。规则库可以是：

1. **个人规则库**：供个人开发者使用的规则集合
2. **团队规则库**：团队共享和协作开发的规则集合
3. **组织规则库**：整个组织范围内使用的标准规则集合
4. **公共规则库**：开源社区分享的规则集合

### 规则库的价值

规则库带来的主要价值包括：

- **可重用性**：避免重复创建类似功能的规则
- **一致性**：确保相同任务使用统一的规则
- **知识共享**：将个人经验转化为团队资产
- **效率提升**：快速找到并应用合适的规则
- **质量保证**：经过验证的规则可以保持一致的质量标准

### 规则库的结构

一个典型的规则库结构包括：

```
rules-library/
├── categories/           # 按类别组织的规则
│   ├── code-quality/
│   ├── workflow/
│   └── documentation/
├── templates/            # 规则模板
├── shared/               # 共享组件和辅助函数
└── metadata/             # 规则库元数据
```

## 创建个人规则库

个人规则库是您自己创建和维护的规则集合，它是规则库管理的起点。

### 设置规则库目录

首先，让我们创建一个基本的规则库目录结构：

```bash
# 创建规则库目录
mkdir -p ~/cursor-rules-library
cd ~/cursor-rules-library

# 创建基本目录结构
mkdir -p categories/{code-quality,workflow,documentation}
mkdir -p templates
mkdir -p shared
mkdir -p metadata
```

在Windows PowerShell中，可以使用以下命令：

```powershell
# 创建规则库目录
$libraryPath = "$HOME\cursor-rules-library"
New-Item -Path $libraryPath -ItemType Directory -Force

# 创建基本目录结构
New-Item -Path "$libraryPath\categories\code-quality" -ItemType Directory -Force
New-Item -Path "$libraryPath\categories\workflow" -ItemType Directory -Force
New-Item -Path "$libraryPath\categories\documentation" -ItemType Directory -Force
New-Item -Path "$libraryPath\templates" -ItemType Directory -Force
New-Item -Path "$libraryPath\shared" -ItemType Directory -Force
New-Item -Path "$libraryPath\metadata" -ItemType Directory -Force
```

### 创建规则库清单

接下来，创建一个规则库清单文件，用于描述规则库的基本信息：

```bash
# 创建规则库清单
cat > ~/cursor-rules-library/library.json << EOL
{
  "name": "Personal Cursor Rules Library",
  "description": "我的个人Cursor规则集合",
  "version": "1.0.0",
  "author": "Your Name",
  "created": "$(date '+%Y-%m-%d')",
  "updated": "$(date '+%Y-%m-%d')",
  "categories": [
    "code-quality",
    "workflow",
    "documentation"
  ],
  "rules_count": 0
}
EOL
```

在Windows PowerShell中，可以这样创建：

```powershell
# 创建规则库清单
$currentDate = Get-Date -Format "yyyy-MM-dd"
$libraryJson = @"
{
  "name": "Personal Cursor Rules Library",
  "description": "我的个人Cursor规则集合",
  "version": "1.0.0",
  "author": "Your Name",
  "created": "$currentDate",
  "updated": "$currentDate",
  "categories": [
    "code-quality",
    "workflow",
    "documentation"
  ],
  "rules_count": 0
}
"@
$libraryJson | Set-Content -Path "$libraryPath\library.json"
```

### 创建规则模板

规则模板可以帮助您更快地创建新规则。以下是一个基本的规则模板：

```bash
# 创建基本规则模板
cat > ~/cursor-rules-library/templates/basic-rule.mdc << EOL
---
description: 规则描述
globs: **/*
---
# 规则标题

<rule>
name: rule_name
description: 详细描述规则的用途

filters:
  - type: filter_type
    pattern: "pattern"

actions:
  - type: action_type
    message: |
      消息内容

metadata:
  priority: medium
  version: 1.0.0
  tags: ["tag1", "tag2"]
  category: "category-name"
  author: "Your Name"
  created: "$(date '+%Y-%m-%d')"
  updated: "$(date '+%Y-%m-%d')"
</rule>
EOL
```

在Windows PowerShell中：

```powershell
# 创建基本规则模板
$currentDate = Get-Date -Format "yyyy-MM-dd"
$basicRuleTemplate = @"
---
description: 规则描述
globs: **/*
---
# 规则标题

<rule>
name: rule_name
description: 详细描述规则的用途

filters:
  - type: filter_type
    pattern: "pattern"

actions:
  - type: action_type
    message: |
      消息内容

metadata:
  priority: medium
  version: 1.0.0
  tags: ["tag1", "tag2"]
  category: "category-name"
  author: "Your Name"
  created: "$currentDate"
  updated: "$currentDate"
</rule>
"@
$basicRuleTemplate | Set-Content -Path "$libraryPath\templates\basic-rule.mdc"
```

### 添加示例规则

让我们添加一个示例规则到规则库：

```bash
# 创建示例规则
cat > ~/cursor-rules-library/categories/code-quality/js-best-practices.mdc << EOL
---
description: JavaScript最佳实践检查
globs: **/*.js,**/*.jsx,**/*.ts,**/*.tsx
---
# JavaScript最佳实践

<rule>
name: js_best_practices
description: 检查JavaScript代码中的常见最佳实践

filters:
  - type: file_extension
    pattern: "\\.(js|jsx|ts|tsx)$"
  
  - type: content
    pattern: "var\\s+\\w+"

actions:
  - type: suggest
    message: |
      ## JavaScript最佳实践建议
      
      检测到使用 \`var\` 声明变量。推荐使用 \`const\` 或 \`let\` 来声明变量，以获得更好的作用域控制：
      
      ```javascript
      // 不推荐
      var x = 10;
      
      // 推荐
      const x = 10; // 对于不会改变的值
      let y = 20;   // 对于可能会改变的值
      ```
      
      使用 \`const\` 和 \`let\` 的好处：
      - 块级作用域，避免变量提升问题
      - \`const\` 可以防止变量被意外重新赋值
      - 代码更容易理解和维护

metadata:
  priority: high
  version: 1.0.0
  tags: ["javascript", "best-practices", "code-quality"]
  category: "code-quality"
  author: "Your Name"
  created: "$(date '+%Y-%m-%d')"
  updated: "$(date '+%Y-%m-%d')"
</rule>
EOL
```

在Windows PowerShell中：

```powershell
# 创建示例规则
$currentDate = Get-Date -Format "yyyy-MM-dd"
$jsBestPracticesRule = @"
---
description: JavaScript最佳实践检查
globs: **/*.js,**/*.jsx,**/*.ts,**/*.tsx
---
# JavaScript最佳实践

<rule>
name: js_best_practices
description: 检查JavaScript代码中的常见最佳实践

filters:
  - type: file_extension
    pattern: "\\.(js|jsx|ts|tsx)$"
  
  - type: content
    pattern: "var\\s+\\w+"

actions:
  - type: suggest
    message: |
      ## JavaScript最佳实践建议
      
      检测到使用 \`var\` 声明变量。推荐使用 \`const\` 或 \`let\` 来声明变量，以获得更好的作用域控制：
      
      ```javascript
      // 不推荐
      var x = 10;
      
      // 推荐
      const x = 10; // 对于不会改变的值
      let y = 20;   // 对于可能会改变的值
      ```
      
      使用 \`const\` 和 \`let\` 的好处：
      - 块级作用域，避免变量提升问题
      - \`const\` 可以防止变量被意外重新赋值
      - 代码更容易理解和维护

metadata:
  priority: high
  version: 1.0.0
  tags: ["javascript", "best-practices", "code-quality"]
  category: "code-quality"
  author: "Your Name"
  created: "$currentDate"
  updated: "$currentDate"
</rule>
"@
$jsBestPracticesRule | Set-Content -Path "$libraryPath\categories\code-quality\js-best-practices.mdc"
```

### 创建规则库索引

为了更好地管理规则，让我们创建一个索引文件，记录规则库中的所有规则：

```bash
# 创建规则库索引
cat > ~/cursor-rules-library/rules-index.json << EOL
{
  "rules": [
    {
      "id": "js_best_practices",
      "name": "JavaScript最佳实践",
      "description": "检查JavaScript代码中的常见最佳实践",
      "path": "categories/code-quality/js-best-practices.mdc",
      "category": "code-quality",
      "tags": ["javascript", "best-practices", "code-quality"],
      "version": "1.0.0",
      "created": "$(date '+%Y-%m-%d')",
      "updated": "$(date '+%Y-%m-%d')"
    }
  ]
}
EOL
```

在Windows PowerShell中：

```powershell
# 创建规则库索引
$currentDate = Get-Date -Format "yyyy-MM-dd"
$rulesIndexJson = @"
{
  "rules": [
    {
      "id": "js_best_practices",
      "name": "JavaScript最佳实践",
      "description": "检查JavaScript代码中的常见最佳实践",
      "path": "categories/code-quality/js-best-practices.mdc",
      "category": "code-quality",
      "tags": ["javascript", "best-practices", "code-quality"],
      "version": "1.0.0",
      "created": "$currentDate",
      "updated": "$currentDate"
    }
  ]
}
"@
$rulesIndexJson | Set-Content -Path "$libraryPath\rules-index.json"
```

### 创建规则库管理脚本

为了简化规则库的管理，我们可以创建一个管理脚本。以下是一个基本的脚本示例：

```bash
# 创建规则库管理脚本
cat > ~/cursor-rules-library/manage-library.sh << EOL
#!/bin/bash

# Cursor规则库管理脚本

LIBRARY_DIR="\$HOME/cursor-rules-library"
RULES_INDEX="\$LIBRARY_DIR/rules-index.json"
LIBRARY_JSON="\$LIBRARY_DIR/library.json"

function show_help {
    echo "Cursor规则库管理工具"
    echo ""
    echo "用法:"
    echo "  ./manage-library.sh [命令] [参数]"
    echo ""
    echo "命令:"
    echo "  list                列出所有规则"
    echo "  add [模板] [路径]    添加新规则"
    echo "  find [关键词]       搜索规则"
    echo "  update [id] [路径]  更新规则"
    echo "  help               显示帮助信息"
}

function list_rules {
    echo "规则库中的规则:"
    jq -r '.rules[] | "- \(.id): \(.name) [\(.category)]\"" "\$RULES_INDEX"
}

function find_rules {
    if [ -z "\$1" ]; then
        echo "错误: 请提供搜索关键词"
        return 1
    fi
    
    echo "搜索关键词: \$1"
    jq -r ".rules[] | select(.name | contains(\"\$1\") or .description | contains(\"\$1\") or .tags[] | contains(\"\$1\")) | \"- \(.id): \(.name) [\(.category)]\"" "\$RULES_INDEX"
}

function add_rule {
    if [ -z "\$1" ] || [ -z "\$2" ]; then
        echo "错误: 请提供模板和目标路径"
        echo "用法: ./manage-library.sh add [模板] [路径]"
        return 1
    fi
    
    TEMPLATE="\$LIBRARY_DIR/templates/\$1.mdc"
    TARGET="\$LIBRARY_DIR/\$2"
    
    if [ ! -f "\$TEMPLATE" ]; then
        echo "错误: 模板 '\$1' 不存在"
        return 1
    fi
    
    mkdir -p "\$(dirname "\$TARGET")"
    cp "\$TEMPLATE" "\$TARGET"
    echo "创建新规则: \$TARGET"
    echo "请编辑新创建的规则文件"
}

function update_rule {
    if [ -z "\$1" ] || [ -z "\$2" ]; then
        echo "错误: 请提供规则ID和新路径"
        echo "用法: ./manage-library.sh update [id] [路径]"
        return 1
    fi
    
    # 更新规则索引
    TMP_FILE="\$(mktemp)"
    jq ".rules[] | select(.id == \"\$1\").updated = \"$(date '+%Y-%m-%d')\"" "\$RULES_INDEX" > "\$TMP_FILE"
    mv "\$TMP_FILE" "\$RULES_INDEX"
    
    echo "更新规则 '\$1' 到 '\$2'"
}

# 主函数
case "\$1" in
    list)
        list_rules
        ;;
    find)
        find_rules "\$2"
        ;;
    add)
        add_rule "\$2" "\$3"
        ;;
    update)
        update_rule "\$2" "\$3"
        ;;
    help|*)
        show_help
        ;;
esac
EOL

# 添加执行权限
chmod +x ~/cursor-rules-library/manage-library.sh
```

在Windows PowerShell中，我们可以创建一个PowerShell脚本：

```powershell
# 创建规则库管理脚本
$manageLibraryScript = @"
# Cursor规则库管理脚本

`$libraryDir = "`$HOME\cursor-rules-library"
`$rulesIndex = "`$libraryDir\rules-index.json"
`$libraryJson = "`$libraryDir\library.json"

function Show-Help {
    Write-Output "Cursor规则库管理工具"
    Write-Output ""
    Write-Output "用法:"
    Write-Output "  .\manage-library.ps1 [命令] [参数]"
    Write-Output ""
    Write-Output "命令:"
    Write-Output "  list                列出所有规则"
    Write-Output "  add [模板] [路径]    添加新规则"
    Write-Output "  find [关键词]       搜索规则"
    Write-Output "  update [id] [路径]  更新规则"
    Write-Output "  help               显示帮助信息"
}

function List-Rules {
    Write-Output "规则库中的规则:"
    `$rules = Get-Content -Path `$rulesIndex | ConvertFrom-Json
    foreach (`$rule in `$rules.rules) {
        Write-Output "- `$(`$rule.id): `$(`$rule.name) [`$(`$rule.category)]"
    }
}

function Find-Rules {
    param (
        [string]`$keyword
    )
    
    if (-not `$keyword) {
        Write-Output "错误: 请提供搜索关键词"
        return
    }
    
    Write-Output "搜索关键词: `$keyword"
    `$rules = Get-Content -Path `$rulesIndex | ConvertFrom-Json
    foreach (`$rule in `$rules.rules) {
        if (`$rule.name -like "*`$keyword*" -or 
            `$rule.description -like "*`$keyword*" -or 
            `$rule.tags -contains `$keyword) {
            Write-Output "- `$(`$rule.id): `$(`$rule.name) [`$(`$rule.category)]"
        }
    }
}

function Add-Rule {
    param (
        [string]`$template,
        [string]`$path
    )
    
    if (-not `$template -or -not `$path) {
        Write-Output "错误: 请提供模板和目标路径"
        Write-Output "用法: .\manage-library.ps1 add [模板] [路径]"
        return
    }
    
    `$templatePath = "`$libraryDir\templates\`$template.mdc"
    `$targetPath = "`$libraryDir\`$path"
    
    if (-not (Test-Path -Path `$templatePath -PathType Leaf)) {
        Write-Output "错误: 模板 '`$template' 不存在"
        return
    }
    
    `$targetDir = Split-Path -Path `$targetPath -Parent
    if (-not (Test-Path -Path `$targetDir -PathType Container)) {
        New-Item -Path `$targetDir -ItemType Directory -Force
    }
    
    Copy-Item -Path `$templatePath -Destination `$targetPath
    Write-Output "创建新规则: `$targetPath"
    Write-Output "请编辑新创建的规则文件"
}

function Update-RuleItem {
    param (
        [string]`$id,
        [string]`$newPath
    )
    
    if (-not `$id -or -not `$newPath) {
        Write-Output "错误: 请提供规则ID和新路径"
        Write-Output "用法: .\manage-library.ps1 update [id] [路径]"
        return
    }
    
    # 更新规则索引
    `$rules = Get-Content -Path `$rulesIndex | ConvertFrom-Json
    foreach (`$rule in `$rules.rules) {
        if (`$rule.id -eq `$id) {
            `$rule.updated = (Get-Date -Format "yyyy-MM-dd")
            `$rule.path = `$newPath
        }
    }
    
    `$rules | ConvertTo-Json -Depth 10 | Set-Content -Path `$rulesIndex
    Write-Output "更新规则 '`$id' 到 '`$newPath'"
}

# 主函数
`$command = `$args[0]
switch (`$command) {
    "list" {
        List-Rules
    }
    "find" {
        Find-Rules -keyword `$args[1]
    }
    "add" {
        Add-Rule -template `$args[1] -path `$args[2]
    }
    "update" {
        Update-RuleItem -id `$args[1] -newPath `$args[2]
    }
    default {
        Show-Help
    }
}
"@
$manageLibraryScript | Set-Content -Path "$libraryPath\manage-library.ps1"
```

### 链接到项目

最后，我们可以创建一个符号链接，将规则库链接到当前项目：

```bash
# 链接规则库到当前项目
PROJECT_DIR=$(pwd)
mkdir -p "$PROJECT_DIR/.cursor/rules"
ln -sf ~/cursor-rules-library/categories/code-quality/js-best-practices.mdc "$PROJECT_DIR/.cursor/rules/js-best-practices.mdc"
```

在Windows PowerShell中，可以使用以下命令创建符号链接（需要管理员权限）：

```powershell
# 链接规则库到当前项目
$projectDir = Get-Location
New-Item -Path "$projectDir\.cursor\rules" -ItemType Directory -Force
New-Item -ItemType SymbolicLink -Path "$projectDir\.cursor\rules\js-best-practices.mdc" -Target "$HOME\cursor-rules-library\categories\code-quality\js-best-practices.mdc"
```

如果没有管理员权限，可以使用复制替代：

```powershell
# 复制规则到当前项目
$projectDir = Get-Location
New-Item -Path "$projectDir\.cursor\rules" -ItemType Directory -Force
Copy-Item -Path "$HOME\cursor-rules-library\categories\code-quality\js-best-practices.mdc" -Destination "$projectDir\.cursor\rules\js-best-practices.mdc"
```

## 使用个人规则库

创建好个人规则库后，您可以使用以下方法将其应用到项目中：

### 1. 从规则库导入规则

```bash
# 将规则从规则库导入到项目
cp ~/cursor-rules-library/categories/code-quality/js-best-practices.mdc .cursor/rules/
```

### 2. 使用管理脚本

```bash
# 列出规则库中的所有规则
~/cursor-rules-library/manage-library.sh list

# 添加新规则
~/cursor-rules-library/manage-library.sh add basic-rule categories/workflow/git-commit.mdc

# 搜索规则
~/cursor-rules-library/manage-library.sh find javascript
```

### 3. 创建规则引用文件

您可以创建一个引用文件，指向规则库中的规则：

```bash
# 创建引用文件
cat > .cursor/rules/library-refs.json << EOL
{
  "references": [
    {
      "id": "js_best_practices",
      "source": "$HOME/cursor-rules-library/categories/code-quality/js-best-practices.mdc"
    }
  ]
}
EOL
```

在下一部分，我们将探讨如何有效地组织和分类规则，以便更好地管理您的规则库。 
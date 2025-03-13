# 规则库管理（第二部分）

## 规则组织和分类

随着规则库的增长，规则的组织和分类变得至关重要。一个良好的组织结构可以帮助您和您的团队快速找到需要的规则，并确保规则的可维护性。

### 规则分类策略

#### 1. 基于功能的分类

根据规则的功能和用途进行分类是最常用的方法之一：

```
rules-library/
├── code-quality/          # 代码质量检查规则
├── documentation/         # 文档生成和验证规则
├── workflow/              # 工作流自动化规则
├── testing/               # 测试相关规则
└── security/              # 安全检查规则
```

**优点**：
- 规则的功能一目了然
- 易于查找特定目的的规则
- 与开发流程中的实际需求对应

**示例**：

```bash
# 创建基于功能的分类目录
mkdir -p ~/cursor-rules-library/categories/{code-quality,documentation,workflow,testing,security}
```

在Windows PowerShell中：

```powershell
# 创建基于功能的分类目录
$libraryPath = "$HOME\cursor-rules-library"
New-Item -Path "$libraryPath\categories\code-quality" -ItemType Directory -Force
New-Item -Path "$libraryPath\categories\documentation" -ItemType Directory -Force
New-Item -Path "$libraryPath\categories\workflow" -ItemType Directory -Force
New-Item -Path "$libraryPath\categories\testing" -ItemType Directory -Force
New-Item -Path "$libraryPath\categories\security" -ItemType Directory -Force
```

#### 2. 基于技术栈的分类

根据规则适用的技术栈或编程语言进行分类：

```
rules-library/
├── javascript/        # JavaScript相关规则
├── python/            # Python相关规则
├── react/             # React相关规则
├── nodejs/            # Node.js相关规则
└── database/          # 数据库相关规则
```

**优点**：
- 针对特定技术的规则集中管理
- 便于技术专家维护
- 与项目的技术选择直接对应

**示例**：

```bash
# 创建基于技术栈的分类目录
mkdir -p ~/cursor-rules-library/tech-stack/{javascript,python,react,nodejs,database}
```

在Windows PowerShell中：

```powershell
# 创建基于技术栈的分类目录
New-Item -Path "$libraryPath\tech-stack\javascript" -ItemType Directory -Force
New-Item -Path "$libraryPath\tech-stack\python" -ItemType Directory -Force
New-Item -Path "$libraryPath\tech-stack\react" -ItemType Directory -Force
New-Item -Path "$libraryPath\tech-stack\nodejs" -ItemType Directory -Force
New-Item -Path "$libraryPath\tech-stack\database" -ItemType Directory -Force
```

#### 3. 基于团队的分类

在大型组织中，可以按照团队职责划分规则：

```
rules-library/
├── frontend/          # 前端团队规则
├── backend/           # 后端团队规则
├── devops/            # DevOps团队规则
├── data-science/      # 数据科学团队规则
└── security/          # 安全团队规则
```

**优点**：
- 明确规则的所有权和维护责任
- 符合组织结构
- 方便团队协作和知识共享

### 使用标签系统

除了目录结构外，使用标签系统可以提供更灵活的分类方式：

```json
{
  "id": "js_best_practices",
  "name": "JavaScript最佳实践",
  "tags": ["javascript", "best-practices", "code-quality", "es6", "linting"]
}
```

这样，一个规则可以同时属于多个类别，便于通过不同维度查找。

### 创建标签索引

为了有效利用标签系统，可以创建一个标签索引文件：

```bash
# 创建标签索引
cat > ~/cursor-rules-library/tags-index.json << EOL
{
  "tags": {
    "javascript": [
      "js_best_practices",
      "js_performance_checks"
    ],
    "best-practices": [
      "js_best_practices",
      "python_code_style",
      "react_component_standards"
    ],
    "code-quality": [
      "js_best_practices",
      "code_complexity_checker",
      "duplicate_code_detector"
    ]
  }
}
EOL
```

在Windows PowerShell中：

```powershell
# 创建标签索引
$tagsIndexJson = @"
{
  "tags": {
    "javascript": [
      "js_best_practices",
      "js_performance_checks"
    ],
    "best-practices": [
      "js_best_practices",
      "python_code_style",
      "react_component_standards"
    ],
    "code-quality": [
      "js_best_practices",
      "code_complexity_checker",
      "duplicate_code_detector"
    ]
  }
}
"@
$tagsIndexJson | Set-Content -Path "$libraryPath\tags-index.json"
```

### 组织优化技巧

#### 1. 创建README文件

在每个目录中添加README文件，描述该目录的规则用途和使用方法：

```bash
# 创建README文件
cat > ~/cursor-rules-library/categories/code-quality/README.md << EOL
# 代码质量规则

本目录包含用于检查和提高代码质量的规则。

## 规则列表

- **js_best_practices**: JavaScript编码最佳实践检查
- **code_complexity_checker**: 代码复杂度检查
- **duplicate_code_detector**: 重复代码检测

## 使用指南

将这些规则添加到项目的\`.cursor/rules/\`目录中，以启用代码质量检查。

## 贡献指南

添加新规则时，请确保:
1. 遵循命名约定
2. 提供详细文档
3. 添加示例
EOL
```

在Windows PowerShell中：

```powershell
# 创建README文件
$readmeContent = @"
# 代码质量规则

本目录包含用于检查和提高代码质量的规则。

## 规则列表

- **js_best_practices**: JavaScript编码最佳实践检查
- **code_complexity_checker**: 代码复杂度检查
- **duplicate_code_detector**: 重复代码检测

## 使用指南

将这些规则添加到项目的`.cursor/rules/`目录中，以启用代码质量检查。

## 贡献指南

添加新规则时，请确保:
1. 遵循命名约定
2. 提供详细文档
3. 添加示例
"@
$readmeContent | Set-Content -Path "$libraryPath\categories\code-quality\README.md"
```

#### 2. 创建规则集

规则集是一组相关规则的集合，可以一次性应用到项目中：

```bash
# 创建规则集
cat > ~/cursor-rules-library/rule-sets/javascript-standards.json << EOL
{
  "name": "JavaScript Standards",
  "description": "JavaScript编码标准规则集",
  "version": "1.0.0",
  "rules": [
    "js_best_practices",
    "js_performance_checks",
    "js_security_rules"
  ]
}
EOL
```

在Windows PowerShell中：

```powershell
# 创建规则集目录
New-Item -Path "$libraryPath\rule-sets" -ItemType Directory -Force

# 创建规则集
$ruleSetContent = @"
{
  "name": "JavaScript Standards",
  "description": "JavaScript编码标准规则集",
  "version": "1.0.0",
  "rules": [
    "js_best_practices",
    "js_performance_checks",
    "js_security_rules"
  ]
}
"@
$ruleSetContent | Set-Content -Path "$libraryPath\rule-sets\javascript-standards.json"
```

#### 3. 创建导入脚本

为了方便将规则集应用到项目中，可以创建导入脚本：

```bash
# 创建导入脚本
cat > ~/cursor-rules-library/scripts/import-ruleset.sh << EOL
#!/bin/bash

# 导入规则集到项目

if [ -z "\$1" ] || [ -z "\$2" ]; then
    echo "用法: ./import-ruleset.sh <规则集名称> <项目目录>"
    exit 1
fi

RULESET_NAME="\$1"
PROJECT_DIR="\$2"
LIBRARY_DIR="\$HOME/cursor-rules-library"
RULESET_FILE="\$LIBRARY_DIR/rule-sets/\$RULESET_NAME.json"

if [ ! -f "\$RULESET_FILE" ]; then
    echo "错误: 规则集 '\$RULESET_NAME' 不存在"
    exit 1
fi

# 创建项目规则目录
mkdir -p "\$PROJECT_DIR/.cursor/rules"

# 读取规则集
RULES=\$(jq -r '.rules[]' "\$RULESET_FILE")

# 导入规则
for RULE in \$RULES; do
    # 查找规则文件路径
    RULE_PATH=\$(jq -r ".rules[] | select(.id == \"\$RULE\") | .path" "\$LIBRARY_DIR/rules-index.json")
    
    if [ -n "\$RULE_PATH" ] && [ -f "\$LIBRARY_DIR/\$RULE_PATH" ]; then
        cp "\$LIBRARY_DIR/\$RULE_PATH" "\$PROJECT_DIR/.cursor/rules/"
        echo "导入规则: \$RULE"
    else
        echo "警告: 找不到规则 '\$RULE'"
    fi
done

echo "规则集 '\$RULESET_NAME' 已导入到项目 '\$PROJECT_DIR'"
EOL

# 添加执行权限
chmod +x ~/cursor-rules-library/scripts/import-ruleset.sh
```

在Windows PowerShell中：

```powershell
# 创建脚本目录
New-Item -Path "$libraryPath\scripts" -ItemType Directory -Force

# 创建导入脚本
$importScriptContent = @"
# 导入规则集到项目

param (
    [string]`$RuleSetName,
    [string]`$ProjectDir
)

if (-not `$RuleSetName -or -not `$ProjectDir) {
    Write-Output "用法: .\import-ruleset.ps1 <规则集名称> <项目目录>"
    exit 1
}

`$libraryDir = "`$HOME\cursor-rules-library"
`$ruleSetFile = "`$libraryDir\rule-sets\`$RuleSetName.json"

if (-not (Test-Path -Path `$ruleSetFile -PathType Leaf)) {
    Write-Output "错误: 规则集 '`$RuleSetName' 不存在"
    exit 1
}

# a项目规则目录
if (-not (Test-Path -Path "`$ProjectDir\.cursor\rules" -PathType Container)) {
    New-Item -Path "`$ProjectDir\.cursor\rules" -ItemType Directory -Force
}

# 读取规则集
`$ruleSet = Get-Content -Path `$ruleSetFile | ConvertFrom-Json
`$rules = `$ruleSet.rules

# 读取规则索引
`$rulesIndex = Get-Content -Path "`$libraryDir\rules-index.json" | ConvertFrom-Json

# 导入规则
foreach (`$rule in `$rules) {
    # 查找规则文件路径
    `$rulePath = `$null
    foreach (`$indexRule in `$rulesIndex.rules) {
        if (`$indexRule.id -eq `$rule) {
            `$rulePath = `$indexRule.path
            break
        }
    }
    
    if (`$rulePath -and (Test-Path -Path "`$libraryDir\`$rulePath" -PathType Leaf)) {
        Copy-Item -Path "`$libraryDir\`$rulePath" -Destination "`$ProjectDir\.cursor\rules\"
        Write-Output "导入规则: `$rule"
    } else {
        Write-Output "警告: 找不到规则 '`$rule'"
    }
}

Write-Output "规则集 '`$RuleSetName' 已导入到项目 '`$ProjectDir'"
"@
$importScriptContent | Set-Content -Path "$libraryPath\scripts\import-ruleset.ps1"
```

### 规则组织最佳实践

#### 1. 一致的命名约定

使用一致的命名约定使规则更易于查找和理解：

- **规则ID**：使用下划线命名法，如 `js_best_practices`
- **规则文件**：使用连字符命名法，如 `js-best-practices.mdc`
- **目录名**：使用连字符命名法，如 `code-quality`

#### 2. 避免重复规则

在添加新规则前，检查是否已存在类似功能的规则：

```bash
# 搜索现有规则
grep -r "var\\s+\\w+" ~/cursor-rules-library/categories/
```

在Windows PowerShell中：

```powershell
# 搜索现有规则
Get-ChildItem -Path "$libraryPath\categories" -Recurse -File | Select-String -Pattern "var\\s+\\w+"
```

#### 3. 规则依赖管理

如果规则之间存在依赖关系，在元数据中明确标出：

```rule
metadata:
  dependencies: [
    "base_style_rules",
    "common_patterns"
  ]
</rule>
```

并创建依赖图以可视化依赖关系：

```bash
# 创建依赖图
cat > ~/cursor-rules-library/metadata/dependencies.json << EOL
{
  "dependencies": {
    "js_best_practices": ["base_style_rules", "common_patterns"],
    "react_component_standards": ["js_best_practices"],
    "typescript_rules": ["js_best_practices"]
  }
}
EOL
```

在Windows PowerShell中：

```powershell
# 创建依赖图
$dependenciesJson = @"
{
  "dependencies": {
    "js_best_practices": ["base_style_rules", "common_patterns"],
    "react_component_standards": ["js_best_practices"],
    "typescript_rules": ["js_best_practices"]
  }
}
"@
$dependenciesJson | Set-Content -Path "$libraryPath\metadata\dependencies.json"
```

#### 4. 规则文档模板

为每个规则创建一个文档模板，确保文档的完整性：

```bash
# 创建规则文档模板
cat > ~/cursor-rules-library/templates/rule-docs-template.md << EOL
# {{RULE_NAME}}

## 概述

{{RULE_DESCRIPTION}}

## 用途

- {{PURPOSE_1}}
- {{PURPOSE_2}}
- {{PURPOSE_3}}

## 配置

```json
{
  "option1": "value1",
  "option2": "value2"
}
```

## 示例

### 触发规则的代码

```javascript
{{BAD_CODE_EXAMPLE}}
```

### 符合规则的代码

```javascript
{{GOOD_CODE_EXAMPLE}}
```

## 相关规则

- {{RELATED_RULE_1}}
- {{RELATED_RULE_2}}

## 维护者

- {{MAINTAINER_NAME}} ({{MAINTAINER_EMAIL}})
EOL
```

在Windows PowerShell中：

```powershell
# 创建规则文档模板
$ruleDocsTemplate = @"
# {{RULE_NAME}}

## 概述

{{RULE_DESCRIPTION}}

## 用途

- {{PURPOSE_1}}
- {{PURPOSE_2}}
- {{PURPOSE_3}}

## 配置

```json
{
  "option1": "value1",
  "option2": "value2"
}
```

## 示例

### 触发规则的代码

```javascript
{{BAD_CODE_EXAMPLE}}
```

### 符合规则的代码

```javascript
{{GOOD_CODE_EXAMPLE}}
```

## 相关规则

- {{RELATED_RULE_1}}
- {{RELATED_RULE_2}}

## 维护者

- {{MAINTAINER_NAME}} ({{MAINTAINER_EMAIL}})
"@
$ruleDocsTemplate | Set-Content -Path "$libraryPath\templates\rule-docs-template.md"
```

### 规则组织工具

为了更好地管理规则库，可以创建一些辅助工具：

#### 1. 规则目录生成器

```bash
# 创建规则目录生成器
cat > ~/cursor-rules-library/scripts/generate-rules-directory.sh << EOL
#!/bin/bash

# 生成规则目录结构

LIBRARY_DIR="\$HOME/cursor-rules-library"
OUTPUT_FILE="\$LIBRARY_DIR/rules-directory.md"

echo "# Cursor Rules 目录" > "\$OUTPUT_FILE"
echo "" >> "\$OUTPUT_FILE"
echo "生成时间: \$(date '+%Y-%m-%d %H:%M:%S')" >> "\$OUTPUT_FILE"
echo "" >> "\$OUTPUT_FILE"

# 遍历分类目录
for CATEGORY_DIR in \$LIBRARY_DIR/categories/*; do
    if [ -d "\$CATEGORY_DIR" ]; then
        CATEGORY=\$(basename "\$CATEGORY_DIR")
        echo "## \${CATEGORY^}" >> "\$OUTPUT_FILE"
        echo "" >> "\$OUTPUT_FILE"
        
        # 查找该分类下的规则
        for RULE_FILE in "\$CATEGORY_DIR"/*.mdc; do
            if [ -f "\$RULE_FILE" ]; then
                RULE_NAME=\$(grep -m 1 "^name:" "\$RULE_FILE" | sed 's/name: //')
                RULE_DESCRIPTION=\$(grep -m 1 "^description:" "\$RULE_FILE" | sed 's/description: //')
                
                echo "- **\$RULE_NAME**: \$RULE_DESCRIPTION" >> "\$OUTPUT_FILE"
            fi
        done
        
        echo "" >> "\$OUTPUT_FILE"
    fi
done

echo "规则目录已生成到: \$OUTPUT_FILE"
EOL

# 添加执行权限
chmod +x ~/cursor-rules-library/scripts/generate-rules-directory.sh
```

在Windows PowerShell中：

```powershell
# 创建规则目录生成器
$directoryGeneratorScript = @"
# 生成规则目录结构

`$libraryDir = "`$HOME\cursor-rules-library"
`$outputFile = "`$libraryDir\rules-directory.md"

"# Cursor Rules 目录" | Set-Content -Path `$outputFile
"" | Add-Content -Path `$outputFile
"生成时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Add-Content -Path `$outputFile
"" | Add-Content -Path `$outputFile

# 遍历分类目录
Get-ChildItem -Path "`$libraryDir\categories" -Directory | ForEach-Object {
    `$category = `$_.Name
    `$categoryName = (Get-Culture).TextInfo.ToTitleCase(`$category.Replace('-', ' '))
    
    "## `$categoryName" | Add-Content -Path `$outputFile
    "" | Add-Content -Path `$outputFile
    
    # 查找该分类下的规则
    Get-ChildItem -Path "`$(`$_.FullName)" -Filter "*.mdc" | ForEach-Object {
        `$content = Get-Content -Path `$_.FullName
        `$ruleName = `$content | Where-Object { `$_ -match '^name:' } | Select-Object -First 1 | ForEach-Object { `$_ -replace 'name: ', '' }
        `$ruleDescription = `$content | Where-Object { `$_ -match '^description:' } | Select-Object -First 1 | ForEach-Object { `$_ -replace 'description: ', '' }
        
        "- **`$ruleName**: `$ruleDescription" | Add-Content -Path `$outputFile
    }
    
    "" | Add-Content -Path `$outputFile
}

Write-Output "规则目录已生成到: `$outputFile"
"@
$directoryGeneratorScript | Set-Content -Path "$libraryPath\scripts\generate-rules-directory.ps1"
```

#### 2. 规则统计工具

```bash
# 创建规则统计工具
cat > ~/cursor-rules-library/scripts/rules-stats.sh << EOL
#!/bin/bash

# 生成规则库统计信息

LIBRARY_DIR="\$HOME/cursor-rules-library"

# 计算总规则数
TOTAL_RULES=\$(find "\$LIBRARY_DIR/categories" -name "*.mdc" | wc -l)

# 按分类统计
echo "按分类统计规则数量:"
for CATEGORY_DIR in \$LIBRARY_DIR/categories/*; do
    if [ -d "\$CATEGORY_DIR" ]; then
        CATEGORY=\$(basename "\$CATEGORY_DIR")
        COUNT=\$(find "\$CATEGORY_DIR" -name "*.mdc" | wc -l)
        echo "- \${CATEGORY}: \$COUNT"
    fi
done

# 按标签统计
echo -e "\n按标签统计规则数量:"
for TAG in \$(jq -r '.tags | keys[]' "\$LIBRARY_DIR/tags-index.json"); do
    COUNT=\$(jq -r ".tags.\"\$TAG\" | length" "\$LIBRARY_DIR/tags-index.json")
    echo "- \$TAG: \$COUNT"
done

echo -e "\n总规则数: \$TOTAL_RULES"
EOL

# 添加执行权限
chmod +x ~/cursor-rules-library/scripts/rules-stats.sh
```

在Windows PowerShell中：

```powershell
# 创建规则统计工具
$statsScript = @"
# 生成规则库统计信息

`$libraryDir = "`$HOME\cursor-rules-library"

# 计算总规则数
`$totalRules = (Get-ChildItem -Path "`$libraryDir\categories" -Recurse -Filter "*.mdc" | Measure-Object).Count

# 按分类统计
Write-Output "按分类统计规则数量:"
Get-ChildItem -Path "`$libraryDir\categories" -Directory | ForEach-Object {
    `$category = `$_.Name
    `$count = (Get-ChildItem -Path `$_.FullName -Filter "*.mdc" | Measure-Object).Count
    Write-Output "- `$category: `$count"
}

# 按标签统计
Write-Output "`n按标签统计规则数量:"
`$tagsIndex = Get-Content -Path "`$libraryDir\tags-index.json" | ConvertFrom-Json
`$tagsIndex.tags.PSObject.Properties | ForEach-Object {
    `$tag = `$_.Name
    `$count = `$_.Value.Count
    Write-Output "- `$tag: `$count"
}

Write-Output "`n总规则数: `$totalRules"
"@
$statsScript | Set-Content -Path "$libraryPath\scripts\rules-stats.ps1"
```

在下一部分，我们将探讨规则的版本控制和维护策略，帮助您管理规则库的生命周期。 
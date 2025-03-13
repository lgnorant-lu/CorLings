# 规则库管理（第三部分）

## 规则版本控制和维护

随着时间的推移，规则库需要不断更新和演进。本节将探讨如何通过版本控制和维护策略来管理规则的生命周期，确保规则库保持最佳状态。

### 规则版本控制基础

#### 1. 版本号策略

为规则制定合理的版本号策略是管理规则演进的基础。推荐使用语义化版本号（Semantic Versioning）：

```
主版本号.次版本号.修订号
```

- **主版本号**：当做了不兼容的API修改时递增
- **次版本号**：当做了向下兼容的功能性新增时递增
- **修订号**：当做了向下兼容的问题修正时递增

示例规则版本元数据：

```rule
metadata:
  version: 1.2.3  # 主版本.次版本.修订号
  updated: "2023-03-14"
  changelog: "修复了正则表达式匹配问题"
</rule>
```

#### 2. 版本历史记录

为每个规则维护版本历史记录，帮助追踪规则的变更：

```bash
# 创建版本历史记录文件
cat > ~/cursor-rules-library/categories/code-quality/js-best-practices.changelog.md << EOL
# JavaScript最佳实践规则变更日志

## 版本 1.0.0 (2023-03-13)
- 初始版本
- 添加var使用检测
- 添加建议信息

## 版本 1.1.0 (2023-03-14)
- 添加箭头函数风格检查
- 改进建议信息格式

## 版本 1.1.1 (2023-03-14)
- 修复正则表达式匹配问题
- 优化性能
EOL
```

在Windows PowerShell中：

```powershell
# 创建版本历史记录文件
$changelogContent = @"
# JavaScript最佳实践规则变更日志

## 版本 1.0.0 (2023-03-13)
- 初始版本
- 添加var使用检测
- 添加建议信息

## 版本 1.1.0 (2023-03-14)
- 添加箭头函数风格检查
- 改进建议信息格式

## 版本 1.1.1 (2023-03-14)
- 修复正则表达式匹配问题
- 优化性能
"@
$changelogContent | Set-Content -Path "$libraryPath\categories\code-quality\js-best-practices.changelog.md"
```

#### 3. 使用Git进行版本控制

将规则库纳入Git版本控制系统是管理规则变更的最佳方式：

```bash
# 初始化规则库的Git仓库
cd ~/cursor-rules-library
git init
git add .
git commit -m "初始化规则库"
```

在Windows PowerShell中：

```powershell
# 初始化规则库的Git仓库
Set-Location -Path $libraryPath
git init
git add .
git commit -m "初始化规则库"
```

创建`.gitignore`文件，排除不需要版本控制的文件：

```bash
# 创建.gitignore文件
cat > ~/cursor-rules-library/.gitignore << EOL
# 临时文件
*.tmp
*.temp

# 日志文件
*.log

# 个人配置
.user-config.json

# 缓存目录
.cache/
EOL
```

在Windows PowerShell中：

```powershell
# 创建.gitignore文件
$gitignoreContent = @"
# 临时文件
*.tmp
*.temp

# 日志文件
*.log

# 个人配置
.user-config.json

# 缓存目录
.cache/
"@
$gitignoreContent | Set-Content -Path "$libraryPath\.gitignore"
```

### 规则升级策略

随着项目需求的变化和技术的发展，规则需要不断升级和更新。以下是管理规则升级的策略：

#### 1. 向后兼容性原则

尽量保持规则的向后兼容性，避免破坏现有项目：

- **修订版本**：只修复问题，不改变行为
- **次版本**：添加新功能，但保持现有功能不变
- **主版本**：可以进行不兼容更改，但需要明确标注并提供迁移路径

#### 2. 编写升级指南

对于重大版本更新，提供详细的升级指南：

```bash
# 创建升级指南
cat > ~/cursor-rules-library/docs/upgrading-to-v2.md << EOL
# 升级到规则库2.0版本指南

本文档提供从规则库1.x版本升级到2.0版本的详细指导。

## 主要变更

- **正则表达式语法变更**：所有规则现在使用标准ECMAScript正则表达式语法
- **动作API更新**：`suggest`动作的参数结构已更改
- **新增过滤器类型**：添加了`semantic`和`context_aware`两种过滤器类型

## 升级步骤

1. **备份现有规则**：
   \`\`\`bash
   cp -r .cursor/rules .cursor/rules.backup
   \`\`\`

2. **更新规则库**：
   \`\`\`bash
   git pull origin v2.0.0
   \`\`\`

3. **迁移自定义规则**：
   - 更新正则表达式语法
   - 调整动作参数结构
   - 查看是否可以利用新过滤器类型

## 已知问题

- 一些复杂的正则表达式可能需要手动调整
- 旧版本的模板规则需要重新生成

## 帮助和支持

如有问题，请联系规则库维护团队或提交Issue。
EOL
```

在Windows PowerShell中：

```powershell
# 创建docs目录
New-Item -Path "$libraryPath\docs" -ItemType Directory -Force

# 创建升级指南
$upgradeGuideContent = @"
# 升级到规则库2.0版本指南

本文档提供从规则库1.x版本升级到2.0版本的详细指导。

## 主要变更

- **正则表达式语法变更**：所有规则现在使用标准ECMAScript正则表达式语法
- **动作API更新**：`suggest`动作的参数结构已更改
- **新增过滤器类型**：添加了`semantic`和`context_aware`两种过滤器类型

## 升级步骤

1. **备份现有规则**：
   ```powershell
   Copy-Item -Path ".cursor\rules" -Destination ".cursor\rules.backup" -Recurse
   ```

2. **更新规则库**：
   ```powershell
   git pull origin v2.0.0
   ```

3. **迁移自定义规则**：
   - 更新正则表达式语法
   - 调整动作参数结构
   - 查看是否可以利用新过滤器类型

## 已知问题

- 一些复杂的正则表达式可能需要手动调整
- 旧版本的模板规则需要重新生成

## 帮助和支持

如有问题，请联系规则库维护团队或提交Issue。
"@
$upgradeGuideContent | Set-Content -Path "$libraryPath\docs\upgrading-to-v2.md"
```

#### 3. 版本迁移工具

为了简化升级过程，可以创建版本迁移工具：

```bash
# 创建版本迁移脚本
cat > ~/cursor-rules-library/scripts/migrate-to-v2.sh << EOL
#!/bin/bash

# 规则库迁移脚本：从v1迁移到v2

echo "开始迁移规则库到v2.0版本..."

# 设置目录
LIBRARY_DIR="\$HOME/cursor-rules-library"
BACKUP_DIR="\$LIBRARY_DIR/backups/v1-$(date '+%Y%m%d')"

# 创建备份
echo "创建备份到 \$BACKUP_DIR..."
mkdir -p "\$BACKUP_DIR"
cp -r "\$LIBRARY_DIR/categories" "\$BACKUP_DIR/"
cp -r "\$LIBRARY_DIR/templates" "\$BACKUP_DIR/"
cp "\$LIBRARY_DIR/rules-index.json" "\$BACKUP_DIR/"

# 更新正则表达式语法
echo "更新正则表达式语法..."
find "\$LIBRARY_DIR/categories" -name "*.mdc" -type f -exec sed -i 's/\\\\\\\\w/\\\\w/g' {} \\;

# 更新动作结构
echo "更新动作结构..."
find "\$LIBRARY_DIR/categories" -name "*.mdc" -type f -exec sed -i 's/message:/content:/g' {} \\;

# 更新版本号
echo "更新版本号..."
find "\$LIBRARY_DIR/categories" -name "*.mdc" -type f -exec sed -i 's/version: 1\\.\\([0-9]\\+\\)\\.\\([0-9]\\+\\)/version: 2.0.0/g' {} \\;

# 更新索引文件
echo "更新索引文件..."
jq '.rules[].version = "2.0.0"' "\$LIBRARY_DIR/rules-index.json" > "\$LIBRARY_DIR/rules-index.json.new"
mv "\$LIBRARY_DIR/rules-index.json.new" "\$LIBRARY_DIR/rules-index.json"

echo "迁移完成！"
echo "如果出现任何问题，可以从备份 \$BACKUP_DIR 恢复。"
EOL

# 添加执行权限
chmod +x ~/cursor-rules-library/scripts/migrate-to-v2.sh
```

在Windows PowerShell中：

```powershell
# 创建版本迁移脚本
$migrateScriptContent = @"
# 规则库迁移脚本：从v1迁移到v2

Write-Output "开始迁移规则库到v2.0版本..."

# 设置目录
`$libraryDir = "`$HOME\cursor-rules-library"
`$backupDir = "`$libraryDir\backups\v1-$(Get-Date -Format 'yyyyMMdd')"

# 创建备份
Write-Output "创建备份到 `$backupDir..."
if (-not (Test-Path -Path `$backupDir -PathType Container)) {
    New-Item -Path `$backupDir -ItemType Directory -Force
}
Copy-Item -Path "`$libraryDir\categories" -Destination `$backupDir -Recurse
Copy-Item -Path "`$libraryDir\templates" -Destination `$backupDir -Recurse
Copy-Item -Path "`$libraryDir\rules-index.json" -Destination `$backupDir

# 更新正则表达式语法
Write-Output "更新正则表达式语法..."
Get-ChildItem -Path "`$libraryDir\categories" -Filter "*.mdc" -Recurse | ForEach-Object {
    `$content = Get-Content -Path `$_.FullName -Raw
    `$updatedContent = `$content -replace '\\\\w', '\w'
    Set-Content -Path `$_.FullName -Value `$updatedContent
}

# 更新动作结构
Write-Output "更新动作结构..."
Get-ChildItem -Path "`$libraryDir\categories" -Filter "*.mdc" -Recurse | ForEach-Object {
    `$content = Get-Content -Path `$_.FullName -Raw
    `$updatedContent = `$content -replace 'message:', 'content:'
    Set-Content -Path `$_.FullName -Value `$updatedContent
}

# 更新版本号
Write-Output "更新版本号..."
Get-ChildItem -Path "`$libraryDir\categories" -Filter "*.mdc" -Recurse | ForEach-Object {
    `$content = Get-Content -Path `$_.FullName -Raw
    `$updatedContent = `$content -replace 'version: 1\.[0-9]+\.[0-9]+', 'version: 2.0.0'
    Set-Content -Path `$_.FullName -Value `$updatedContent
}

# 更新索引文件
Write-Output "更新索引文件..."
`$rulesIndex = Get-Content -Path "`$libraryDir\rules-index.json" | ConvertFrom-Json
foreach (`$rule in `$rulesIndex.rules) {
    `$rule.version = "2.0.0"
}
`$rulesIndex | ConvertTo-Json -Depth 10 | Set-Content -Path "`$libraryDir\rules-index.json"

Write-Output "迁移完成！"
Write-Output "如果出现任何问题，可以从备份 `$backupDir 恢复。"
"@
$migrateScriptContent | Set-Content -Path "$libraryPath\scripts\migrate-to-v2.ps1"
```

在下一部分，我们将继续探讨规则维护的高级策略和团队协作管理方法。 
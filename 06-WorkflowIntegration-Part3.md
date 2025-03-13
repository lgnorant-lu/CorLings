# 工作流集成（第三部分）

## 与其他工具协作

Cursor规则的强大之处在于能够与其他开发工具协作，形成完整的工具链。本节探讨如何将规则与常用开发工具集成，创建无缝的开发体验。

### 与版本控制系统集成

版本控制系统（如Git）是现代开发工作流的核心。Cursor规则可以增强版本控制系统的功能。

#### 1. Git提交增强

规则可以帮助团队遵循一致的提交消息格式和工作流：

```rule
<rule>
name: git_commit_formatter
description: 强制使用约定式提交格式并进行提交前检查

filters:
  - type: command
    pattern: "git commit|commit|git-commit"

actions:
  - type: prompt
    questions:
      - id: "commit_type"
        question: "提交类型:"
        options: ["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"]
        placeholder: "选择提交类型"
      
      - id: "commit_scope"
        question: "影响范围 (可选):"
        placeholder: "例如: auth, api, ui"
        required: false
      
      - id: "commit_description"
        question: "简短描述:"
        placeholder: "描述此次更改的内容"
  
  - type: execute
    command: |
      echo "执行提交前检查..."
      
      # 检查是否有未暂存文件
      UNSTAGED=$(git diff --name-only)
      if [ -n "$UNSTAGED" ]; then
        echo "WARNING: 检测到未暂存的更改:"
        echo "$UNSTAGED"
        
        read -p "是否要将这些更改添加到此次提交? (y/n): " ADD_UNSTAGED
        if [ "$ADD_UNSTAGED" = "y" ]; then
          git add .
          echo "已添加所有文件到暂存区"
        fi
      fi
      
      # 运行Lint检查
      echo "运行Lint检查..."
      if command -v eslint &> /dev/null; then
        eslint --ext .js,.jsx,.ts,.tsx src/ || {
          echo "WARNING: ESLint检查发现问题"
          read -p "是否继续提交? (y/n): " CONTINUE_COMMIT
          if [ "$CONTINUE_COMMIT" != "y" ]; then
            echo "提交已取消。请修复Lint问题后再提交。"
            exit 1
          fi
        }
      fi
      
      # 运行测试
      echo "运行单元测试..."
      npm test -- --watchAll=false || {
        echo "WARNING: 测试失败"
        read -p "是否继续提交? (y/n): " CONTINUE_COMMIT
        if [ "$CONTINUE_COMMIT" != "y" ]; then
          echo "提交已取消。请修复测试问题后再提交。"
          exit 1
        fi
      }
      
      # 构建提交消息
      COMMIT_MSG=""
      if [ -n "{{commit_scope}}" ]; then
        COMMIT_MSG="{{commit_type}}({{commit_scope}}): {{commit_description}}"
      else
        COMMIT_MSG="{{commit_type}}: {{commit_description}}"
      fi
      
      # 执行提交
      git commit -m "$COMMIT_MSG"
      
      echo "提交成功: $COMMIT_MSG"
  
  - type: suggest
    message: |
      ## 提交已完成 ✅
      
      已使用约定式提交格式创建提交：
      
      ```
      {{commit_type}}{{commit_scope ? `(${commit_scope})` : ''}}: {{commit_description}}
      ```
      
      ### 提交前检查
      
      - ✓ 文件暂存状态检查
      - ✓ Lint代码质量检查
      - ✓ 单元测试运行
      
      ### 下一步
      
      您可以使用 `git push` 将提交推送到远程仓库。

metadata:
  priority: high
  version: 1.0.0
  tags: ["git", "commit", "workflow"]
</rule>
```

在Windows PowerShell环境中，可以调整为：

```powershell
Write-Output "执行提交前检查..."

# 检查是否有未暂存文件
$unstaged = git diff --name-only
if ($unstaged) {
    Write-Output "WARNING: 检测到未暂存的更改:"
    Write-Output $unstaged
    
    $addUnstaged = Read-Host "是否要将这些更改添加到此次提交? (y/n)"
    if ($addUnstaged -eq "y") {
        git add .
        Write-Output "已添加所有文件到暂存区"
    }
}

# 运行Lint检查
Write-Output "运行Lint检查..."
if (Get-Command eslint -ErrorAction SilentlyContinue) {
    $eslintResult = $null
    try {
        $eslintResult = eslint --ext .js,.jsx,.ts,.tsx src/
    }
    catch {
        Write-Output "WARNING: ESLint检查发现问题"
        $continueCommit = Read-Host "是否继续提交? (y/n)"
        if ($continueCommit -ne "y") {
            Write-Output "提交已取消。请修复Lint问题后再提交。"
            exit 1
        }
    }
}

# 运行测试
Write-Output "运行单元测试..."
try {
    npm test -- --watchAll=false
}
catch {
    Write-Output "WARNING: 测试失败"
    $continueCommit = Read-Host "是否继续提交? (y/n)"
    if ($continueCommit -ne "y") {
        Write-Output "提交已取消。请修复测试问题后再提交。"
        exit 1
    }
}

# 构建提交消息
$commitMsg = if ($commitScope) {
    "$commitType($commitScope): $commitDescription"
} else {
    "$commitType: $commitDescription"
}

# 执行提交
git commit -m $commitMsg

Write-Output "提交成功: $commitMsg"
```

#### 2. 分支管理与合并

规则可以帮助团队管理分支和合并过程：

```rule
<rule>
name: branch_and_merge_manager
description: 帮助管理分支创建、同步和合并流程

filters:
  - type: command
    pattern: "branch-(create|sync|merge) (\\w+)(?:\\s+from\\s+(\\w+))?"
    capture_as: [
      "action",
      "branch_name",
      "source_branch"
    ]

actions:
  - type: branch
    property: "{{captures.action}}"
    branches:
      "create":
        - type: execute
          command: |
            # 设置源分支（默认为main）
            SOURCE_BRANCH="{{captures.source_branch || 'main'}}"
            
            echo "从 $SOURCE_BRANCH 创建新分支 {{captures.branch_name}}..."
            
            # 检查当前工作区状态
            if [ -n "$(git status --porcelain)" ]; then
              echo "WARNING: 当前工作区有未提交的更改。"
              read -p "是否继续? (y/n): " CONTINUE
              if [ "$CONTINUE" != "y" ]; then
                echo "操作已取消。"
                exit 1
              fi
            fi
            
            # 检查源分支是否存在
            git fetch
            if ! git show-ref --verify --quiet refs/heads/$SOURCE_BRANCH && ! git show-ref --verify --quiet refs/remotes/origin/$SOURCE_BRANCH; then
              echo "ERROR: 源分支 '$SOURCE_BRANCH' 不存在。"
              exit 1
            fi
            
            # 确保源分支是最新的
            git checkout $SOURCE_BRANCH
            git pull
            
            # 创建新分支
            git checkout -b {{captures.branch_name}}
            
            echo "分支 {{captures.branch_name}} 已创建"
        
        - type: suggest
          message: |
            ## 分支创建成功 ✅
            
            已从 `{{captures.source_branch || 'main'}}` 创建新分支 `{{captures.branch_name}}`。
            
            您现在可以开始在此分支上进行开发。完成后，使用以下命令合并回目标分支：
            
            ```bash
            branch-merge {{captures.branch_name}} to {{captures.source_branch || 'main'}}
            ```
      
      "sync":
        - type: execute
          command: |
            # 设置源分支（默认为main）
            SOURCE_BRANCH="{{captures.source_branch || 'main'}}"
            
            echo "同步分支 {{captures.branch_name}} 与 $SOURCE_BRANCH..."
            
            # 保存当前分支
            CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
            
            # 检查当前工作区状态
            if [ -n "$(git status --porcelain)" ]; then
              echo "WARNING: 当前工作区有未提交的更改。"
              read -p "是否暂存这些更改? (y/n): " STASH_CHANGES
              if [ "$STASH_CHANGES" = "y" ]; then
                git stash
                echo "已暂存更改"
              else
                echo "WARNING: 继续操作可能会导致冲突。"
                read -p "是否继续? (y/n): " CONTINUE
                if [ "$CONTINUE" != "y" ]; then
                  echo "操作已取消。"
                  exit 1
                fi
              fi
            fi
            
            # 更新源分支
            git fetch
            git checkout $SOURCE_BRANCH
            git pull
            
            # 切换到目标分支并合并源分支
            git checkout {{captures.branch_name}}
            git merge $SOURCE_BRANCH
            
            # 处理可能的冲突
            if [ $? -ne 0 ]; then
              echo "WARNING: 合并过程中发生冲突。请解决冲突后手动完成合并。"
              exit 1
            fi
            
            # 如果之前暂存了更改，恢复它们
            if [ "$STASH_CHANGES" = "y" ]; then
              git stash pop
              echo "已恢复暂存的更改"
            fi
            
            # 如果不是在目标分支上操作，恢复到原始分支
            if [ "$CURRENT_BRANCH" != "{{captures.branch_name}}" ]; then
              git checkout $CURRENT_BRANCH
              echo "已恢复到原始分支 $CURRENT_BRANCH"
            fi
            
            echo "分支 {{captures.branch_name}} 已与 $SOURCE_BRANCH 同步"
        
        - type: suggest
          message: |
            ## 分支同步成功 ✅
            
            已将 `{{captures.branch_name}}` 与 `{{captures.source_branch || 'main'}}` 同步。
            
            分支现在包含了 `{{captures.source_branch || 'main'}}` 的最新更改。
      
      "merge":
        - type: execute
          command: |
            # 设置目标分支（默认为main）
            TARGET_BRANCH="{{captures.source_branch || 'main'}}"
            
            echo "将分支 {{captures.branch_name}} 合并到 $TARGET_BRANCH..."
            
            # 保存当前分支
            CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
            
            # 检查当前工作区状态
            if [ -n "$(git status --porcelain)" ]; then
              echo "WARNING: 当前工作区有未提交的更改。"
              read -p "是否提交这些更改? (y/n): " COMMIT_CHANGES
              if [ "$COMMIT_CHANGES" = "y" ]; then
                git add .
                read -p "提交信息: " COMMIT_MSG
                git commit -m "$COMMIT_MSG"
                echo "已提交更改"
              else
                echo "WARNING: 继续操作将不包括未提交的更改。"
                read -p "是否继续? (y/n): " CONTINUE
                if [ "$CONTINUE" != "y" ]; then
                  echo "操作已取消。"
                  exit 1
                fi
              fi
            fi
            
            # 确保分支是最新的
            git checkout {{captures.branch_name}}
            git pull origin {{captures.branch_name}} || true
            
            # 更新目标分支
            git fetch
            git checkout $TARGET_BRANCH
            git pull
            
            # 执行合并
            git merge --no-ff {{captures.branch_name}} -m "Merge branch '{{captures.branch_name}}' into $TARGET_BRANCH"
            
            # 处理可能的冲突
            if [ $? -ne 0 ]; then
              echo "WARNING: 合并过程中发生冲突。请解决冲突后手动完成合并。"
              exit 1
            fi
            
            # 推送合并结果
            git push origin $TARGET_BRANCH
            
            # 如果不是在目标分支上操作，恢复到原始分支
            if [ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]; then
              git checkout $CURRENT_BRANCH
              echo "已恢复到原始分支 $CURRENT_BRANCH"
            fi
            
            # 询问是否删除已合并的分支
            read -p "是否删除已合并的分支 {{captures.branch_name}}? (y/n): " DELETE_BRANCH
            if [ "$DELETE_BRANCH" = "y" ]; then
              git branch -d {{captures.branch_name}}
              git push origin --delete {{captures.branch_name}} || true
              echo "已删除分支 {{captures.branch_name}}"
            fi
            
            echo "分支 {{captures.branch_name}} 已合并到 $TARGET_BRANCH"
        
        - type: suggest
          message: |
            ## 分支合并成功 ✅
            
            已将 `{{captures.branch_name}}` 合并到 `{{captures.source_branch || 'main'}}`。
            
            合并后的更改已推送到远程仓库。
            {{DELETE_BRANCH === 'y' ? '\n已删除分支 `' + captures.branch_name + '`。' : ''}}

metadata:
  priority: high
  version: 1.0.0
  tags: ["git", "branch", "merge", "workflow"]
</rule>
```

在Windows PowerShell环境中，分支创建部分可以调整为：

```powershell
# 设置源分支（默认为main）
$sourceBranch = if ($captures.source_branch) { $captures.source_branch } else { "main" }

Write-Output "从 $sourceBranch 创建新分支 $($captures.branch_name)..."

# 检查当前工作区状态
$uncommittedChanges = git status --porcelain
if ($uncommittedChanges) {
    Write-Output "WARNING: 当前工作区有未提交的更改。"
    $continue = Read-Host "是否继续? (y/n)"
    if ($continue -ne "y") {
        Write-Output "操作已取消。"
        exit 1
    }
}

# 检查源分支是否存在
git fetch
$localBranchExists = git show-ref --verify --quiet refs/heads/$sourceBranch 2>$null
$remoteBranchExists = git show-ref --verify --quiet refs/remotes/origin/$sourceBranch 2>$null

if (-not $localBranchExists -and -not $remoteBranchExists) {
    Write-Output "ERROR: 源分支 '$sourceBranch' 不存在。"
    exit 1
}

# 确保源分支是最新的
git checkout $sourceBranch
git pull

# 创建新分支
git checkout -b $($captures.branch_name)

Write-Output "分支 $($captures.branch_name) 已创建"
```

### 与代码检查工具集成

集成代码检查工具可以确保代码质量和一致性。

#### 1. 与ESLint集成

规则可以将ESLint集成到工作流中：

```rule
<rule>
name: eslint_integration
description: 集成ESLint进行代码质量检查

filters:
  - type: file_change
    pattern: ".*\\.(js|jsx|ts|tsx)$"
  
  - type: command
    pattern: "lint|eslint|check"

actions:
  - type: execute
    command: |
      echo "运行ESLint检查..."
      
      # 检查ESLint是否已安装
      if ! command -v eslint &> /dev/null; then
        echo "ESLint未安装，正在安装..."
        npm install eslint --save-dev
      fi
      
      # 检查是否有ESLint配置文件
      if [ ! -f ".eslintrc.js" ] && [ ! -f ".eslintrc.json" ] && [ ! -f ".eslintrc.yml" ]; then
        echo "未检测到ESLint配置文件，创建默认配置..."
        cat > .eslintrc.js << EOL
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: [
    'react',
    '@typescript-eslint',
  ],
  rules: {
    // 自定义规则
  },
};
EOL
        
        # 安装必要的依赖
        npm install --save-dev eslint-plugin-react @typescript-eslint/eslint-plugin @typescript-eslint/parser
        
        echo "已创建ESLint配置文件"
      fi
      
      # 确定检查范围
      if [ -n "{{file_path}}" ]; then
        # 检查单个文件
        LINT_TARGET="{{file_path}}"
      else
        # 检查整个项目
        LINT_TARGET="src/"
      fi
      
      # 运行ESLint
      eslint $LINT_TARGET --fix
      
      # 捕获ESLint结果
      LINT_RESULT=$?
      LINT_OUTPUT=$(eslint $LINT_TARGET -f json)
      
      # 计算错误和警告数量
      ERROR_COUNT=$(echo $LINT_OUTPUT | grep -o '"errorCount":[0-9]*' | grep -o '[0-9]*' | awk '{sum+=$1} END {print sum}')
      WARNING_COUNT=$(echo $LINT_OUTPUT | grep -o '"warningCount":[0-9]*' | grep -o '[0-9]*' | awk '{sum+=$1} END {print sum}')
      
      echo "ESLint检查完成: $ERROR_COUNT 个错误, $WARNING_COUNT 个警告"
  
  - type: branch
    property: "{{ERROR_COUNT > 0}}"
    branches:
      "true":
        - type: suggest
          severity: "error"
          message: |
            ## ESLint检查发现错误 ❌
            
            ESLint在代码中发现了 {{ERROR_COUNT}} 个错误和 {{WARNING_COUNT}} 个警告。
            
            请修复这些问题以确保代码质量。您可以运行以下命令自动修复部分问题：
            
            ```bash
            eslint {{file_path || 'src/'}} --fix
            ```
            
            ### 常见ESLint错误修复方法
            
            1. **未使用的变量**: 删除或使用它们
            2. **缺少分号**: 确保语句末尾有分号
            3. **引号使用不一致**: 统一使用单引号或双引号
            4. **缩进不正确**: 使用一致的缩进风格
      
      "false":
        - type: branch
          property: "{{WARNING_COUNT > 0}}"
          branches:
            "true":
              - type: suggest
                severity: "warning"
                message: |
                  ## ESLint检查完成 ⚠️
                  
                  ESLint没有发现错误，但有 {{WARNING_COUNT}} 个警告。
                  
                  建议修复这些警告以提高代码质量。您可以运行以下命令自动修复部分问题：
                  
                  ```bash
                  eslint {{file_path || 'src/'}} --fix
                  ```
            
            "false":
              - type: suggest
                message: |
                  ## ESLint检查通过 ✅
                  
                  代码质量检查未发现任何问题。代码符合项目的编码标准。

metadata:
  priority: high
  version: 1.0.0
  tags: ["linting", "code-quality", "eslint"]
</rule>
```

在Windows PowerShell环境中，可以调整为：

```powershell
Write-Output "运行ESLint检查..."

# 检查ESLint是否已安装
if (-not (Get-Command eslint -ErrorAction SilentlyContinue)) {
    Write-Output "ESLint未安装，正在安装..."
    npm install eslint --save-dev
}

# 检查是否有ESLint配置文件
if (-not (Test-Path -Path ".eslintrc.js" -PathType Leaf) -and 
    -not (Test-Path -Path ".eslintrc.json" -PathType Leaf) -and 
    -not (Test-Path -Path ".eslintrc.yml" -PathType Leaf)) {
    
    Write-Output "未检测到ESLint配置文件，创建默认配置..."
    
    @"
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: [
    'react',
    '@typescript-eslint',
  ],
  rules: {
    // 自定义规则
  },
};
"@ | Set-Content -Path ".eslintrc.js"
    
    # 安装必要的依赖
    npm install --save-dev eslint-plugin-react @typescript-eslint/eslint-plugin @typescript-eslint/parser
    
    Write-Output "已创建ESLint配置文件"
}

# 确定检查范围
$lintTarget = if ($filePath) { $filePath } else { "src\" }

# 运行ESLint
eslint $lintTarget --fix

# 获取ESLint结果
$lintOutput = eslint $lintTarget -f json | ConvertFrom-Json
$errorCount = ($lintOutput | ForEach-Object { $_.errorCount } | Measure-Object -Sum).Sum
$warningCount = ($lintOutput | ForEach-Object { $_.warningCount } | Measure-Object -Sum).Sum

Write-Output "ESLint检查完成: $errorCount 个错误, $warningCount 个警告"
```

### 与开发环境集成

将规则与开发环境工具集成可以提高开发效率。

#### 1. 与Node.js项目环境集成

规则可以帮助管理Node.js项目的依赖和脚本：

```rule
<rule>
name: node_project_helper
description: 管理Node.js项目依赖和脚本

filters:
  - type: command
    pattern: "npm-(install|update|script) ([\\w@\\/.-]+)(?: (\\w+))?"
    capture_as: [
      "action",
      "package",
      "script_name"
    ]

actions:
  - type: branch
    property: "{{captures.action}}"
    branches:
      "install":
        - type: execute
          command: |
            echo "安装软件包 {{captures.package}}..."
            
            # 检查是否要安装为开发依赖
            if [[ "{{captures.package}}" == *"-dev" ]]; then
              # 去除-dev后缀
              PACKAGE="${{captures.package}/-dev/}"
              npm install $PACKAGE --save-dev
              echo "已安装开发依赖: $PACKAGE"
            else
              npm install {{captures.package}}
              echo "已安装依赖: {{captures.package}}"
            fi
            
            # 更新package.json中的版本信息
            PACKAGE_NAME=$(echo "{{captures.package}}" | sed 's/@.*//')
            PACKAGE_VERSION=$(npm list $PACKAGE_NAME -json | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
            
            echo "已安装 $PACKAGE_NAME@$PACKAGE_VERSION"
        
        - type: suggest
          message: |
            ## 软件包安装完成 ✅
            
            已安装 `{{captures.package}}` 到项目中。
            
            {{captures.package.includes('-dev') ? '此包已作为开发依赖安装。' : '此包已作为生产依赖安装。'}}
            
            ### 使用方法
            
            ```javascript
            const {{packageNameToVariable(captures.package)}} = require('{{packageNameOnly(captures.package)}}');
            ```
      
      "update":
        - type: execute
          command: |
            echo "更新软件包..."
            
            if [ "{{captures.package}}" = "all" ]; then
              # 更新所有依赖
              npm update
              echo "已更新所有依赖"
            else
              # 更新特定依赖
              npm update {{captures.package}}
              echo "已更新依赖: {{captures.package}}"
            fi
            
            # 显示更新后的版本信息
            if [ "{{captures.package}}" != "all" ]; then
              PACKAGE_NAME=$(echo "{{captures.package}}" | sed 's/@.*//')
              PACKAGE_VERSION=$(npm list $PACKAGE_NAME -json | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
              echo "当前版本: $PACKAGE_NAME@$PACKAGE_VERSION"
            fi
        
        - type: suggest
          message: |
            ## 软件包更新完成 ✅
            
            {{captures.package === 'all' ? '已更新项目中的所有依赖。' : `已更新 \`${captures.package}\` 到最新版本。`}}
            
            建议测试应用以确保更新不会导致任何问题。
      
      "script":
        - type: branch
          property: "{{!captures.script_name}}"
          branches:
            "true":
              - type: execute
                command: |
                  echo "查看可用脚本..."
                  
                  # 提取package.json中的脚本
                  SCRIPTS=$(cat package.json | grep -A 100 '"scripts"' | grep -B 100 '},' | grep -v '"scripts"' | grep -v '},')
                  
                  echo "项目中的可用脚本:"
                  echo "$SCRIPTS"
              
              - type: suggest
                message: |
                  ## 项目脚本
                  
                  以下是项目中定义的脚本:
                  
                  ```json
                  {
                  {{SCRIPTS}}
                  }
                  ```
                  
                  您可以使用以下命令运行脚本:
                  
                  ```bash
                  npm run <script-name>
                  ```
            
            "false":
              - type: execute
                command: |
                  echo "运行脚本 {{captures.script_name}}..."
                  
                  # 检查脚本是否存在
                  if ! grep -q "\"{{captures.script_name}}\":" package.json; then
                    echo "ERROR: 脚本 '{{captures.script_name}}' 在package.json中不存在"
                    
                    # 获取可用脚本列表
                    AVAILABLE_SCRIPTS=$(cat package.json | grep -A 100 '"scripts"' | grep -B 100 '},' | grep -v '"scripts"' | grep -v '},' | grep -o '"[^"]*"' | grep -v ':' | tr -d '"')
                    
                    echo "可用脚本: $AVAILABLE_SCRIPTS"
                    exit 1
                  fi
                  
                  # 运行脚本
                  npm run {{captures.script_name}}
                  
                  echo "脚本 {{captures.script_name}} 已完成执行"
              
              - type: suggest
                message: |
                  ## 脚本执行完成 ✅
                  
                  已执行脚本 `{{captures.script_name}}`。
                  
                  如需查看所有可用脚本，可以运行:
                  
                  ```bash
                  npm-script list
                  ```

metadata:
  priority: medium
  version: 1.0.0
  tags: ["node", "npm", "dependencies", "scripts"]
</rule>
```

在Windows PowerShell环境中，脚本查看部分可以调整为：

```powershell
Write-Output "查看可用脚本..."

# 提取package.json中的脚本
$packageJson = Get-Content -Path "package.json" -Raw | ConvertFrom-Json
$scripts = $packageJson.scripts | ConvertTo-Json -Depth 1

Write-Output "项目中的可用脚本:"
Write-Output $scripts
```

## 组合规则创建完整工作流

通过组合不同的规则，我们可以创建完整的端到端工作流，覆盖从需求分析到部署和维护的整个开发过程。

### 工作流示例：Web应用开发流程

以下是一个完整的Web应用开发工作流示例，它组合了前面介绍的多个规则：

1. 使用 `user_story_template` 规则创建用户故事
2. 使用 `feature_development_workflow` 规则初始化特性开发环境
3. 使用 `feature_implementation_helper` 规则创建组件/服务
4. 使用 `eslint_integration` 规则确保代码质量
5. 使用 `test_coverage_checker` 规则验证测试覆盖率
6. 使用 `git_commit_formatter` 规则提交更改
7. 使用 `branch_and_merge_manager` 规则合并到主分支
8. 使用 `pre_deployment_checks` 规则验证部署准备情况

这个工作流程可以通过一个元规则来协调，该规则将根据开发阶段触发相应的子规则：

```rule
<rule>
name: web_app_workflow_coordinator
description: 协调Web应用开发的完整工作流程

filters:
  - type: command
    pattern: "workflow-(plan|dev|test|deploy|maintain) (.+)"
    capture_as: [
      "stage",
      "params"
    ]

actions:
  - type: branch
    property: "{{captures.stage}}"
    branches:
      "plan":
        - type: execute
          command: |
            echo "启动规划阶段..."
            cursor-cli run-command "new-story"
      
      "dev":
        - type: execute
          command: |
            echo "启动开发阶段..."
            cursor-cli run-command "start-feature {{captures.params}}"
      
      "test":
        - type: execute
          command: |
            echo "启动测试阶段..."
            cursor-cli run-command "check-coverage"
      
      "deploy":
        - type: execute
          command: |
            echo "启动部署阶段..."
            cursor-cli run-command "pre-deploy-check"
      
      "maintain":
        - type: execute
          command: |
            echo "启动维护阶段..."
            cursor-cli run-command "tech-debt"
  
  - type: suggest
    message: |
      ## 工作流阶段已启动
      
      已启动 `{{captures.stage}}` 阶段的工作流程。
      
      请按照向导完成此阶段的任务。完成后，可以继续下一阶段：
      
      {{
        captures.stage === 'plan' ? '`workflow-dev feature-name`' :
        captures.stage === 'dev' ? '`workflow-test`' :
        captures.stage === 'test' ? '`workflow-deploy`' :
        captures.stage === 'deploy' ? '`workflow-maintain`' :
        '`workflow-plan`'
      }}

metadata:
  priority: critical
  version: 1.0.0
  tags: ["workflow", "coordination", "development-lifecycle"]
</rule>
```

## 小结

本章探讨了如何将Cursor规则集成到开发工作流中，以及如何与其他工具协作创建完整的开发体验。通过将规则应用于开发流程的各个阶段，您可以自动化重复任务、确保代码质量和一致性，并提高团队协作效率。

关键要点包括：

1. **规则可以增强各个开发阶段**，从规划到部署和维护
2. **自动化工作流可以减少手动工作**，提高一致性和效率
3. **与其他工具的集成**使规则成为强大的开发工具链的一部分
4. **组合规则可以创建完整的端到端工作流**，覆盖整个开发生命周期

在下一章中，我们将探讨如何创建和管理规则库，以便更好地组织和共享您的规则。

## 实践练习

1. 创建一个集成您团队使用的CI/CD工具的规则
2. 设计一个自动化代码审查工作流
3. 实现一个与您项目的包管理器集成的规则
4. 构建一个完整的特性开发工作流，从需求到部署

## 参考资源

- [Git Workflow Best Practices](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [ESLint Documentation](https://eslint.org/docs/user-guide/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Node.js Package Management](https://docs.npmjs.com/cli/v7/commands)
- [Conventional Commits](https://www.conventionalcommits.org/) 
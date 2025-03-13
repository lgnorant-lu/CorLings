# 高级规则技术

## 概述

在掌握了基础规则的编写后，本章将引导您进入更高级的Cursor Rules领域。我们将探讨如何构建复杂规则、实现条件逻辑和分支，以及使用高级过滤器和动作来解决更复杂的自动化需求。通过本章的学习，您将能够创建更强大、更灵活的规则系统来优化您的工作流程。

## 学习目标

- 掌握复杂规则的构建方法和组织技巧
- 学习如何实现条件逻辑和分支结构
- 理解并应用高级过滤器和动作
- 解决实际开发中的复杂自动化场景

## 复杂规则构建

简单规则通常只关注单一问题，而复杂规则则需要处理多个相关联的问题或更复杂的逻辑。本节将介绍构建复杂规则的方法和技巧。

### 规则组合与链接

复杂规则的第一种构建方法是将多个简单规则组合或链接起来。

#### 1. 使用规则引用

您可以在一个规则中引用另一个规则，形成规则链：

```rule
<rule>
name: component_validation_chain
description: 组件验证规则链

filters:
  - type: file_extension
    pattern: "\\.tsx$"
  - type: file_path
    pattern: "src/components/"

actions:
  # 引用其他规则
  - type: reference
    rule: "component_structure_check"
    
  - type: reference
    rule: "component_naming_check"
    
  - type: reference
    rule: "component_accessibility_check"

metadata:
  priority: high
  version: 1.0.0
  tags: ["react", "component", "validation", "chain"]
</rule>
```

在Windows环境中实现这种链接时，确保引用的规则文件都位于正确的目录中，并且使用正确的路径格式。

#### 2. 使用元规则

元规则是控制其他规则行为的规则。它们可以启用、禁用或修改其他规则的行为：

```rule
<rule>
name: development_mode_rules
description: 在开发模式下修改规则行为

filters:
  - type: environment
    pattern: "NODE_ENV=development"

actions:
  # 在开发模式下禁用某些严格规则
  - type: modify_rule
    rule: "strict_type_checking"
    action: "disable"
    
  # 在开发模式下降低某些规则的优先级
  - type: modify_rule
    rule: "code_documentation"
    action: "set_priority"
    value: "low"

metadata:
  priority: critical
  version: 1.0.0
  tags: ["meta", "development", "environment"]
</rule>
```

### 上下文感知规则

上下文感知规则能够基于更广泛的上下文做出决策，而不仅仅是基于当前文件的内容。

#### 1. 项目结构感知

这类规则了解整个项目的结构，并基于此做出决策：

```rule
<rule>
name: component_import_validator
description: 验证组件导入路径是否符合项目结构

filters:
  - type: content
    pattern: "import\\s+\\{?\\s*[A-Z]\\w+\\s*\\}?\\s+from\\s+['\"]"
  - type: file_path
    pattern: "src/"

actions:
  - type: validate
    validation: |
      # 检查导入路径是否符合项目结构
      import_path = re.search(r"from\s+['\"](.+?)['\"]", "{{match}}").group(1)
      if import_path.startswith('.'):
        # 相对路径导入
        relative_file = os.path.normpath(os.path.join(os.path.dirname("{{file_path}}"), import_path))
        if not os.path.exists(relative_file):
          return False, f"导入路径 '{import_path}' 无效, 文件不存在"
      else:
        # 绝对路径导入
        if not import_path.startswith('@/'):
          return False, f"绝对路径导入应使用 '@/' 前缀"
      return True, "导入路径有效"

  - type: suggest
    when: "{{validation_result == false}}"
    message: "{{validation_message}}"

metadata:
  priority: medium
  version: 1.0.0
  tags: ["imports", "structure", "validation"]
</rule>
```

#### 2. 开发历史感知

这类规则能够考虑文件的修改历史：

```rule
<rule>
name: code_ownership
description: 识别代码所有者并在修改时提醒

filters:
  - type: file_modify
    pattern: ".*"

actions:
  - type: execute
    command: |
      # 使用git blame识别代码所有者
      OWNERS=$(git blame -L {{match_line_start}},{{match_line_end}} "{{file_path}}" | awk '{print $2}' | sort | uniq)
      CURRENT_USER=$(git config user.email)
      
      # 检查当前用户是否为所有者
      if echo "$OWNERS" | grep -q "$CURRENT_USER"; then
        echo "你是此代码段的所有者之一"
      else
        echo "警告: 你不是此代码段的所有者。考虑与以下人员讨论你的更改: $OWNERS"
      fi

metadata:
  priority: medium
  version: 1.0.0
  tags: ["git", "ownership", "collaboration"]
</rule>
```

在Windows环境中，需要使用PowerShell调整上述bash命令：

```powershell
$owners = git blame -L $matchLineStart,$matchLineEnd "$filePath" | ForEach-Object { $_.Split()[1] } | Sort-Object -Unique
$currentUser = git config user.email

if ($owners -contains $currentUser) {
    Write-Host "你是此代码段的所有者之一"
} else {
    Write-Host "警告: 你不是此代码段的所有者。考虑与以下人员讨论你的更改: $owners"
}
```

### 多阶段规则

多阶段规则将处理过程分为多个阶段，每个阶段有特定的任务：

```rule
<rule>
name: code_review_assistant
description: 多阶段代码审查助手

filters:
  - type: command
    pattern: "review"

actions:
  # 第1阶段: 收集信息
  - type: stage
    name: "collect_info"
    actions:
      - type: prompt
        questions:
          - id: "files"
            question: "要审查的文件路径:"
            placeholder: "src/components/Button.tsx"
          - id: "scope"
            question: "审查范围:"
            options: ["全面审查", "性能", "安全", "可访问性", "代码风格"]
            placeholder: "选择审查范围"

  # 第2阶段: 分析代码
  - type: stage
    name: "analyze"
    depends_on: "collect_info"
    actions:
      - type: execute
        command: |
          echo "正在分析文件: {{files}}"
          echo "审查范围: {{scope}}"
          
          # 执行相应的分析
          case "{{scope}}" in
            "性能")
              # 性能分析逻辑
              echo "执行性能分析..."
              ;;
            "安全")
              # 安全分析逻辑
              echo "执行安全分析..."
              ;;
            *)
              # 默认分析逻辑
              echo "执行标准代码分析..."
              ;;
          esac

  # 第3阶段: 生成报告
  - type: stage
    name: "report"
    depends_on: "analyze"
    actions:
      - type: suggest
        message: |
          ## 代码审查报告: {{files}}
          
          审查范围: {{scope}}
          
          ### 发现的问题
          
          1. 示例问题1
          2. 示例问题2
          
          ### 改进建议
          
          - 建议1
          - 建议2

metadata:
  priority: high
  version: 1.0.0
  tags: ["code-review", "multi-stage", "analysis"]
</rule>
```

### 自适应规则

自适应规则能够根据过去的交互历史和用户反馈调整自己的行为：

```rule
<rule>
name: adaptive_code_suggestions
description: 根据用户反馈调整代码建议

filters:
  - type: content
    pattern: "function\\s+\\w+\\s*\\([^)]*\\)"

actions:
  - type: suggest
    message: |
      建议你考虑以下改进:
      
      1. 添加函数参数类型注释
      2. 添加函数返回类型
      3. 添加函数描述文档
    
  - type: feedback
    prompt: "这个建议对你有帮助吗?"
    options: ["有帮助", "部分有帮助", "没有帮助"]
    
  - type: learn
    feedback_mapping:
      "有帮助": 
        action: "增强"
        weight: 1.2
      "部分有帮助": 
        action: "保持"
        weight: 1.0
      "没有帮助": 
        action: "减弱"
        weight: 0.8

metadata:
  priority: medium
  version: 1.0.0
  tags: ["adaptive", "suggestions", "feedback"]
  learning_rate: 0.1
</rule>
```

### 复杂规则的组织和管理

随着规则数量的增加，良好的组织和管理变得越来越重要。

#### 1. 使用命名空间

通过命名空间对规则进行分类：

```rule
<rule>
name: react:components:naming
description: React组件命名规范

# 规则内容...

metadata:
  namespace: "react.components"
  priority: medium
  version: 1.0.0
</rule>
```

#### 2. 规则依赖管理

明确规则之间的依赖关系：

```rule
<rule>
name: typescript_advanced_validation
description: TypeScript高级验证规则

# 规则内容...

metadata:
  priority: high
  version: 1.0.0
  dependencies: [
    "typescript_basic_validation:1.0.0",
    "project_structure:2.0.0+"
  ]
</rule>
```

#### 3. 版本控制和变更管理

使用版本控制管理规则的变更：

```rule
<rule>
name: code_formatting
description: 代码格式化规则

# 规则内容...

metadata:
  priority: medium
  version: "2.1.0"
  changelog: [
    { version: "1.0.0", changes: "初始版本" },
    { version: "2.0.0", changes: "添加缩进和空格规则" },
    { version: "2.1.0", changes: "修复正则表达式匹配问题" }
  ]
</rule>
```

#### 4. 文档和示例

为复杂规则提供完整的文档和示例：

```rule
<rule>
name: api_documentation
description: API文档生成规则

# 规则内容...

examples:
  - description: "基本函数文档"
    input: |
      function calculateTotal(price, quantity) {
        return price * quantity;
      }
    output: |
      /**
       * 计算总价
       * @param {number} price - 单价
       * @param {number} quantity - 数量
       * @returns {number} 总价金额
       */
      function calculateTotal(price, quantity) {
        return price * quantity;
      }
  
  - description: "带有错误处理的函数文档"
    input: |
      function divideValues(a, b) {
        if (b === 0) throw new Error("Cannot divide by zero");
        return a / b;
      }
    output: |
      /**
       * 除法计算
       * @param {number} a - 被除数
       * @param {number} b - 除数
       * @returns {number} 除法结果
       * @throws {Error} 当除数为零时抛出错误
       */
      function divideValues(a, b) {
        if (b === 0) throw new Error("Cannot divide by zero");
        return a / b;
      }

documentation: |
  # API文档生成规则
  
  这个规则会自动为JavaScript/TypeScript函数生成JSDoc文档注释。
  
  ## 使用方法
  
  1. 规则会自动检测未文档化的函数
  2. 分析函数签名、参数和返回语句
  3. 生成包含参数、返回值和可能异常的JSDoc注释
  
  ## 配置选项
  
  - `detail_level`: 文档详细程度 ("basic", "standard", "detailed")
  - `include_examples`: 是否包含示例代码 (true/false)

metadata:
  priority: high
  version: 1.0.0
  tags: ["documentation", "jsdoc", "api"]
</rule>
```

通过以上方法和技巧，您可以构建强大的复杂规则来解决更复杂的开发问题。在下一节中，我们将探讨如何在规则中实现条件逻辑和分支结构。

## 条件逻辑和分支结构

在复杂规则中，我们通常需要根据不同条件执行不同操作。本节将探讨如何在Cursor Rules中实现条件逻辑和分支结构。

### 条件过滤器

条件过滤器允许您基于条件表达式控制规则的触发。

#### 1. 基本条件过滤器

使用条件过滤器仅在满足特定条件时触发规则：

```rule
<rule>
name: conditional_linting_rule
description: 根据文件大小和复杂度有条件地应用代码风格规则

filters:
  - type: file_extension
    pattern: "\\.js$|\\.ts$"
  
  - type: conditional
    conditions:
      # 文件大小大于500行
      - check: "{{file_lines_count}} > 500"
        subfilters:
          - type: content
            pattern: "function\\s+\\w+\\s*\\(\\s*\\)"
        message: "大文件中的空参数函数需要文档化"

      # 文件包含复杂逻辑
      - check: "{{file_content.includes('switch') || file_content.includes('if') && file_content.includes('else if')}}"
        subfilters:
          - type: content
            pattern: "\\b(switch|if)\\b"
        message: "复杂逻辑需要清晰的注释"

actions:
  - type: suggest
    message: "{{condition_message}}"

metadata:
  priority: medium
  version: 1.0.0
  tags: ["conditional", "linting", "complexity"]
</rule>
```

#### 2. 多条件组合

使用AND、OR和NOT逻辑组合多个条件：

```rule
<rule>
name: complex_conditional_validation
description: 使用复杂条件组合验证代码

filters:
  - type: file_path
    pattern: "src/"
  
  - type: logical_and
    subfilters:
      - type: content
        pattern: "import.*React"
      - type: negation
        subfilters:
          - type: content
            pattern: "import.*PropTypes"

actions:
  - type: suggest
    message: "React组件导入了React但缺少PropTypes。考虑添加PropTypes来增强组件的类型安全性。"

metadata:
  priority: medium
  version: 1.0.0
  tags: ["react", "proptypes", "validation"]
</rule>
```

### 条件动作

条件动作允许基于条件执行不同的操作。

#### 1. 基本条件动作

根据条件执行不同的动作：

```rule
<rule>
name: conditional_code_fix
description: 根据代码上下文提供不同的修复方案

filters:
  - type: content
    pattern: "console\\.log\\([^)]*\\)"

actions:
  - type: conditional
    conditions:
      # 生产环境中的console.log
      - check: "{{file_path.includes('/prod/') || file_path.includes('/release/')}}"
        actions:
          - type: suggest
            severity: "warning"
            message: "生产代码中不应包含console.log语句。建议移除。"
          
          - type: edit
            description: "移除console.log语句"
            template: "// 已移除调试语句: {{match}}"
      
      # 开发环境中的console.log
      - check: "{{file_path.includes('/dev/') || file_path.includes('/debug/')}}"
        actions:
          - type: suggest
            severity: "info"
            message: "这是调试语句。请确保在提交前适当注释或移除。"
          
          - type: edit
            description: "注释console.log语句"
            template: "// DEBUG: {{match}}"
      
      # 默认情况
      - check: "true"
        actions:
          - type: suggest
            message: "考虑使用结构化日志记录代替console.log。"

metadata:
  priority: medium
  version: 1.0.0
  tags: ["debugging", "logging", "conditional"]
</rule>
```

#### 2. 嵌套条件动作

使用嵌套条件实现更复杂的决策树：

```rule
<rule>
name: nested_conditional_suggestions
description: 使用嵌套条件提供上下文相关的代码改进建议

filters:
  - type: file_extension
    pattern: "\\.jsx$|\\.tsx$"
  
  - type: content
    pattern: "<\\w+[^>]*>"

actions:
  - type: conditional
    conditions:
      # 检查是否为React组件
      - check: "{{match.match(/^<[A-Z]/)}}"
        actions:
          - type: conditional
            conditions:
              # 检查组件是否缺少键
              - check: "{{!match.includes('key=') && (file_content.includes('map(') || file_content.includes('forEach(') || file_content.includes('filter('))}}"
                actions:
                  - type: suggest
                    message: "列表渲染的组件应该有一个唯一的'key'属性。"
              
              # 检查组件是否可能需要可访问性属性
              - check: "{{match.includes('button') || match.includes('input') || match.includes('a ')}}"
                actions:
                  - type: suggest
                    message: "交互元素应包含适当的可访问性属性（如aria-*或role）。"
      
      # HTML元素
      - check: "{{match.match(/^<[a-z]/)}}"
        actions:
          - type: conditional
            conditions:
              # 检查图像是否缺少alt属性
              - check: "{{match.includes('<img') && !match.includes('alt=')}}"
                actions:
                  - type: suggest
                    message: "图像元素应包含alt属性以提高可访问性。"
                  - type: edit
                    description: "添加alt属性"
                    template: "{{match.replace('<img', '<img alt=\"描述这个图像\"')}}"

metadata:
  priority: high
  version: 1.0.0
  tags: ["react", "jsx", "accessibility", "nested-conditional"]
</rule>
```

### 基于上下文的分支

基于代码上下文的分支允许规则根据周围代码的情况做出不同的决策。

#### 1. 文件上下文分支

基于文件的类型、大小和内容等上下文信息进行分支：

```rule
<rule>
name: context_aware_styling
description: 根据文件上下文应用不同的代码样式规则

filters:
  - type: file_extension
    pattern: "\\.js$|\\.ts$|\\.css$|\\.scss$"

actions:
  - type: branch
    property: "{{file_extension}}"
    branches:
      ".js":
        - type: suggest
          message: "JavaScript文件应遵循驼峰命名法。"
      
      ".ts": 
        - type: suggest
          message: "TypeScript文件应使用类型注释和接口。"
      
      ".css":
        - type: suggest
          message: "CSS文件应使用class选择器而非ID选择器。"
      
      ".scss":
        - type: suggest
          message: "SCSS文件应使用嵌套和变量以提高可维护性。"
      
      "default":
        - type: suggest
          message: "请确保代码遵循项目的样式指南。"

metadata:
  priority: medium
  version: 1.0.0
  tags: ["styling", "context-aware", "branching"]
</rule>
```

#### 2. 项目上下文分支

基于项目配置、依赖和架构进行分支：

```rule
<rule>
name: project_aware_suggestions
description: 根据项目上下文提供建议

filters:
  - type: content
    pattern: "import\\s+.*from\\s+['\"]react['\"]"

actions:
  - type: execute
    command: |
      # 检查项目配置
      if [ -f "package.json" ]; then
        REACT_VERSION=$(grep -o '"react": "[^"]*"' package.json | grep -o '[0-9.]*')
        echo "REACT_VERSION=${REACT_VERSION}"
        
        # 检查是否有React测试库
        HAS_TESTING_LIBRARY=$(grep -c '@testing-library/react' package.json || echo "0")
        echo "HAS_TESTING_LIBRARY=${HAS_TESTING_LIBRARY}"
      fi
  
  - type: branch
    property: "{{REACT_VERSION}}"
    branches:
      "16.*":
        - type: suggest
          message: "您正在使用React 16。考虑使用函数组件和钩子代替类组件。"
      
      "17.*":
        - type: suggest
          message: "您正在使用React 17。新的JSX转换不再需要导入React。"
      
      "18.*":
        - type: suggest
          message: "您正在使用React 18。考虑利用并发特性和自动批处理。"
      
      "default":
        - type: suggest
          message: "确保使用适合您React版本的最佳实践。"
  
  - type: branch
    property: "{{HAS_TESTING_LIBRARY}}"
    branches:
      "0":
        - type: suggest
          message: "建议添加@testing-library/react以便更有效地测试React组件。"
      
      "default":
        - type: suggest
          message: "使用Testing Library测试组件行为而非实现细节。"

metadata:
  priority: high
  version: 1.0.0
  tags: ["react", "project-context", "version-aware"]
</rule>
```

在Windows环境中，可以使用PowerShell改写上述bash命令：

```powershell
# 检查项目配置
if (Test-Path "package.json") {
    $packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
    $reactVersion = $packageJson.dependencies.react -replace '^[\^~]'
    Write-Output "REACT_VERSION=$reactVersion"
    
    # 检查是否有React测试库
    $hasTestingLibrary = if ($packageJson.dependencies.'@testing-library/react' -or $packageJson.devDependencies.'@testing-library/react') { 1 } else { 0 }
    Write-Output "HAS_TESTING_LIBRARY=$hasTestingLibrary"
}
```

### 动态规则生成

动态规则生成允许根据上下文动态创建或修改规则。

#### 1. 项目配置驱动的规则

基于项目配置文件（如ESLint、Prettier等）动态生成规则：

```rule
<rule>
name: config_driven_rules
description: 根据项目配置动态生成规则

filters:
  - type: file_create
    pattern: ".*\\.js$|.*\\.ts$"

actions:
  - type: execute
    command: |
      # 检查项目配置文件
      CONFIG_FILES=()
      
      if [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ]; then
        CONFIG_FILES+=("eslint")
      fi
      
      if [ -f ".prettierrc" ] || [ -f ".prettierrc.js" ]; then
        CONFIG_FILES+=("prettier")
      fi
      
      if [ -f "tsconfig.json" ]; then
        CONFIG_FILES+=("typescript")
      fi
      
      # 输出找到的配置
      echo "CONFIG_FILES=${CONFIG_FILES[@]}"
  
  - type: generate_rule
    when: "{{CONFIG_FILES.includes('eslint')}}"
    rule: |
      <rule>
      name: eslint_integration
      description: 基于项目ESLint配置的规则
      
      filters:
        - type: file_modify
          pattern: ".*\\.js$|.*\\.ts$"
      
      actions:
        - type: execute
          command: "npx eslint --fix {{file_path}}"
        
        - type: suggest
          message: "文件已根据项目ESLint规则自动修复。"
      
      metadata:
        priority: high
        version: 1.0.0
        tags: ["eslint", "auto-fix", "generated"]
      </rule>
  
  - type: generate_rule
    when: "{{CONFIG_FILES.includes('prettier')}}"
    rule: |
      <rule>
      name: prettier_integration
      description: 基于项目Prettier配置的规则
      
      filters:
        - type: file_save
          pattern: ".*\\.(js|ts|jsx|tsx|css|scss|json|md)$"
      
      actions:
        - type: execute
          command: "npx prettier --write {{file_path}}"
        
        - type: echo
          message: "文件已使用Prettier格式化。"
      
      metadata:
        priority: medium
        version: 1.0.0
        tags: ["prettier", "formatting", "generated"]
      </rule>

metadata:
  priority: critical
  version: 1.0.0
  tags: ["meta", "config-driven", "dynamic"]
</rule>
```

在Windows中，使用PowerShell调整上述bash代码：

```powershell
# 检查项目配置文件
$configFiles = @()

if (Test-Path ".eslintrc.js" -PathType Leaf) -or (Test-Path ".eslintrc.json" -PathType Leaf) {
    $configFiles += "eslint"
}

if (Test-Path ".prettierrc" -PathType Leaf) -or (Test-Path ".prettierrc.js" -PathType Leaf) {
    $configFiles += "prettier"
}

if (Test-Path "tsconfig.json" -PathType Leaf) {
    $configFiles += "typescript"
}

# 输出找到的配置
Write-Output "CONFIG_FILES=$($configFiles -join ',')"
```

#### 2. 数据驱动的规则

基于数据或API响应动态生成规则：

```rule
<rule>
name: api_schema_validation
description: 根据API文档动态生成验证规则

filters:
  - type: command
    pattern: "generate-api-validators"

actions:
  - type: prompt
    questions:
      - id: "api_docs_url"
        question: "API文档URL(OpenAPI/Swagger):"
        placeholder: "https://api.example.com/swagger.json"
  
  - type: execute
    command: |
      # 获取API文档
      curl -s "{{api_docs_url}}" -o /tmp/api-docs.json
      
      # 解析API端点
      ENDPOINTS=$(jq -r '.paths | keys[]' /tmp/api-docs.json)
      echo "已找到以下API端点:"
      echo "$ENDPOINTS"
  
  - type: generate_rules
    script: |
      // 解析API文档并生成验证规则
      const apiDocs = require('/tmp/api-docs.json');
      const rules = [];
      
      // 为每个端点生成验证规则
      for (const [path, methods] of Object.entries(apiDocs.paths)) {
        for (const [method, details] of Object.entries(methods)) {
          if (details.requestBody) {
            // 创建请求体验证规则
            const schema = details.requestBody.content['application/json'].schema;
            rules.push({
              name: `validate_${method}_${path.replace(/\//g, '_')}`,
              description: `验证${method.toUpperCase()} ${path}请求`,
              filters: [
                { type: 'content', pattern: `fetch\\(['"].*${path}['"]` }
              ],
              actions: [
                { 
                  type: 'validate',
                  schema: JSON.stringify(schema),
                  message: `请求必须符合API规范: ${details.summary || path}`
                }
              ],
              metadata: {
                priority: 'medium',
                version: '1.0.0',
                tags: ['api', 'validation', 'generated']
              }
            });
          }
        }
      }
      
      return rules;

metadata:
  priority: high
  version: 1.0.0
  tags: ["api", "schema", "dynamic-rules"]
</rule>
```

在Windows中，需要调整JSON处理方式：

```powershell
# 获取API文档
Invoke-WebRequest -Uri "{{api_docs_url}}" -OutFile "$env:TEMP\api-docs.json"

# 解析API端点
$apiDocs = Get-Content -Raw "$env:TEMP\api-docs.json" | ConvertFrom-Json
$endpoints = $apiDocs.paths.PSObject.Properties.Name
Write-Output "已找到以下API端点:"
Write-Output $endpoints
```

### 状态管理与决策树

在复杂的规则中，维护状态和实现决策树可以提高规则的智能性。

#### 1. 使用上下文变量

通过上下文变量在规则执行过程中存储和使用状态：

```rule
<rule>
name: stateful_code_review
description: 使用状态变量进行代码审查

filters:
  - type: command
    pattern: "review-code"

actions:
  - type: init_state
    variables:
      issues_count: 0
      warnings_count: 0
      suggestions_count: 0
      reviewed_files: []
  
  - type: prompt
    questions:
      - id: "target_file"
        question: "要审查的文件:"
        placeholder: "src/components/App.js"
  
  - type: execute
    command: |
      # 分析文件
      if [ -f "{{target_file}}" ]; then
        # 检查代码问题
        ISSUES=$(eslint "{{target_file}}" --format=json)
        ISSUES_COUNT=$(echo "$ISSUES" | jq '. | length')
        
        # 更新状态变量
        echo "ISSUES_COUNT=$ISSUES_COUNT"
        echo "REVIEWED_FILES={{target_file}}"
      else
        echo "文件不存在"
      fi
  
  - type: update_state
    updates:
      issues_count: "{{state.issues_count + ISSUES_COUNT}}"
      reviewed_files: "{{state.reviewed_files.concat([target_file])}}"
  
  - type: branch
    property: "{{state.issues_count}}"
    branches:
      "0":
        - type: suggest
          message: "恭喜！审查的文件没有发现问题。"
      
      "1-5":
        - type: suggest
          message: "文件中发现少量问题，请修复它们。"
      
      "default":
        - type: suggest
          message: "文件中发现大量问题({{state.issues_count}})，需要进行较大修改。"
  
  - type: suggest
    message: |
      ## 代码审查摘要
      
      已审查文件: {{state.reviewed_files.join(', ')}}
      问题总数: {{state.issues_count}}
      
      建议采取的行动:
      {{state.issues_count > 5 ? '- 需要重大重构' : state.issues_count > 0 ? '- 修复发现的问题' : '- 代码质量良好，继续保持'}}

metadata:
  priority: high
  version: 1.0.0
  tags: ["code-review", "stateful", "decision-tree"]
</rule>
```

在Windows中，使用PowerShell调整：

```powershell
# 分析文件
if (Test-Path "{{target_file}}" -PathType Leaf) {
    # 检查代码问题
    $issues = npx eslint "{{target_file}}" --format=json | ConvertFrom-Json
    $issuesCount = $issues.Length
    
    # 更新状态变量
    Write-Output "ISSUES_COUNT=$issuesCount"
    Write-Output "REVIEWED_FILES={{target_file}}"
} else {
    Write-Output "文件不存在"
}
```

#### 2. 实现决策树

使用嵌套条件和分支实现复杂的决策树：

```rule
<rule>
name: security_audit_decision_tree
description: 使用决策树进行安全审计

filters:
  - type: command
    pattern: "security-audit"

actions:
  - type: decision_tree
    root:
      question: "项目类型是什么?"
      options:
        - label: "Web应用"
          next:
            question: "使用了哪种框架?"
            options:
              - label: "React"
                next:
                  question: "使用了哪种状态管理?"
                  options:
                    - label: "Redux"
                      action:
                        type: "suggest"
                        message: "检查Redux存储中的敏感数据是否加密"
                    - label: "Context API"
                      action:
                        type: "suggest"
                        message: "确保Context不存储未加密的敏感数据"
              - label: "Angular"
                action:
                  type: "suggest"
                  message: "检查Angular服务中的数据处理和XSS防护"
        - label: "移动应用"
          next:
            question: "是否处理敏感数据?"
            options:
              - label: "是"
                action:
                  type: "suggest"
                  message: "确保实现适当的数据加密和安全存储"
              - label: "否"
                action:
                  type: "suggest"
                  message: "检查API通信安全"
        - label: "API服务"
          action:
            type: "suggest"
            message: "检查身份验证、授权和输入验证机制"

metadata:
  priority: critical
  version: 1.0.0
  tags: ["security", "audit", "decision-tree"]
</rule>
```

通过本节中介绍的条件逻辑和分支结构，您可以构建高度动态和上下文感知的规则，使它们能够处理各种复杂场景。在下一节中，我们将探讨高级过滤器和动作，进一步扩展规则的功能。

## 高级过滤器和动作

在前面的章节中，我们探讨了复杂规则的构建和条件逻辑实现。本节将深入研究高级过滤器和动作，它们能让您的规则更加精确和强大。

### 高级过滤器技术

过滤器决定规则何时触发，高级过滤器技术可以让您的规则更加精准地匹配特定场景。

#### 1. 上下文感知过滤器

这类过滤器不仅考虑匹配内容，还考虑周围的上下文：

```rule
<rule>
name: function_error_handling
description: 确保异步函数包含适当的错误处理

filters:
  # 匹配async函数定义
  - type: content
    pattern: "async\\s+function\\s+\\w+\\s*\\([^)]*\\)\\s*\\{"
  
  # 上下文检查：确保在函数体中检查是否有try-catch块
  - type: context
    lookbehind: 0
    lookahead: 100
    not_pattern: "try\\s*\\{.*?\\}\\s*catch\\s*\\([^)]*\\)\\s*\\{"

actions:
  - type: suggest
    message: "发现不包含错误处理的异步函数。考虑添加try-catch块处理潜在异常。"

metadata:
  priority: medium
  version: 1.0.0
  tags: ["error-handling", "async", "best-practices"]
</rule>
```

#### 2. 多模式匹配过滤器

同时匹配多个模式，且可以引用之前的匹配结果：

```rule
<rule>
name: api_usage_validator
description: 验证API调用使用方式是否正确

filters:
  # 第一个模式：API初始化
  - type: content
    pattern: "const\\s+(\\w+)\\s*=\\s*new\\s+Api\\([^)]*\\)"
    capture_as: "api_instance"
  
  # 第二个模式：API方法调用，引用第一个匹配捕获的实例名
  - type: content
    pattern: "{{captures.api_instance}}\\.call\\([^)]*\\)"
    capture_as: "api_call"
  
  # 第三个模式：缺少错误处理的API调用
  - type: content
    pattern: "{{captures.api_call}}(?!\\.catch)"

actions:
  - type: suggest
    message: "API调用缺少错误处理。建议添加.catch()或使用try-catch块处理潜在错误。"

metadata:
  priority: high
  version: 1.0.0
  tags: ["api", "error-handling", "pattern-chaining"]
</rule>
```

#### 3. 语义分析过滤器

基于代码语义而非简单文本模式进行匹配：

```rule
<rule>
name: semantic_code_analyzer
description: 使用语义分析检查代码问题

filters:
  - type: file_extension
    pattern: "\\.js$|\\.ts$"
  
  - type: semantic
    analysis: |
      // 使用AST分析找出未使用的变量
      const ast = parse(file_content, { sourceType: 'module' });
      const unusedVars = [];
      
      // 收集所有变量声明
      const declarations = {};
      traverse(ast, {
        VariableDeclarator(path) {
          if (path.node.id.type === 'Identifier') {
            declarations[path.node.id.name] = {
              declared: true,
              used: false,
              node: path.node
            };
          }
        }
      });
      
      // 检查变量使用情况
      traverse(ast, {
        Identifier(path) {
          if (path.parent.type !== 'VariableDeclarator' && 
              declarations[path.node.name]) {
            declarations[path.node.name].used = true;
          }
        }
      });
      
      // 找出未使用的变量
      for (const [name, info] of Object.entries(declarations)) {
        if (info.declared && !info.used) {
          unusedVars.push({
            name,
            line: info.node.loc.start.line
          });
        }
      }
      
      return unusedVars.length > 0;

actions:
  - type: execute
    script: |
      // 获取分析结果
      const unusedVars = semanticResult;
      
      // 生成建议消息
      let message = "## 发现未使用的变量\n\n";
      for (const variable of unusedVars) {
        message += `- 第${variable.line}行: \`${variable.name}\`\n`;
      }
      
      return message;
  
  - type: suggest
    message: "{{execute_result}}"

metadata:
  priority: medium
  version: 1.0.0
  tags: ["semantic", "unused-vars", "code-quality"]
</rule>
```

在Windows环境中，如果要运行上述JavaScript代码，可以使用Node.js：

```powershell
# 安装必要的依赖
npm install @babel/parser @babel/traverse

# 编写分析脚本
$analyzeScript = @"
const { parse } = require('@babel/parser');
const { default: traverse } = require('@babel/traverse');
const fs = require('fs');

const fileContent = fs.readFileSync('$filePath', 'utf-8');
// 此处放置上述分析代码
"@

# 保存并执行脚本
$analyzeScript | Out-File -FilePath "analyze-temp.js" -Encoding utf8
node analyze-temp.js
```

#### 4. 历史感知过滤器

基于文件修改历史进行过滤：

```rule
<rule>
name: recurrent_bug_detector
description: 检测反复出现的bug模式

filters:
  - type: file_extension
    pattern: "\\.js$|\\.ts$"
  
  - type: content
    pattern: "function\\s+(\\w+)\\s*\\([^)]*\\)"
    capture_as: "function_name"
  
  - type: history
    command: |
      # 检查Git历史中这个函数是否有多次修复记录
      git log -p -- "{{file_path}}" | 
      grep -A 3 -B 3 "function\\s+{{captures.function_name}}\\s*(" | 
      grep -c "\\bfix\\b\\|\\bbug\\b\\|\\bissue\\b"
    min_count: 3

actions:
  - type: suggest
    severity: "warning"
    message: |
      函数 `{{captures.function_name}}` 在历史记录中有多次bug修复记录。
      建议进行彻底的代码审查和单元测试，以避免问题再次出现。

metadata:
  priority: high
  version: 1.0.0
  tags: ["bug-detection", "history-aware", "code-quality"]
</rule>
```

在Windows中，使用PowerShell改写上述Git历史检查：

```powershell
# 检查Git历史中这个函数是否有多次修复记录
$fixCount = (git log -p -- "$filePath" | 
            Select-String -Context 3,3 -Pattern "function\s+$functionName\s*\(" | 
            Select-String -Pattern "\bfix\b|\bbug\b|\bissue\b").Count

Write-Output "FIX_COUNT=$fixCount"
```

### 高级动作技术

动作定义规则触发后执行的操作，高级动作技术可以让您的规则执行更复杂和智能的任务。

#### 1. 代码转换动作

自动重构和修改代码：

```rule
<rule>
name: react_hooks_converter
description: 将React类组件转换为函数组件和Hooks

filters:
  - type: file_extension
    pattern: "\\.jsx$|\\.tsx$"
  
  - type: content
    pattern: "class\\s+(\\w+)\\s+extends\\s+React\\.Component"
    capture_as: "component_name"

actions:
  - type: transform
    transformation: |
      // 解析组件
      const ast = parse(file_content, {
        plugins: ['jsx', 'typescript'],
        sourceType: 'module'
      });
      
      // 类组件到函数组件的转换逻辑
      let state = {};
      let methods = {};
      let lifecycle = {};
      
      // 收集状态、方法和生命周期
      traverse(ast, {
        ClassProperty(path) {
          if (path.node.key.name === 'state' && path.node.value.type === 'ObjectExpression') {
            // 收集状态
            path.node.value.properties.forEach(prop => {
              state[prop.key.name] = {
                initialValue: generate(prop.value).code,
                usages: []
              };
            });
          }
        },
        ClassMethod(path) {
          const methodName = path.node.key.name;
          if (methodName === 'render') {
            // 处理render方法
          } else if (['componentDidMount', 'componentDidUpdate', 'componentWillUnmount'].includes(methodName)) {
            // 收集生命周期方法
            lifecycle[methodName] = generate(path.node.body).code;
          } else {
            // 收集普通方法
            methods[methodName] = generate(path.node.body).code;
          }
        }
      });
      
      // 生成Hooks代码
      let hooksCode = `import React, { useState, useEffect } from 'react';\n\n`;
      hooksCode += `function {{captures.component_name}}(props) {\n`;
      
      // 添加状态Hooks
      Object.entries(state).forEach(([name, info]) => {
        hooksCode += `  const [${name}, set${name.charAt(0).toUpperCase() + name.slice(1)}] = useState(${info.initialValue});\n`;
      });
      
      // 添加效果Hooks
      if (lifecycle.componentDidMount || lifecycle.componentWillUnmount) {
        hooksCode += `\n  useEffect(() => {\n`;
        if (lifecycle.componentDidMount) {
          hooksCode += `    // componentDidMount\n    ${lifecycle.componentDidMount.replace(/^\{|\}$/g, '').trim()}\n\n`;
        }
        if (lifecycle.componentWillUnmount) {
          hooksCode += `    return () => {\n      // componentWillUnmount\n      ${lifecycle.componentWillUnmount.replace(/^\{|\}$/g, '').trim()}\n    };\n`;
        }
        hooksCode += `  }, []);\n`;
      }
      
      // 添加方法转换为函数
      Object.entries(methods).forEach(([name, body]) => {
        hooksCode += `\n  const ${name} = ${body.replace(/this\./g, '')};\n`;
      });
      
      // 添加render返回
      // 提取类组件render方法的返回值
      let renderBody = "";
      traverse(ast, {
        ClassMethod(path) {
          if (path.node.key.name === 'render') {
            renderBody = generate(path.node.body).code;
          }
        }
      });
      
      hooksCode += `\n  return ${renderBody.replace(/^\{|\}$/g, '').replace(/this\.props/g, 'props').replace(/this\.state\./g, '').trim()};\n}\n\nexport default {{captures.component_name}};`;
      
      return hooksCode;
  
  - type: suggest
    message: |
      发现React类组件 `{{captures.component_name}}`。建议将其转换为函数组件和Hooks。
      
      ```jsx
      {{transform_result}}
      ```

metadata:
  priority: medium
  version: 1.0.0
  tags: ["react", "hooks", "refactoring"]
</rule>
```

在Windows环境中使用此规则时，确保已安装必要的Node.js包：

```powershell
# 安装必要的依赖
npm install @babel/parser @babel/traverse @babel/generator
```

#### 2. 项目层级动作

执行影响整个项目的动作：

```rule
<rule>
name: dependency_analyzer
description: 分析项目依赖关系并提供优化建议

filters:
  - type: file_path
    pattern: "package\\.json$"
  
  - type: event
    pattern: "file_modify"

actions:
  - type: project_analysis
    analysis: |
      const fs = require('fs');
      const path = require('path');
      
      // 读取package.json
      const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf-8'));
      const dependencies = { ...packageJson.dependencies, ...packageJson.devDependencies };
      
      // 分析结果
      const results = {
        outdated: [],
        unused: [],
        vulnerable: [],
        duplicate: []
      };
      
      // 检查过时的依赖
      const execSync = require('child_process').execSync;
      try {
        const outdatedOutput = execSync('npm outdated --json', { encoding: 'utf-8' });
        const outdatedDeps = JSON.parse(outdatedOutput);
        for (const [name, info] of Object.entries(outdatedDeps)) {
          results.outdated.push({
            name,
            current: info.current,
            latest: info.latest
          });
        }
      } catch (e) {
        // npm outdated 返回非零退出码时会抛出异常，但JSON输出仍然有效
        if (e.stdout) {
          try {
            const outdatedDeps = JSON.parse(e.stdout);
            for (const [name, info] of Object.entries(outdatedDeps)) {
              results.outdated.push({
                name,
                current: info.current,
                latest: info.latest
              });
            }
          } catch (parseErr) {
            console.error('无法解析npm outdated输出', parseErr);
          }
        }
      }
      
      // 检查未使用的依赖
      // 这需要深度分析项目文件
      
      return results;
  
  - type: suggest
    message: |
      ## 依赖分析报告
      
      ### 过时的依赖
      
      {{project_analysis.outdated.length > 0 ? project_analysis.outdated.map(dep => `- ${dep.name}: ${dep.current} → ${dep.latest}`).join('\n') : '没有过时的依赖'}}
      
      ### 建议
      
      {{project_analysis.outdated.length > 0 ? '运行 `npm update` 更新依赖' : '您的依赖已是最新版本'}}

metadata:
  priority: medium
  version: 1.0.0
  tags: ["dependencies", "project-analysis", "maintenance"]
</rule>
```

在Windows PowerShell中调整依赖分析代码：

```powershell
# 分析过时的依赖
try {
    $outdatedOutput = npm outdated --json 2>$null
    if ($outdatedOutput) {
        $outdatedDeps = $outdatedOutput | ConvertFrom-Json -AsHashtable
        foreach ($dep in $outdatedDeps.GetEnumerator()) {
            $name = $dep.Key
            $current = $dep.Value.current
            $latest = $dep.Value.latest
            Write-Output "OUTDATED:$name:$current:$latest"
        }
    }
} catch {
    Write-Output "无法分析过时的依赖: $_"
}
```

#### 3. AI辅助动作

使用AI增强的动作提供智能建议和修复：

```rule
<rule>
name: ai_code_reviewer
description: 使用AI进行代码审查和改进建议

filters:
  - type: file_modify
    pattern: ".*\\.(js|ts|jsx|tsx)$"
  
  - type: content_change
    min_lines: 10

actions:
  - type: ai_review
    prompt: |
      作为代码审查专家，请分析以下代码的问题和改进机会：
      
      ```{{file_extension}}
      {{changed_content}}
      ```
      
      关注以下方面：
      1. 代码可读性
      2. 性能优化
      3. 安全问题
      4. 最佳实践
      5. 可维护性
      
      请提供具体的改进建议和示例代码。
  
  - type: suggest
    message: |
      ## AI代码审查
      
      {{ai_review_result}}
      
      *此审查由AI辅助完成，请根据项目具体情况酌情采纳建议。*

metadata:
  priority: medium
  version: 1.0.0
  tags: ["ai", "code-review", "best-practices"]
</rule>
```

#### 4. 集成外部工具的动作

与外部工具集成的高级动作：

```rule
<rule>
name: security_scanner_integration
description: 集成安全扫描工具检测代码漏洞

filters:
  - type: file_extension
    pattern: "\\.js$|\\.ts$"
  
  - type: content
    pattern: "(?:api|fetch|axios)\\.(?:get|post|put|delete)\\s*\\("

actions:
  - type: execute
    command: |
      # 使用npm audit检查依赖安全问题
      npm audit --json > security-audit.json
      
      # 使用ESLint安全插件检查代码
      npx eslint --plugin security --rule 'security/detect-possible-timing-attacks: error' "{{file_path}}" -f json > security-eslint.json
  
  - type: parse
    files:
      - path: "security-audit.json"
        parser: "json"
        store_as: "dependency_audit"
      - path: "security-eslint.json"
        parser: "json"
        store_as: "code_audit"
  
  - type: suggest
    message: |
      ## 安全扫描报告
      
      ### 依赖安全问题
      
      {{dependency_audit.vulnerabilities ? `发现 ${Object.keys(dependency_audit.vulnerabilities).length} 个依赖安全问题` : '未发现依赖安全问题'}}
      
      {{dependency_audit.vulnerabilities && Object.keys(dependency_audit.vulnerabilities).length > 0 ? '#### 严重问题\n\n' + Object.entries(dependency_audit.vulnerabilities).filter(([_, vuln]) => vuln.severity === 'high' || vuln.severity === 'critical').map(([pkg, vuln]) => `- ${pkg}: ${vuln.severity} - ${vuln.title}`).join('\n') : ''}}
      
      ### 代码安全问题
      
      {{code_audit.length > 0 ? `发现 ${code_audit.length} 个代码安全问题` : '未发现代码安全问题'}}
      
      {{code_audit.length > 0 ? code_audit.map(issue => `- 第${issue.line}行: ${issue.message}`).join('\n') : ''}}
      
      ### 建议
      
      {{dependency_audit.vulnerabilities ? '运行 `npm audit fix` 修复可自动修复的依赖问题' : ''}}
      {{code_audit.length > 0 ? '查看并修复代码中的安全问题' : ''}}

  - type: cleanup
    files:
      - "security-audit.json"
      - "security-eslint.json"

metadata:
  priority: critical
  version: 1.0.0
  tags: ["security", "vulnerability", "scanning"]
</rule>
```

在Windows PowerShell中调整安全扫描命令：

```powershell
# 使用npm audit检查依赖安全问题
npm audit --json | Out-File -FilePath "security-audit.json" -Encoding utf8

# 使用ESLint安全插件检查代码
npx eslint --plugin security --rule "security/detect-possible-timing-attacks: error" "$filePath" -f json | Out-File -FilePath "security-eslint.json" -Encoding utf8
```

### 组合高级过滤器和动作

#### 1. 文档生成器规则

结合多种高级过滤器和动作自动生成项目文档：

```rule
<rule>
name: auto_documentation_generator
description: 自动为项目生成文档

filters:
  - type: command
    pattern: "generate-docs"

actions:
  - type: project_scan
    scan: |
      const fs = require('fs');
      const path = require('path');
      
      function scanDirectory(dir, fileTypes) {
        const results = [];
        const files = fs.readdirSync(dir);
        
        for (const file of files) {
          const filePath = path.join(dir, file);
          const stat = fs.statSync(filePath);
          
          if (stat.isDirectory()) {
            results.push(...scanDirectory(filePath, fileTypes));
          } else if (fileTypes.some(type => file.endsWith(type))) {
            results.push(filePath);
          }
        }
        
        return results;
      }
      
      // 扫描项目文件
      const sourceFiles = scanDirectory('./src', ['.js', '.jsx', '.ts', '.tsx']);
      const docFiles = scanDirectory('./docs', ['.md']);
      
      return {
        sourceFiles,
        docFiles,
        hasReadme: fs.existsSync('./README.md')
      };
  
  - type: execute
    command: |
      # 创建文档目录（如果不存在）
      mkdir -p docs
      
      # 生成项目总览文档
      echo "# 项目文档" > docs/index.md
      echo "" >> docs/index.md
      echo "## 项目概述" >> docs/index.md
      echo "" >> docs/index.md
      echo "本文档自动生成于 $(date)" >> docs/index.md
      echo "" >> docs/index.md
      
      # 从README提取信息（如果存在）
      if [ -f README.md ]; then
        echo "## 项目说明" >> docs/index.md
        echo "" >> docs/index.md
        sed -n '/^# /,/^#/p' README.md | grep -v "^# " >> docs/index.md
        echo "" >> docs/index.md
      fi
      
      # 生成文件结构文档
      echo "## 文件结构" >> docs/index.md
      echo "" >> docs/index.md
      echo "\`\`\`" >> docs/index.md
      find src -type f | sort >> docs/index.md
      echo "\`\`\`" >> docs/index.md
  
  - type: ai_generate
    for_each: "{{project_scan.sourceFiles}}"
    prompt: |
      作为文档专家，请为以下代码生成清晰的文档：
      
      ```
      {{fs.readFileSync(item, 'utf-8')}}
      ```
      
      文件路径: {{item}}
      
      请提供：
      1. 文件的主要功能概述
      2. 导出的组件/函数/类的详细说明
      3. 参数和返回值的描述
      4. 使用示例
    output_file: "docs/{{item.replace(/^src\//, '').replace(/\.[^.]+$/, '.md')}}"
  
  - type: generate
    template: |
      # API参考
      
      {{project_scan.sourceFiles.map(file => {
        const relativePath = file.replace(/^src\//, '');
        const docPath = `docs/${relativePath.replace(/\.[^.]+$/, '.md')}`;
        return `- [${relativePath}](${docPath.replace(/\\/g, '/')})`;
      }).join('\n')}}
    output_file: "docs/api-reference.md"
  
  - type: suggest
    message: |
      ## 文档生成完成
      
      已生成以下文档：
      
      - [项目概览](docs/index.md)
      - [API参考](docs/api-reference.md)
      {{project_scan.sourceFiles.map(file => {
        const relativePath = file.replace(/^src\//, '');
        const docPath = `docs/${relativePath.replace(/\.[^.]+$/, '.md')}`;
        return `- [${relativePath}](${docPath})`;
      }).join('\n')}}
      
      您可以通过编辑这些文档文件来完善项目文档。

metadata:
  priority: medium
  version: 1.0.0
  tags: ["documentation", "automation", "project-management"]
</rule>
```

在Windows PowerShell中调整上述脚本：

```powershell
# 创建文档目录（如果不存在）
if (-not (Test-Path -Path "docs" -PathType Container)) {
    New-Item -Path "docs" -ItemType Directory
}

# 生成项目总览文档
Set-Content -Path "docs\index.md" -Value "# 项目文档"
Add-Content -Path "docs\index.md" -Value ""
Add-Content -Path "docs\index.md" -Value "## 项目概述"
Add-Content -Path "docs\index.md" -Value ""
Add-Content -Path "docs\index.md" -Value "本文档自动生成于 $(Get-Date)"
Add-Content -Path "docs\index.md" -Value ""

# 从README提取信息（如果存在）
if (Test-Path -Path "README.md" -PathType Leaf) {
    Add-Content -Path "docs\index.md" -Value "## 项目说明"
    Add-Content -Path "docs\index.md" -Value ""
    
    $readmeContent = Get-Content -Path "README.md" -Raw
    $projectDescription = if ($readmeContent -match '(?s)^# .*?(?=^#|\z)') {
        $matches[0] -replace '^# .*\r?\n', ''
    } else { "" }
    
    Add-Content -Path "docs\index.md" -Value $projectDescription
    Add-Content -Path "docs\index.md" -Value ""
}

# 生成文件结构文档
Add-Content -Path "docs\index.md" -Value "## 文件结构"
Add-Content -Path "docs\index.md" -Value ""
Add-Content -Path "docs\index.md" -Value "```"
Get-ChildItem -Path "src" -Recurse -File | ForEach-Object { $_.FullName.Replace("$pwd\", "") } | Sort-Object | Add-Content -Path "docs\index.md"
Add-Content -Path "docs\index.md" -Value "```"
```

#### 2. 工作流自动化规则

结合多种高级过滤器和动作自动化开发工作流：

```rule
<rule>
name: feature_branch_workflow
description: 自动化特性分支开发工作流

filters:
  - type: command
    pattern: "feature (start|finish) (\\w+[-\\w]*)"
    capture_as: [
      "action",
      "feature_name"
    ]

actions:
  - type: branch
    property: "{{captures.action}}"
    branches:
      "start":
        - type: execute
          command: |
            # 确保工作区干净
            if [ -n "$(git status --porcelain)" ]; then
              echo "ERROR: 工作区不干净，请先提交或暂存您的更改"
              exit 1
            fi
            
            # 更新主分支
            git checkout main
            git pull
            
            # 创建特性分支
            git checkout -b feature/{{captures.feature_name}}
            
            # 创建特性文档
            mkdir -p .features
            cat > .features/{{captures.feature_name}}.md << EOL
            # 特性: {{captures.feature_name}}
            
            ## 描述
            <!-- 添加特性描述 -->
            
            ## 任务
            - [ ] 任务1
            - [ ] 任务2
            
            ## 相关问题
            <!-- 添加相关问题链接 -->
            EOL
            
            echo "特性分支 'feature/{{captures.feature_name}}' 已创建并设置"
        
        - type: prompt
          questions:
            - id: "description"
              question: "特性描述:"
              multiline: true
        
        - type: execute
          command: |
            # 更新特性文档
            sed -i "s/<!-- 添加特性描述 -->/{{description.replace(/\//g, '\\/').replace(/&/g, '\\&')}}/" .features/{{captures.feature_name}}.md
            
            # 将文档添加到Git
            git add .features/{{captures.feature_name}}.md
            git commit -m "docs: 初始化特性 {{captures.feature_name}} 文档"
            
            echo "特性 '{{captures.feature_name}}' 已初始化"
      
      "finish":
        - type: execute
          command: |
            # 确保在特性分支上
            CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
            if [ "$CURRENT_BRANCH" != "feature/{{captures.feature_name}}" ]; then
              echo "ERROR: 您不在 'feature/{{captures.feature_name}}' 分支上"
              exit 1
            fi
            
            # 检查是否有未提交更改
            if [ -n "$(git status --porcelain)" ]; then
              echo "ERROR: 有未提交的更改，请先处理它们"
              exit 1
            fi
            
            # 更新特性文档状态
            if [ -f .features/{{captures.feature_name}}.md ]; then
              sed -i 's/- \[ \]/- \[x\]/g' .features/{{captures.feature_name}}.md
              git add .features/{{captures.feature_name}}.md
              git commit -m "docs: 更新特性 {{captures.feature_name}} 状态为完成"
            fi
            
            # 更新main分支
            git checkout main
            git pull
            
            # 合并特性分支
            git merge --no-ff feature/{{captures.feature_name}} -m "feat: 完成特性 {{captures.feature_name}}"
            
            # 删除特性分支
            git branch -d feature/{{captures.feature_name}}
            
            echo "特性 '{{captures.feature_name}}' 已完成并合并到main分支"
  
  - type: suggest
    message: |
      {{captures.action === 'start' ? 
      `## 特性 '${captures.feature_name}' 已开始
      
      已创建分支 'feature/${captures.feature_name}'，并设置初始文档。
      
      开始开发您的特性，完成后运行:
      \`\`\`
      feature finish ${captures.feature_name}
      \`\`\``
      : 
      `## 特性 '${captures.feature_name}' 已完成
      
      已将 'feature/${captures.feature_name}' 合并到main分支。
      
      特性文档已更新，分支已删除。`
      }}

metadata:
  priority: high
  version: 1.0.0
  tags: ["workflow", "git", "feature-branch"]
</rule>
```

在Windows PowerShell中调整工作流自动化脚本：

```powershell
# 特性开始
if ($action -eq "start") {
    # 确保工作区干净
    if ((git status --porcelain)) {
        Write-Error "工作区不干净，请先提交或暂存您的更改"
        exit 1
    }
    
    # 更新主分支
    git checkout main
    git pull
    
    # 创建特性分支
    git checkout -b "feature/$featureName"
    
    # 创建特性文档
    if (-not (Test-Path -Path ".features" -PathType Container)) {
        New-Item -Path ".features" -ItemType Directory
    }
    
    @"
# 特性: $featureName

## 描述
<!-- 添加特性描述 -->

## 任务
- [ ] 任务1
- [ ] 任务2

## 相关问题
<!-- 添加相关问题链接 -->
"@ | Set-Content -Path ".features\$featureName.md"
    
    Write-Output "特性分支 'feature/$featureName' 已创建并设置"
}
```

## 小结

本节介绍了高级过滤器和动作技术，它们能够让您的Cursor Rules更加强大和灵活。通过组合这些高级功能，您可以创建复杂的智能规则，自动化日常工作流程并提高代码质量。记住，高级规则的威力在于它们的组合和集成能力，可以将多个工具和技术融合在一起，形成一个协同工作的自动化系统。

在下一章中，我们将探讨如何将规则集成到实际工作流中，以及如何使用规则系统优化团队协作。

## 实践练习

1. 创建一个使用语义分析过滤器检测代码复杂度的规则
2. 构建一个结合AI辅助动作的代码审查规则
3. 设计一个上下文感知过滤器来检测潜在的安全漏洞
4. 实现一个集成多个外部工具的项目健康检查规则

## 参考资源

- [Cursor官方规则文档](https://cursor.sh/docs/rules)
- [AST Explorer](https://astexplorer.net/) - 用于理解代码语义分析
- [正则表达式测试工具](https://regex101.com/) - 用于测试和优化过滤器模式

# 工作流集成（第一部分）

## 概述

在前面的章节中，我们学习了如何创建从基础到高级的Cursor规则。本章将探讨如何将这些规则集成到日常开发工作流中，使它们成为团队协作和项目管理的重要工具。通过将规则与开发流程紧密结合，我们可以实现更高效的协作、更一致的代码质量和更自动化的开发过程。

## 学习目标

- 了解如何将Cursor规则集成到不同类型的开发流程中
- 学习创建自动化工作流的方法和最佳实践
- 掌握规则与其他开发工具的协作方式
- 构建完整的规则驱动开发流程

## 规则与开发流程集成

将Cursor规则集成到开发流程中是提高团队效率和代码质量的关键步骤。本节将介绍如何在不同的开发阶段和流程中应用规则。

### 开发阶段与规则集成

软件开发通常包括规划、编码、测试、部署和维护等阶段。每个阶段都可以通过特定的规则得到增强。

#### 1. 规划阶段集成

在规划阶段，规则可以帮助创建和管理用户故事、任务和项目结构：

```rule
<rule>
name: user_story_template
description: 为用户故事创建标准模板

filters:
  - type: command
    pattern: "new-story"

actions:
  - type: prompt
    questions:
      - id: "story_title"
        question: "用户故事标题:"
        placeholder: "作为[角色]，我想要[功能]，以便[价值]"
      
      - id: "story_points"
        question: "故事点数 (1-8):"
        placeholder: "3"
      
      - id: "priority"
        question: "优先级:"
        options: ["高", "中", "低"]
        placeholder: "选择优先级"
  
  - type: execute
    command: |
      # 创建用户故事文件
      mkdir -p .project/stories
      
      STORY_ID=$(date +%Y%m%d%H%M%S)
      
      cat > .project/stories/$STORY_ID.md << EOL
      # {{story_title}}
      
      - **ID**: $STORY_ID
      - **创建时间**: $(date "+%Y-%m-%d %H:%M:%S")
      - **故事点数**: {{story_points}}
      - **优先级**: {{priority}}
      
      ## 描述
      
      <!-- 详细描述用户故事 -->
      
      ## 验收标准
      
      - [ ] 标准1
      - [ ] 标准2
      - [ ] 标准3
      
      ## 技术说明
      
      <!-- 添加技术实现相关说明 -->
      
      ## 相关链接
      
      <!-- 添加相关资源链接 -->
      EOL
      
      echo "已创建用户故事: $STORY_ID"

  - type: suggest
    message: |
      ## 用户故事已创建
      
      ID: $STORY_ID
      标题: {{story_title}}
      
      用户故事文件已保存至 `.project/stories/$STORY_ID.md`
      
      请完善故事的描述、验收标准和技术说明。

metadata:
  priority: medium
  version: 1.0.0
  tags: ["planning", "user-story", "template"]
</rule>
```

在Windows环境中，使用PowerShell调整上述命令：

```powershell
# 创建用户故事文件
if (-not (Test-Path -Path ".project\stories" -PathType Container)) {
    New-Item -Path ".project\stories" -ItemType Directory -Force
}

$storyId = Get-Date -Format "yyyyMMddHHmmss"
$currentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

@"
# $storyTitle

- **ID**: $storyId
- **创建时间**: $currentDate
- **故事点数**: $storyPoints
- **优先级**: $priority

## 描述

<!-- 详细描述用户故事 -->

## 验收标准

- [ ] 标准1
- [ ] 标准2
- [ ] 标准3

## 技术说明

<!-- 添加技术实现相关说明 -->

## 相关链接

<!-- 添加相关资源链接 -->
"@ | Set-Content -Path ".project\stories\$storyId.md"

Write-Output "已创建用户故事: $storyId"
```

#### 2. 编码阶段集成

在编码阶段，规则可以帮助实施编码标准、自动化重复任务和提供实时反馈：

```rule
<rule>
name: feature_implementation_helper
description: 帮助在新功能开发时创建必要的文件和测试

filters:
  - type: command
    pattern: "implement-feature (\\w+)"
    capture_as: [
      "feature_name"
    ]

actions:
  - type: prompt
    questions:
      - id: "feature_type"
        question: "功能类型:"
        options: ["组件", "服务", "工具函数", "API端点"]
        placeholder: "选择功能类型"
      
      - id: "description"
        question: "功能描述:"
        multiline: true
  
  - type: branch
    property: "{{feature_type}}"
    branches:
      "组件":
        - type: execute
          command: |
            # 创建组件文件
            mkdir -p src/components/{{captures.feature_name}}
            
            # 创建组件主文件
            cat > src/components/{{captures.feature_name}}/{{captures.feature_name}}.tsx << EOL
            import React from 'react';
            import './{{captures.feature_name}}.css';
            
            interface {{captures.feature_name}}Props {
              // 定义组件属性
            }
            
            /**
             * {{captures.feature_name}} 组件
             * 
             * {{description}}
             */
            export const {{captures.feature_name}}: React.FC<{{captures.feature_name}}Props> = (props) => {
              return (
                <div className="{{captures.feature_name | kebabCase}}">
                  {/* 组件内容 */}
                </div>
              );
            };
            
            export default {{captures.feature_name}};
            EOL
            
            # 创建组件样式文件
            cat > src/components/{{captures.feature_name}}/{{captures.feature_name}}.css << EOL
            .{{captures.feature_name | kebabCase}} {
              /* 组件样式 */
            }
            EOL
            
            # 创建组件测试文件
            cat > src/components/{{captures.feature_name}}/{{captures.feature_name}}.test.tsx << EOL
            import React from 'react';
            import { render, screen } from '@testing-library/react';
            import { {{captures.feature_name}} } from './{{captures.feature_name}}';
            
            describe('{{captures.feature_name}} Component', () => {
              test('renders correctly', () => {
                render(<{{captures.feature_name}} />);
                // 添加断言
              });
            });
            EOL
            
            # 创建组件文档文件
            cat > src/components/{{captures.feature_name}}/README.md << EOL
            # {{captures.feature_name}} 组件
            
            {{description}}
            
            ## 用法
            
            \`\`\`jsx
            import { {{captures.feature_name}} } from './components/{{captures.feature_name}}';
            
            function App() {
              return <{{captures.feature_name}} />;
            }
            \`\`\`
            
            ## 属性
            
            | 属性名 | 类型 | 默认值 | 描述 |
            |--------|------|--------|------|
            |        |      |        |      |
            
            ## 示例
            
            <!-- 添加示例 -->
            EOL
        
        - type: suggest
          message: |
            ## 组件文件已创建
            
            已为 {{captures.feature_name}} 组件创建以下文件:
            
            - `src/components/{{captures.feature_name}}/{{captures.feature_name}}.tsx` - 组件实现
            - `src/components/{{captures.feature_name}}/{{captures.feature_name}}.css` - 组件样式
            - `src/components/{{captures.feature_name}}/{{captures.feature_name}}.test.tsx` - 组件测试
            - `src/components/{{captures.feature_name}}/README.md` - 组件文档
            
            请根据实际需求完善这些文件。
      
      "服务":
        # 服务实现类似组件的分支逻辑，创建服务相关文件

      "工具函数":
        # 工具函数实现

      "API端点":
        # API端点实现

metadata:
  priority: high
  version: 1.0.0
  tags: ["coding", "scaffolding", "automation"]
</rule>
```

在Windows PowerShell中，使用以下方式调整：

```powershell
# 创建组件文件
$componentDir = "src\components\$featureName"
if (-not (Test-Path -Path $componentDir -PathType Container)) {
    New-Item -Path $componentDir -ItemType Directory -Force
}

# 创建各类文件...（其他文件创建步骤类似）
```

#### 3. 测试阶段集成

在测试阶段，规则可以自动生成测试案例、运行测试并分析结果：

```rule
<rule>
name: test_coverage_checker
description: 检查测试覆盖率并提供改进建议

filters:
  - type: command
    pattern: "check-coverage"
  
  - type: content
    pattern: "function\\s+(\\w+)\\s*\\([^)]*\\)"
    capture_as: "function_name"

actions:
  - type: execute
    command: |
      # 运行测试并生成覆盖率报告
      npm test -- --coverage
      
      # 分析覆盖率数据
      COVERAGE_REPORT="coverage/lcov-report/index.html"
      
      if [ -f "$COVERAGE_REPORT" ]; then
        # 提取覆盖率数据
        LINES_COVERAGE=$(grep -A 1 "Lines" $COVERAGE_REPORT | tail -n 1 | grep -o "[0-9.]*%" | tr -d '%')
        STATEMENTS_COVERAGE=$(grep -A 1 "Statements" $COVERAGE_REPORT | tail -n 1 | grep -o "[0-9.]*%" | tr -d '%')
        FUNCTIONS_COVERAGE=$(grep -A 1 "Functions" $COVERAGE_REPORT | tail -n 1 | grep -o "[0-9.]*%" | tr -d '%')
        BRANCHES_COVERAGE=$(grep -A 1 "Branches" $COVERAGE_REPORT | tail -n 1 | grep -o "[0-9.]*%" | tr -d '%')
        
        echo "LINES_COVERAGE=$LINES_COVERAGE"
        echo "STATEMENTS_COVERAGE=$STATEMENTS_COVERAGE"
        echo "FUNCTIONS_COVERAGE=$FUNCTIONS_COVERAGE"
        echo "BRANCHES_COVERAGE=$BRANCHES_COVERAGE"
      else
        echo "ERROR: 找不到覆盖率报告"
      fi
      
      # 检查缺少测试的函数
      UNCOVERED_FUNCTIONS=$(grep -r "function" src --include="*.js" --include="*.ts" | grep -v "test" | grep -o "function\s\+\w\+" | sed 's/function\s\+//' | sort)
      TESTED_FUNCTIONS=$(grep -r "test(" test --include="*.js" --include="*.ts" | grep -o "'\w\+'" | tr -d "'" | sort)
      
      MISSING_TESTS=$(comm -23 <(echo "$UNCOVERED_FUNCTIONS") <(echo "$TESTED_FUNCTIONS"))
      echo "MISSING_TESTS<<EOF"
      echo "$MISSING_TESTS"
      echo "EOF"
  
  - type: branch
    property: "{{LINES_COVERAGE < 80}}"
    branches:
      "true":
        - type: suggest
          severity: "warning"
          message: |
            ## 测试覆盖率低于目标值
            
            当前测试覆盖率:
            - 行覆盖率: {{LINES_COVERAGE}}% (目标: 80%)
            - 语句覆盖率: {{STATEMENTS_COVERAGE}}%
            - 函数覆盖率: {{FUNCTIONS_COVERAGE}}%
            - 分支覆盖率: {{BRANCHES_COVERAGE}}%
            
            ### 缺少测试的函数:
            
            {{MISSING_TESTS.split('\n').map(fn => `- \`${fn}\``).join('\n')}}
            
            ### 建议
            
            1. 为上述缺少测试的函数添加单元测试
            2. 增加边界条件的测试用例
            3. 考虑添加集成测试确保组件间交互正常
      
      "false":
        - type: suggest
          message: |
            ## 测试覆盖率良好
            
            当前测试覆盖率:
            - 行覆盖率: {{LINES_COVERAGE}}% ✅
            - 语句覆盖率: {{STATEMENTS_COVERAGE}}% ✅
            - 函数覆盖率: {{FUNCTIONS_COVERAGE}}% ✅
            - 分支覆盖率: {{BRANCHES_COVERAGE}}% ✅
            
            继续保持良好的测试实践！

metadata:
  priority: high
  version: 1.0.0
  tags: ["testing", "coverage", "quality"]
</rule>
```

在Windows PowerShell中，调整以下部分：

```powershell
# 运行测试并生成覆盖率报告
npm test -- --coverage

# 分析覆盖率数据
$coverageReport = "coverage\lcov-report\index.html"

if (Test-Path -Path $coverageReport -PathType Leaf) {
    # 从HTML报告中提取覆盖率数据
    $content = Get-Content -Path $coverageReport -Raw
    $linesCoverage = if ($content -match "Lines.*?([0-9.]+)%") { $matches[1] } else { "0" }
    $statementsCoverage = if ($content -match "Statements.*?([0-9.]+)%") { $matches[1] } else { "0" }
    $functionsCoverage = if ($content -match "Functions.*?([0-9.]+)%") { $matches[1] } else { "0" }
    $branchesCoverage = if ($content -match "Branches.*?([0-9.]+)%") { $matches[1] } else { "0" }
    
    Write-Output "LINES_COVERAGE=$linesCoverage"
    Write-Output "STATEMENTS_COVERAGE=$statementsCoverage"
    Write-Output "FUNCTIONS_COVERAGE=$functionsCoverage"
    Write-Output "BRANCHES_COVERAGE=$branchesCoverage"
} else {
    Write-Output "ERROR: 找不到覆盖率报告"
}
``` 
 # 工作流集成（第二部分）

## 规则与开发流程集成（续）

### 开发阶段与规则集成（续）

#### 4. 部署阶段集成

在部署阶段，规则可以帮助准备和验证部署内容，确保部署过程顺利：

```rule
<rule>
name: pre_deployment_checks
description: 部署前的准备检查和验证

filters:
  - type: command
    pattern: "deploy|pre-deploy-check"

actions:
  - type: execute
    command: |
      echo "开始执行部署前检查..."
      
      # 检查构建是否成功
      echo "检查构建状态..."
      npm run build
      if [ $? -ne 0 ]; then
        echo "ERROR: 构建失败，请修复错误后再尝试部署"
        exit 1
      fi
      
      # 检查测试是否通过
      echo "运行测试..."
      npm test
      if [ $? -ne 0 ]; then
        echo "WARNING: 测试未全部通过，请检查失败的测试"
      fi
      
      # 检查依赖是否有安全漏洞
      echo "检查依赖安全漏洞..."
      npm audit
      
      # 检查环境配置文件
      echo "检查环境配置..."
      ENV_FILES=(".env.production" ".env.staging")
      
      for ENV_FILE in "${ENV_FILES[@]}"; do
        if [ ! -f "$ENV_FILE" ]; then
          echo "WARNING: 缺少环境配置文件 $ENV_FILE"
        else
          # 检查关键配置项是否存在
          for KEY in "API_URL" "DATABASE_URL" "AUTH_SECRET"; do
            if ! grep -q "^$KEY=" "$ENV_FILE"; then
              echo "WARNING: $ENV_FILE 中缺少关键配置项 $KEY"
            fi
          done
        fi
      done
      
      # 检查静态资源是否已优化
      echo "检查静态资源..."
      IMAGES_UNOPTIMIZED=$(find public/images -type f \( -name "*.png" -o -name "*.jpg" \) -size +300k | wc -l)
      if [ $IMAGES_UNOPTIMIZED -gt 0 ]; then
        echo "WARNING: 发现 $IMAGES_UNOPTIMIZED 个大于300KB的图像文件，建议进行优化"
        find public/images -type f \( -name "*.png" -o -name "*.jpg" \) -size +300k -exec ls -lh {} \;
      fi
      
      echo "部署前检查完成"
  
  - type: branch
    conditions:
      - validation: "$? == 0"
        actions:
          - type: suggest
            message: |
              ## 部署前检查成功 ✅
              
              所有必要的检查都已通过，项目可以部署到生产环境。
              
              ### 下一步
              
              运行以下命令开始部署:
              
              ```bash
              npm run deploy
              ```
      
      - validation: "true"
        actions:
          - type: suggest
            severity: "warning"
            message: |
              ## 部署前检查完成，但有警告 ⚠️
              
              部署检查过程中发现了一些警告，建议在部署前解决这些问题。
              
              请查看上方的警告信息并进行相应修复。解决问题后，重新运行部署前检查。

metadata:
  priority: critical
  version: 1.0.0
  tags: ["deployment", "validation", "quality"]
</rule>
```

在Windows环境中，调整为：

```CMD
# Windows CMD
@echo off
echo 开始执行部署前检查...

rem 检查构建是否成功
echo 检查构建状态...
npm run build
if %errorlevel% neq 0 (
    echo ERROR: 构建失败，请修复错误后再尝试部署
    exit /b 1
)

rem 检查测试是否通过
echo 运行测试...
npm test
if %errorlevel% neq 0 (
    echo WARNING: 测试未全部通过，请检查失败的测试
)

# Linux/macOS
#!/bin/bash
echo "开始执行部署前检查..."

# 检查构建是否成功
echo "检查构建状态..."
npm run build
if [ $? -ne 0 ]; then
    echo "ERROR: 构建失败，请修复错误后再尝试部署"
    exit 1
fi

# 检查测试是否通过
echo "运行测试..."
npm test
if [ $? -ne 0 ]; then
    echo "WARNING: 测试未全部通过，请检查失败的测试"
fi
```

#### 5. 维护阶段集成

在维护阶段，规则可以帮助监控应用性能、分析问题和管理技术债务：

```rule
<rule>
name: tech_debt_manager
description: 技术债务管理和追踪

filters:
  - type: command
    pattern: "tech-debt|manage-debt"
  
  - type: content
    pattern: "// TODO:|// FIXME:|// HACK:|// DEBT:"
    capture_as: "tech_debt_marker"

actions:
  - type: execute
    command: |
      echo "正在分析技术债务..."
      
      # 创建技术债务目录
      DEBT_DIR=".techdebt"
      mkdir -p "$DEBT_DIR"
      
      # 查找所有技术债务标记
      echo "查找代码中的技术债务标记..."
      
      # 搜索各类技术债务标记
      grep -r "// TODO:" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . > "$DEBT_DIR/todos.txt"
      grep -r "// FIXME:" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . > "$DEBT_DIR/fixmes.txt"
      grep -r "// HACK:" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . > "$DEBT_DIR/hacks.txt"
      grep -r "// DEBT:" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . > "$DEBT_DIR/debts.txt"
      
      # 统计各类技术债务数量
      TODO_COUNT=$(wc -l < "$DEBT_DIR/todos.txt" || echo "0")
      FIXME_COUNT=$(wc -l < "$DEBT_DIR/fixmes.txt" || echo "0")
      HACK_COUNT=$(wc -l < "$DEBT_DIR/hacks.txt" || echo "0")
      DEBT_COUNT=$(wc -l < "$DEBT_DIR/debts.txt" || echo "0")
      
      TOTAL_COUNT=$((TODO_COUNT + FIXME_COUNT + HACK_COUNT + DEBT_COUNT))
      
      # 生成技术债务报告
      cat > "$DEBT_DIR/report.md" << EOL
      # 技术债务报告
      
      *生成于 $(date "+%Y-%m-%d %H:%M:%S")*
      
      ## 摘要
      
      | 类型 | 数量 |
      |------|------|
      | TODO | $TODO_COUNT |
      | FIXME | $FIXME_COUNT |
      | HACK | $HACK_COUNT |
      | DEBT | $DEBT_COUNT |
      | **总计** | **$TOTAL_COUNT** |
      
      ## 详细列表
      
      ### TODO 项
      
      \`\`\`
      $(cat "$DEBT_DIR/todos.txt")
      \`\`\`
      
      ### FIXME 项
      
      \`\`\`
      $(cat "$DEBT_DIR/fixmes.txt")
      \`\`\`
      
      ### HACK 项
      
      \`\`\`
      $(cat "$DEBT_DIR/hacks.txt")
      \`\`\`
      
      ### DEBT 项
      
      \`\`\`
      $(cat "$DEBT_DIR/debts.txt")
      \`\`\`
      EOL
      
      echo "技术债务分析完成，共发现 $TOTAL_COUNT 项债务"
  
  - type: suggest
    message: |
      ## 技术债务报告
      
      已分析项目中的技术债务并生成报告。
      
      ### 摘要
      
      - TODO 项: {{TODO_COUNT}}
      - FIXME 项: {{FIXME_COUNT}}
      - HACK 项: {{HACK_COUNT}}
      - DEBT 项: {{DEBT_COUNT}}
      - **总计**: {{TOTAL_COUNT}}
      
      ### 建议
      
      1. 查看完整报告: `.techdebt/report.md`
      2. 将高优先级的 FIXME 添加到下一个迭代
      3. 安排定期的"技术债务清理"迭代
      4. 更新团队的技术债务管理流程

  - type: branch
    property: "{{TOTAL_COUNT > 20}}"
    branches:
      "true":
        - type: suggest
          severity: "warning"
          message: |
            ## 技术债务水平警告 ⚠️
            
            项目中的技术债务项数量({{TOTAL_COUNT}})超过了推荐的阈值(20)。
            
            建议尽快安排技术债务清理工作，防止债务累积影响项目可维护性和开发效率。
      
      "false":
        - type: suggest
          message: |
            ## 技术债务水平可接受 ✅
            
            当前技术债务水平在可控范围内。继续定期监控和管理技术债务。

metadata:
  priority: high
  version: 1.0.0
  tags: ["maintenance", "tech-debt", "quality"]
</rule>
```

在Windows环境中，调整为：

```CMD
# Windows CMD
@echo off
echo 正在分析技术债务...

rem 创建技术债务目录
set debtDir=.techdebt
if not exist %debtDir% mkdir %debtDir%

rem 查找所有技术债务标记
echo 查找代码中的技术债务标记...

rem 搜索各类技术债务标记
findstr /S /M /C:"// TODO:" *.js *.ts *.jsx *.tsx > %debtDir%\todos.txt
findstr /S /M /C:"// FIXME:" *.js *.ts *.jsx *.tsx > %debtDir%\fixmes.txt
findstr /S /M /C:"// HACK:" *.js *.ts *.jsx *.tsx > %debtDir%\hacks.txt
findstr /S /M /C:"// DEBT:" *.js *.ts *.jsx *.tsx > %debtDir%\debts.txt

# Linux/macOS
#!/bin/bash
echo "正在分析技术债务..."

# 创建技术债务目录
debtDir=".techdebt"
mkdir -p $debtDir

# 查找所有技术债务标记
echo "查找代码中的技术债务标记..."

# 搜索各类技术债务标记
grep -r "// TODO:" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . > $debtDir/todos.txt
grep -r "// FIXME:" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . > $debtDir/fixmes.txt
grep -r "// HACK:" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . > $debtDir/hacks.txt
grep -r "// DEBT:" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . > $debtDir/debts.txt
```

## 自动化工作流创建

除了将规则集成到各个开发阶段，我们还可以创建完整的自动化工作流，将多个规则组合以实现更复杂的自动化流程。

### 端到端工作流设计

设计有效的端到端工作流需要考虑以下因素：

1. **明确工作流程目标**：明确自动化的具体目标和期望结果
2. **识别关键步骤**：分解工作流为可管理的步骤
3. **定义触发条件**：确定何时启动工作流
4. **处理依赖关系**：管理步骤间的依赖和数据流
5. **错误处理和恢复**：为潜在问题设计解决方案

以下是一个完整的特性开发自动化工作流示例：

```rule
<rule>
name: feature_development_workflow
description: 从规划到部署的完整特性开发工作流

filters:
  - type: command
    pattern: "start-feature (\\w+)(?: \"([^\"]+)\")?"
    capture_as: [
      "feature_name",
      "feature_description"
    ]

actions:
  - type: prompt
    questions:
      - id: "feature_description"
        question: "特性描述 (如未提供):"
        placeholder: "描述这个特性的功能和价值"
        skip_if: "{{captures.feature_description}}"
      
      - id: "feature_type"
        question: "特性类型:"
        options: ["UI组件", "API功能", "核心功能", "性能优化", "其他"]
      
      - id: "priority"
        question: "优先级:"
        options: ["高", "中", "低"]
  
  # 第1步：特性规划
  - type: title
    content: "1. 特性规划"
  
  - type: execute
    command: |
      echo "创建特性分支..."
      
      # 确保我们在最新的主分支上
      git checkout main
      git pull
      
      # 创建特性分支
      FEATURE_BRANCH="feature/{{captures.feature_name}}"
      git checkout -b $FEATURE_BRANCH
      
      # 创建特性规划文档
      mkdir -p docs/features
      
      # 生成特性规划文档
      cat > docs/features/{{captures.feature_name}}.md << EOL
      # {{captures.feature_name}}
      
      ## 概述
      
      {{feature_description}}
      
      ## 详细信息
      
      - **类型**: {{feature_type}}
      - **优先级**: {{priority}}
      - **创建日期**: $(date "+%Y-%m-%d")
      - **状态**: 规划中
      
      ## 功能要求
      
      - [ ] 要求1
      - [ ] 要求2
      - [ ] 要求3
      
      ## 技术设计
      
      <!-- 在此描述技术设计和架构决策 -->
      
      ## 测试计划
      
      <!-- 在此描述测试计划和验收标准 -->
      
      ## 相关资源
      
      <!-- 在此添加相关资源链接 -->
      EOL
      
      # 提交特性规划文档
      git add docs/features/{{captures.feature_name}}.md
      git commit -m "docs: 添加{{captures.feature_name}}特性规划文档"
      
      echo "特性规划文档已创建并提交"
  
  # 第2步：环境准备
  - type: title
    content: "2. 环境准备"
  
  - type: branch
    property: "{{feature_type}}"
    branches:
      "UI组件":
        - type: execute
          command: |
            echo "准备UI组件开发环境..."
            
            # 创建组件目录
            mkdir -p src/components/{{captures.feature_name}}
            
            # 创建基础组件文件
            cat > src/components/{{captures.feature_name}}/index.tsx << EOL
            import React from 'react';
            import './styles.css';
            
            interface {{pascalCase(captures.feature_name)}}Props {
              // 定义组件属性
            }
            
            export const {{pascalCase(captures.feature_name)}}: React.FC<{{pascalCase(captures.feature_name)}}Props> = (props) => {
              return (
                <div className="{{kebabCase(captures.feature_name)}}">
                  {/* 组件内容 */}
                </div>
              );
            };
            
            export default {{pascalCase(captures.feature_name)}};
            EOL
            
            # 创建样式文件
            cat > src/components/{{captures.feature_name}}/styles.css << EOL
            .{{kebabCase(captures.feature_name)}} {
              /* 组件样式 */
            }
            EOL
            
            # 创建测试文件
            cat > src/components/{{captures.feature_name}}/index.test.tsx << EOL
            import React from 'react';
            import { render } from '@testing-library/react';
            import { {{pascalCase(captures.feature_name)}} } from './index';
            
            describe('{{pascalCase(captures.feature_name)}} Component', () => {
              test('renders correctly', () => {
                render(<{{pascalCase(captures.feature_name)}} />);
                // 添加测试断言
              });
            });
            EOL
            
            # 提交环境准备文件
            git add src/components/{{captures.feature_name}}
            git commit -m "feat({{captures.feature_name}}): 初始化UI组件结构"
            
            echo "UI组件环境准备完成"
      
      "API功能":
        - type: execute
          command: |
            echo "准备API功能开发环境..."
            
            # 创建API相关文件
            mkdir -p src/api/{{captures.feature_name}}
            
            # 创建API接口文件
            cat > src/api/{{captures.feature_name}}/index.ts << EOL
            import axios from 'axios';
            
            const API_URL = process.env.API_URL || '';
            
            export interface {{pascalCase(captures.feature_name)}}Request {
              // 请求参数类型定义
            }
            
            export interface {{pascalCase(captures.feature_name)}}Response {
              // 响应类型定义
            }
            
            /**
             * {{pascalCase(captures.feature_name)}} API
             * {{feature_description}}
             */
            export const {{camelCase(captures.feature_name)}} = async (params: {{pascalCase(captures.feature_name)}}Request): Promise<{{pascalCase(captures.feature_name)}}Response> => {
              try {
                const response = await axios.post(\`\${API_URL}/api/{{kebabCase(captures.feature_name)}}\`, params);
                return response.data;
              } catch (error) {
                console.error('API Error:', error);
                throw error;
              }
            };
            EOL
            
            # 创建API测试文件
            cat > src/api/{{captures.feature_name}}/index.test.ts << EOL
            import axios from 'axios';
            import { {{camelCase(captures.feature_name)}} } from './index';
            
            # Mock axios
            jest.mock('axios');
            const mockedAxios = axios as jest.Mocked<typeof axios>;
            
            describe('{{pascalCase(captures.feature_name)}} API', () => {
              beforeEach(() => {
                jest.clearAllMocks();
              });
              
              test('calls the correct endpoint with params', async () => {
                # 设置模拟响应
                mockedAxios.post.mockResolvedValueOnce({ data: {} });
                
                # 调用API
                await {{camelCase(captures.feature_name)}}({});
                
                # 验证调用
                expect(mockedAxios.post).toHaveBeenCalledWith(
                  expect.stringContaining('/api/{{kebabCase(captures.feature_name)}}'),
                  expect.any(Object)
                );
              });
            });
            EOL
            
            # 提交环境准备文件
            git add src/api/{{captures.feature_name}}
            git commit -m "feat({{captures.feature_name}}): 初始化API功能结构"
            
            echo "API功能环境准备完成"
  
  # 第3步：测试设置
  - type: title
    content: "3. 测试设置"
  
  - type: execute
    command: |
      echo "设置特性测试..."
      
      # 确保测试目录存在
      mkdir -p tests/features/{{captures.feature_name}}
      
      # 创建特性测试计划
      cat > tests/features/{{captures.feature_name}}/test-plan.md << EOL
      # {{captures.feature_name}} 测试计划
      
      ## 单元测试
      
      - [ ] 测试核心功能
      - [ ] 测试边界条件
      - [ ] 测试错误处理
      
      ## 集成测试
      
      - [ ] 测试与其他组件的集成
      - [ ] 测试与API的集成
      
      ## 端到端测试
      
      - [ ] 测试完整用户流程
      - [ ] 测试性能和负载
      
      ## 验收标准
      
      - [ ] 标准1
      - [ ] 标准2
      - [ ] 标准3
      EOL
      
      # 提交测试计划
      git add tests/features/{{captures.feature_name}}
      git commit -m "test({{captures.feature_name}}): 添加测试计划"
      
      echo "测试设置完成"
  
  # 第4步：持续集成配置
  - type: title
    content: "4. 持续集成配置"
  
  - type: execute
    command: |
      echo "配置持续集成..."
      
      # 创建或更新CI配置
      if [ -f ".github/workflows/ci.yml" ]; then
        echo "使用现有CI配置"
      else
        mkdir -p .github/workflows
        cat > .github/workflows/ci.yml << EOL
      name: CI
      
      on:
        push:
          branches: [ main, feature/** ]
        pull_request:
          branches: [ main ]
      
      jobs:
        build:
          runs-on: ubuntu-latest
          
          steps:
          - uses: actions/checkout@v2
          
          - name: Setup Node.js
            uses: actions/setup-node@v2
            with:
              node-version: '16'
              
          - name: Install dependencies
            run: npm ci
              
          - name: Run tests
            run: npm test
              
          - name: Build
            run: npm run build
      EOL
        
        git add .github/workflows/ci.yml
        git commit -m "ci: 添加基本CI工作流配置"
      fi
      
      echo "持续集成配置完成"
  
  # 第5步：推送分支并创建PR
  - type: title
    content: "5. 推送分支并创建PR模板"
  
  - type: execute
    command: |
      echo "推送特性分支到远程..."
      
      # 推送分支
      git push -u origin $FEATURE_BRANCH
      
      # 创建PR模板
      cat > pull_request_template.md << EOL
      ## PR: {{captures.feature_name}}
      
      {{feature_description}}
      
      ### 变更内容
      
      <!-- 描述你的变更 -->
      
      ### 相关问题
      
      <!-- 链接相关问题 -->
      
      ### 测试
      
      <!-- 描述如何测试这个PR -->
      
      ### 审阅注意事项
      
      <!-- 审阅者应特别注意的地方 -->
      
      ### 检查清单
      
      - [ ] 代码遵循项目编码规范
      - [ ] 添加了适当的测试
      - [ ] 更新了文档
      - [ ] PR标题遵循约定式提交格式
      EOL
      
      echo "特性分支已推送，可以在GitHub上创建PR"
  
  - type: suggest
    message: |
      ## 特性开发工作流已初始化 ✅
      
      已完成 "{{captures.feature_name}}" 特性的开发环境设置:
      
      1. ✅ **特性规划**: 创建了特性规划文档
      2. ✅ **环境准备**: 根据特性类型({{feature_type}})设置了开发环境
      3. ✅ **测试设置**: 创建了测试计划
      4. ✅ **CI配置**: 配置了持续集成流程
      5. ✅ **分支管理**: 推送了特性分支并创建PR模板
      
      ### 下一步
      
      1. 完善特性规划文档: `docs/features/{{captures.feature_name}}.md`
      2. 完成特性实现
      3. 添加测试用例
      4. 创建PR请求代码审查
      
      可以使用以下命令查看工作流创建的文件:
      
      ```bash
      git log --name-status HEAD~5..HEAD
      ```

metadata:
  priority: critical
  version: 1.0.0
  tags: ["workflow", "automation", "feature-development"]
</rule>
```

以下是针对特性分支创建部分的调整示例：

```CMD
# Windows CMD
@echo off
echo 创建特性分支...

rem 确保我们在最新的主分支上
git checkout main
git pull

rem 创建特性分支
set featureBranch=feature/%featureName%
git checkout -b %featureBranch%

rem 创建特性规划文档
set featuresDir=docs\features
if not exist %featuresDir% mkdir %featuresDir%

rem 生成特性规划文档

# Linux/macOS
#!/bin/bash
echo "创建特性分支..."

# 确保我们在最新的主分支上
git checkout main
git pull

# 创建特性分支
featureBranch="feature/$featureName"
git checkout -b $featureBranch

# 创建特性规划文档
featuresDir="docs/features"
mkdir -p $featuresDir

# 生成特性规划文档
# Cursor Rules 教程系列 (CorLings)

<div align="center">
  <img src="./images/CorLings.png" alt="CorLings" width="500" />
  <h3>通过结构化学习掌握Cursor Rules的艺术</h3>
</div>

## 项目介绍

CorLings (Cursor Rules Learnings) 是一套全面的、结构化的Cursor Rules教程系列，旨在帮助开发者从入门到精通Cursor Rules的各个方面。通过循序渐进的学习路径，您将了解如何利用Cursor Rules提高开发效率、保证代码质量，并实现工作流程自动化。

本教程适合：
- 希望提高AI辅助编程效率的开发者
- 追求代码质量一致性的团队
- 想要自动化开发工作流的项目负责人
- 对Cursor Rules感兴趣的任何人

## 教程结构

本教程分为10个主要章节，每个章节聚焦于Cursor Rules的特定方面：

1. **[基础介绍](CorLings/01-Introduction.md)** - Cursor Rules的概念和核心理念
2. **[基础设置与环境](CorLings/02-BasicSetup.md)** - 环境配置和初始设置
3. **[规则组件详解](CorLings/03-RuleComponents.md)** - 过滤器、动作和元数据等核心组件
4. **[基础规则编写](CorLings/04-BasicRules.md)** - 编写简单规则的方法和技巧
5. **[高级规则技术](CorLings/05-AdvancedRules.md)** - 复杂规则、条件逻辑和高级组件
6. **[工作流集成](CorLings/06-WorkflowIntegration-Part1.md)** - 将规则融入开发工作流
7. **[规则库管理](CorLings/07-RuleLibrary-Part1.md)** - 规则的组织、版本控制和维护
8. **[实际案例研究](CorLings/08-CaseStudies-Part1.md)** - 真实项目中的应用实例
9. **[高级架构](CorLings/09-AdvancedArchitecture-Part1.md)** - 多代理系统和自学习规则系统
10. **[未来发展方向](CorLings/10-FutureDirections.md)** - 新特性、趋势和学习路径

为便于阅读，一些章节被分为多个部分：
- 第6章：[第一部分](CorLings/06-WorkflowIntegration-Part1.md) | [第二部分](CorLings/06-WorkflowIntegration-Part2.md) | [第三部分](CorLings/06-WorkflowIntegration-Part3.md)
- 第7章：[第一部分](CorLings/07-RuleLibrary-Part1.md) | [第二部分](CorLings/07-RuleLibrary-Part2.md) | [第三部分](CorLings/07-RuleLibrary-Part3.md) | [第四部分](CorLings/07-RuleLibrary-Part4.md) | [第五部分](CorLings/07-RuleLibrary-Part5.md)
- 第8章：[第一部分](CorLings/08-CaseStudies-Part1.md) | [第二部分](CorLings/08-CaseStudies-Part2.md) | [第三部分](CorLings/08-CaseStudies-Part3.md) | [第四部分](CorLings/08-CaseStudies-Part4.md)
- 第9章：[第一部分](CorLings/09-AdvancedArchitecture-Part1.md) | [第二部分](CorLings/09-AdvancedArchitecture-Part2.md)

## 辅助资源

除了核心教程章节外，我们还提供以下辅助资源，帮助您更好地学习和应用Cursor Rules：

1. **[用户指南](CorLings/UserGuide.md)** - 提供教程使用方法、学习路径建议和最佳实践
2. **[故障排除指南](CorLings/Troubleshooting.md)** - 收集常见错误和解决方案的参考手册
3. **[贡献指南](CorLings/CONTRIBUTING.md)** - 说明如何为教程项目贡献内容和改进
4. **[~~GeneratePDF.ps1~~](CorLings/GeneratePDF.ps1)** - ~~PDF生成脚本，用于将所有教程内容合并为PDF文档的工具~~(需安装 Microsoft Word)
5. **[GeneratePDF.py](CorLings/GeneratePDF.py)** - 使用pypandoc库实现的PDF生成脚本，更简洁高效
6. **[CorLingsPDFGenerator.exe](CorLings/CorLingsPDFGenerator.exe)** - PDF生成可执行文件，用于将所有教程内容合并为PDF文档(基于Pandoc，需安装xelatex)
7. **[术语表](CorLings/Glossary.md)** - Cursor Rules相关术语的定义和解释

这些资源文件可以帮助您更有效地使用教程内容，解决实际问题，并参与到教程的持续改进中。

## 文件说明

以下是项目特定文件的说明：

- **[UserGuide.md](CorLings/UserGuide.md)** - 用户指南，提供教程使用方法、学习路径建议和最佳实践
- **[Troubleshooting.md](CorLings/Troubleshooting.md)** - 故障排除指南，收集常见错误和解决方案的参考手册
- **[CONTRIBUTING.md](CorLings/CONTRIBUTING.md)** - 贡献指南，说明如何为教程项目贡献内容和改进
- **[~~GeneratePDF.ps1~~](CorLings/GeneratePDF.ps1)** - ~~PDF生成脚本，用于将所有教程内容合并为PDF文档的工具~~(需安装 Microsoft Word)
- **[GeneratePDF.py](CorLings/GeneratePDF.py)** - 使用pypandoc库实现的PDF生成脚本，更简洁高效
- **[CorLingsPDFGenerator.exe](CorLings/CorLingsPDFGenerator.exe)** - PDF生成可执行文件，用于将所有教程内容合并为PDF文档(基于Pandoc，需安装xelatex)
- **[Glossary.md](CorLings/Glossary.md)** - 术语表，Cursor Rules相关术语的定义和解释

## 使用PDF生成工具

要生成完整的PDF教程文档，您需要：

1. 安装Python 3.6或更高版本
2. 安装Pandoc: 从 [https://pandoc.org/installing.html](https://pandoc.org/installing.html) 下载并安装
3. 安装LaTeX引擎(用于PDF生成):
   - Windows: 安装[MiKTeX](https://miktex.org/download) 或 [TeX Live](https://tug.org/texlive/windows.html)
   - macOS: 安装[MacTeX](https://tug.org/mactex/)
   - Linux: 安装TeX Live (`sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic`)
4. 安装Python依赖: `pip install pypandoc`
5. 运行PDF生成脚本: `python CorLings/GeneratePDF.py`

生成的PDF文件将保存为 `CorLings-完整教程.pdf`。

## 特色内容

本教程系列的特色包括：

- **实践导向** - 每章都包含实际可用的代码和规则示例
- **循序渐进** - 从基础概念到高级架构的清晰学习路径
- **丰富案例** - 真实世界中的应用案例和最佳实践
- **完整示例** - 可以直接复制使用的规则和脚本

## 如何使用本教程

我们建议按照章节顺序学习，但您也可以根据需要跳转到特定章节：

1. 初学者应从第1章开始，逐章学习基础知识
2. 已了解基础的开发者可以从第5章开始学习高级技术
3. 团队负责人可能对第7章的规则库管理特别感兴趣
4. 寻找解决特定问题的开发者可以直接查看第8章的案例研究

## 环境要求

- Cursor IDE（最新版本）
- 基本的编程知识
- Windows、macOS或Linux操作系统

## 社区贡献

我们欢迎社区对教程内容的贡献和改进：

- 提交错误修正或内容更新的拉取请求
- 分享您创建的规则示例
- 提出新的章节或主题建议

## 许可协议

本教程系列采用 [MIT许可协议](LICENSE)。您可以自由使用、修改和分享这些内容，但请保留原始著作权声明。

## 致谢

特别感谢Cursor团队创建了这一强大的开发工具，以及所有为本教程提供反馈和建议的社区成员。

---

开始您的Cursor Rules学习之旅，点击 [基础介绍](CorLings/01-Introduction.md) 章节！ 
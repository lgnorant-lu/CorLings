# -*- coding: utf-8 -*-
"""
CorLings PDF生成脚本 - 使用pypandoc简化Markdown到PDF的转换

使用说明：
1. 确保已安装以下依赖：
   - Python 3.6+
   - pypandoc (pip install pypandoc)
   - pandoc (https://pandoc.org/installing.html)
   - 对于PDF生成，需要安装以下之一：
     a. XeLaTeX (推荐，通过安装MiKTeX或TeX Live)
     b. pdflatex (作为备选)
     c. weasyprint (pip install weasyprint，需要额外的系统依赖)
     d. pdfkit (pip install pdfkit，需要额外安装wkhtmltopdf)

2. 使用方法：
   - 将本脚本放在章节文件所在的目录中
   - 运行：python GeneratePDF.py
   - 生成的文件会保存在父目录中

3. 已知问题：
   - 生成PDF时可能会遇到特殊字符处理问题，尤其是代码块中的LaTeX特殊字符
   - 中文字体可能需要额外配置
   - 如果PDF生成失败，脚本会生成一个HTML文件作为备选
   - 环境变量引用（如%VarName%）可能导致LaTeX处理错误

4. 故障排除：
   - 如果生成PDF失败，检查是否正确安装了XeLaTeX或其他PDF引擎
   - 如果HTML文件中缺少内容，检查临时生成的Markdown文件中是否存在格式问题
   - 对于特殊字符问题，可以尝试在preprocess_markdown函数中增加更多替换规则

作者：lgnorant-lu
最后更新：2025-03-15
"""
import os
import sys
import logging
import datetime
import re
from pathlib import Path


# 设置日志
logging.basicConfig(
    level=logging.DEBUG,  # 将日志级别从INFO改为DEBUG，获取更多信息
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import pypandoc
except ImportError as e:
    logger.error(f"缺少必要的库: {e}")
    logger.info("请运行: pip install pypandoc")
    logger.info("同时需要安装Pandoc: https://pandoc.org/installing.html")
    sys.exit(1)


def preprocess_markdown(content):
    """预处理Markdown内容，确保特殊字符正确显示"""
    logger.debug("开始预处理Markdown内容...")
    
    # 保护代码块，避免其中的特殊字符被转义
    protected_blocks = []
    
    # 特殊替换：处理.cursor\rules字符串，这是导致LaTeX错误的主要原因
    content = content.replace(".cursor\\rules", ".cursor-rules")
    content = content.replace(".cursor\\\\rules", ".cursor-rules")
    
    # 特殊替换：处理%libraryPath%\library.json字符串
    content = content.replace("%libraryPath%\\library.json", "percentlibraryPathpercent-library.json")
    content = content.replace("%libraryPath%\\\\library.json", "percentlibraryPathpercent-library.json")
    content = content.replace("\\%libraryPath\\%\\library", "percentlibraryPathpercent-library")
    
    # 特殊替换：处理其他特殊环境变量引用
    pattern = re.compile(r'%([A-Za-z0-9_]+)%')
    content = pattern.sub(r'percent\1percent', content)
    
    # 定义一个函数来处理代码块保护
    def protect_code_blocks(match):
        code_block = match.group(0)
        placeholder = f"___CODEBLOCK_{len(protected_blocks)}___"
        protected_blocks.append(code_block)
        return placeholder
    
    # 保存代码块
    content = re.sub(r'```[\s\S]*?```', protect_code_blocks, content)
    
    # 保护行内代码
    inline_codes = []
    def protect_inline_code(match):
        code = match.group(0)
        placeholder = f"___INLINECODE_{len(inline_codes)}___"
        inline_codes.append(code)
        return placeholder
    
    content = re.sub(r'`[^`]+`', protect_inline_code, content)
    
    # 处理LaTeX特殊字符 (避免在普通文本中的问题)
    replacements = {
        '\\': '\\\\',
        '{': '\\{',
        '}': '\\}',
        '#': '\\#',
        '$': '\\$',
        '%': '\\%',
        '&': '\\&',
        '_': '\\_',
        '^': '\\^',
        '~': '\\textasciitilde{}',
        '<': '\\textless{}',
        '>': '\\textgreater{}',
        '|': '\\textbar{}',
        '"': '\\textquotedbl{}',
        "'": '\\textquotesingle{}',
        '`': '\\`',
        # 特别处理file_extension词汇
        'file_extension': 'file\\_extension'
    }
    
    # 应用替换但避开占位符
    for pattern, replacement in replacements.items():
        # 避开占位符
        pattern_regex = f'(?<!___)({re.escape(pattern)})(?!___)'
        content = re.sub(pattern_regex, replacement, content)
    
    # 恢复行内代码，并保证在LaTeX中正确显示
    for i, code in enumerate(inline_codes):
        # 去掉行内代码的反引号，但保留内容
        code_content = code[1:-1]
        
        # 特殊处理：如果内容包含"file_extension"，直接使用text而不是texttt
        if "file_extension" in code_content:
            latex_code = f'\\text{{{code_content}}}'
        else:
            # 为行内代码添加LaTeX语法，使用text而不是texttt避免问题
            latex_code = f'\\text{{{code_content}}}'
        
        content = content.replace(f"___INLINECODE_{i}___", latex_code)
    
    # 恢复代码块，并使用LaTeX listings包格式化
    for i, block in enumerate(protected_blocks):
        # 提取语言和代码内容
        match = re.match(r'```(\w*)\n([\s\S]*?)```', block)
        if match:
            lang, code = match.groups()
            # 默认为文本，如果没有指定语言
            lang = lang.strip() or 'text'
            
            # 特殊处理：检查并替换潜在问题代码，尤其是.cursor\rules
            code = code.replace(".cursor\\rules", ".cursor-rules")
            code = code.replace(".cursor\\\\rules", ".cursor-rules")
            
            # 转义代码块中的特殊字符
            for char, esc in {'\\': '\\textbackslash{}', '{': '\\{', '}': '\\}'}.items():
                code = code.replace(char, esc)
            
            # 使用LaTeX verbatim环境而不是listings，更简单，更少问题
            latex_code = f'\\begin{{verbatim}}\n{code}\n\\end{{verbatim}}'
            
            content = content.replace(f"___CODEBLOCK_{i}___", latex_code)
    
    # 添加自定义LaTeX头部
    latex_header = '''\\usepackage{listings}
\\usepackage{xcolor}
\\usepackage{verbatim}
\\lstset{
    breaklines=true,
    basicstyle=\\ttfamily\\small,
    commentstyle=\\color{green!50!black},
    keywordstyle=\\color{blue},
    stringstyle=\\color{red},
    numberstyle=\\ttfamily\\tiny\\color{gray},
    backgroundcolor=\\color{gray!10},
    frame=single,
    rulecolor=\\color{black!30},
    captionpos=b,
    tabsize=2,
}

% 重新定义lstinline命令为text
\\let\\oldlstinline\\lstinline
\\renewcommand{\\lstinline}[1]{\\text{#1}}

\\usepackage{fontspec}
\\setmainfont{SimSun}
\\setsansfont{SimHei}
\\setmonofont{Consolas}
'''
    
    logger.debug("Markdown预处理完成")
    return content, latex_header


def main():
    # 获取当前文件的目录路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 设置基本路径，为脚本所在目录的父目录
    base_path = os.path.dirname(script_dir)
    
    # 设置章节文件所在目录
    chapters_path = script_dir
    
    # 改进：输出文件路径，确保在正确的目录下生成文件
    output_file_path = os.path.join(base_path, "CorLings-完整教程.pdf")
    logger.info(f"输出文件将保存至: {output_file_path}")
    
    # 章节文件列表（添加完整路径）
    chapters = [
        "01-Introduction.md",
        "02-BasicSetup.md",
        "03-RuleComponents.md",
        "04-BasicRules.md",
        "05-AdvancedRules.md",
        "06-WorkflowIntegration.md",
        "07-RuleLibrary-Part1.md",
        "07-RuleLibrary-Part2.md",
        "07-RuleLibrary-Part3.md",
        "07-RuleLibrary-Part4.md",
        "07-RuleLibrary-Part5.md",
        "08-CaseStudies-Part1.md",
        "08-CaseStudies-Part2.md",
        "08-CaseStudies-Part3.md",
        "08-CaseStudies-Part4.md",
        "09-AdvancedArchitecture-Part1.md",
        "09-AdvancedArchitecture-Part2.md",
        "10-FutureDirections.md"
    ]
    
    try:
        # 确认所有章节文件的存在
        missing_files = []
        chapter_full_paths = []
        
        for file in chapters:
            file_path = os.path.join(chapters_path, file)
            if os.path.exists(file_path):
                chapter_full_paths.append(file_path)
                logger.info(f"找到章节文件: {file}")
            else:
                missing_files.append(file)
                logger.warning(f"无法找到章节文件: {file}")
        
        if missing_files:
            logger.warning(f"以下章节文件不存在: {', '.join(missing_files)}")
            if not chapter_full_paths:
                raise FileNotFoundError("所有章节文件均不存在，无法继续。")
            logger.info("但仍有可用章节文件，将继续处理...")
        
        try:
            # 读取所有章节文件
            content = ""
            for chapter_file in chapter_full_paths:
                if os.path.exists(chapter_file):
                    with open(chapter_file, 'r', encoding='utf-8') as file:
                        chapter_content = file.read()
                        content += f"\n\n{chapter_content}\n\n"
                        logger.debug(f"添加章节: {chapter_file}")
                else:
                    logger.warning(f"章节文件不存在: {chapter_file}")
            
            # 预处理Markdown内容
            content, latex_header = preprocess_markdown(content)
            
            # 创建临时文件，使用绝对路径确保放在正确位置
            temp_md_file = f"{os.path.splitext(output_file_path)[0]}-temp.md"
            with open(temp_md_file, 'w', encoding='utf-8') as file:
                file.write(content)
            
            logger.info(f"创建临时文件: {temp_md_file}")
            
            # 创建自定义LaTeX头部文件
            header_file = f"{os.path.splitext(output_file_path)[0]}-header.tex"
            with open(header_file, 'w', encoding='utf-8') as file:
                file.write(latex_header)
            
            logger.info(f"创建LaTeX头部文件: {header_file}")
            
            # 使用pypandoc生成PDF
            logger.info("使用pypandoc生成PDF文件...")
            
            # 定义Pandoc转换选项
            extra_args = [
                '--pdf-engine=xelatex',          # 使用xelatex作为PDF引擎，支持中文
                '--toc',                         # 生成目录
                '--toc-depth=3',                 # 目录深度
                '-V', 'geometry:margin=1in',     # 设置页边距
                '-V', 'mainfont=SimSun',         # 设置中文字体
                '-V', 'CJKmainfont=SimSun',      # 指定CJK字体
                '-V', 'fontenc=T1',              # 使用T1字体编码
                '-V', 'colorlinks=true',         # 链接着色
                '-V', 'linkcolor=blue',          # 链接颜色
                '-V', 'toccolor=blue',           # 目录颜色
                '--highlight-style=tango',       # 代码高亮风格
                '-V', 'monofont=Consolas',       # 等宽字体
                # 为代码块中的中文指定字体
                '-V', 'monofontoptions=Scale=0.9', 
                '--listings',                    # 使用listings包处理代码块
                '--no-highlight',                # 禁用默认高亮，使用listings
                '-V', 'title=Cursor Rules 教程', # 指定标题避免默认标题问题
                '--metadata=lang:zh-CN',         # 指定中文
                '--verbose',                     # 显示详细信息
            ]
            
            # 添加头文件到Pandoc参数
            extra_args.extend(['--include-in-header', header_file])
            
            # 使用pandoc生成PDF
            logger.info("开始生成PDF...")
            try:
                # 尝试使用xelatex生成PDF
                output = pypandoc.convert_file(
                    temp_md_file,           # 输入文件
                    'pdf',                  # 输出格式
                    outputfile=output_file_path,  # 输出文件
                    extra_args=extra_args
                )
                
                # 检查PDF文件是否生成
                if os.path.exists(output_file_path):
                    file_size = os.path.getsize(output_file_path) / (1024 * 1024)  # 转换为MB        
                    logger.info(f"PDF生成成功！文件: {output_file_path}")
                    logger.info(f"PDF文件大小: {file_size:.2f} MB")
                    
                    # 删除临时文件
                    os.remove(temp_md_file)
                    os.remove(header_file)
                    logger.debug(f"临时文件已删除: {temp_md_file}, {header_file}")
                else:
                    raise Exception("PDF文件未生成")
                
            except Exception as pandoc_e:
                # 主要方法失败，尝试备用方案
                logger.error(f"使用pandoc+xelatex生成PDF失败: {pandoc_e}")
                try:
                    # 尝试使用pdflatex引擎
                    logger.info("尝试使用pdflatex引擎...")
                    output = pypandoc.convert_file(
                        temp_md_file,
                        'pdf',
                        outputfile=output_file_path,
                        extra_args=[
                            '--pdf-engine=pdflatex',
                            f'--include-in-header={header_file}',
                            '--toc',
                            '--toc-depth=3',
                            '-V', 'geometry:margin=1in',
                            '-V', 'fontsize=11pt',
                        ]
                    )
                    
                    if os.path.exists(output_file_path):
                        file_size = os.path.getsize(output_file_path) / (1024 * 1024)
                        logger.info(f"PDF生成成功(使用pdflatex)！文件: {output_file_path}")    
                        logger.info(f"PDF文件大小: {file_size:.2f} MB")
                        
                        # 删除临时文件
                        os.remove(temp_md_file)
                        os.remove(header_file)
                        logger.debug(f"临时文件已删除: {temp_md_file}, {header_file}")
                    else:
                        raise Exception("PDF文件未生成")
                    
                except Exception as backup_e:
                    # 如果备用方案也失败，尝试使用weasyprint
                    logger.error(f"备用方法也失败，尝试使用weasyprint生成PDF")
                    try:
                        logger.debug("尝试使用weasyprint生成PDF")
                        try:
                            import weasyprint
                            logger.info("使用weasyprint生成PDF...")
                            
                            # 先转换为HTML
                            html_file = output_file_path.replace('.pdf', '.html')
                            logger.debug(f"生成中间HTML文件: {html_file}")
                            
                            pypandoc.convert_file(
                                temp_md_file,
                                'html',
                                outputfile=html_file,
                                extra_args=['--standalone', '--self-contained']
                            )
                            
                            logger.debug(f"HTML文件生成成功，开始转换为PDF")
                            # 使用weasyprint将HTML转换为PDF
                            weasyprint.HTML(html_file).write_pdf(output_file_path)
                            
                            if os.path.exists(output_file_path):
                                file_size = os.path.getsize(output_file_path) / (1024 * 1024)
                                logger.info(f"PDF生成成功（使用weasyprint）！文件: {output_file_path}")
                                logger.info(f"PDF文件大小: {file_size:.2f} MB")
                                os.remove(html_file)
                            else:
                                raise Exception("PDF文件未生成")
                        except ImportError:
                            logger.error("weasyprint未安装，需要手动安装：pip install weasyprint")
                            # 尝试使用pdfkit
                            try:
                                import pdfkit
                                logger.info("尝试使用pdfkit生成PDF...")
                                
                                # 先转换为HTML
                                html_file = output_file_path.replace('.pdf', '.html')
                                logger.debug(f"生成中间HTML文件: {html_file}")
                                
                                pypandoc.convert_file(
                                    temp_md_file,
                                    'html',
                                    outputfile=html_file,
                                    extra_args=['--standalone', '--self-contained']
                                )
                                
                                # 配置pdfkit
                                options = {
                                    'encoding': 'UTF-8',
                                    'page-size': 'A4',
                                    'margin-top': '1in',
                                    'margin-right': '1in',
                                    'margin-bottom': '1in',
                                    'margin-left': '1in',
                                }
                                
                                # 使用pdfkit转换HTML到PDF
                                pdfkit.from_file(html_file, output_file_path, options=options)
                                
                                if os.path.exists(output_file_path):
                                    file_size = os.path.getsize(output_file_path) / (1024 * 1024)
                                    
                                    logger.info(f"PDF生成成功（使用pdfkit）！文件: {output_file_path}")
                                    logger.info(f"PDF文件大小: {file_size:.2f} MB")
                                else:
                                    raise Exception("PDF文件未生成")
                            except ImportError:
                                logger.error("pdfkit未安装，需要手动安装：pip install pdfkit")
                                # 保存为HTML作为备选
                                html_file = output_file_path.replace('.pdf', '.html')
                                pypandoc.convert_file(
                                    temp_md_file,
                                    'html',
                                    outputfile=html_file,
                                    extra_args=['--standalone', '--self-contained', '--metadata', 'title="Cursor Rules 教程"']
                                )
                                logger.info(f"无法生成PDF，但已生成HTML文件: {html_file}")
                                logger.info("请安装以下工具之一来生成PDF: 1) xelatex (MiKTeX/TeX Live), 2) weasyprint, 或 3) pdfkit+wkhtmltopdf")
                    except Exception as e:
                        logger.error(f"使用备选方案生成PDF时出错: {e}")
                        logger.debug(f"错误详情: {str(e)}")
                        # 保存为HTML作为最终备选
                        html_file = output_file_path.replace('.pdf', '.html')
                        try:
                            pypandoc.convert_file(
                                temp_md_file,
                                'html',
                                outputfile=html_file,
                                extra_args=['--standalone', '--self-contained', '--metadata', 'title="Cursor Rules 教程"']
                            )
                            logger.info(f"无法生成PDF，但已生成HTML文件: {html_file}")
                        except Exception as html_e:
                            logger.error(f"生成HTML也失败: {html_e}")
                
        except Exception as e:
            logger.error(f"生成PDF时发生错误: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise
            
    except Exception as e:
        logger.error(f"生成PDF时发生错误: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise
        
    finally:
        # 确保清理临时文件
        try:
            temp_md_file = f"{os.path.splitext(output_file_path)[0]}-temp.md"
            header_file = f"{os.path.splitext(output_file_path)[0]}-header.tex"
            
            if os.path.exists(temp_md_file):
                os.remove(temp_md_file)
                logger.debug(f"已删除临时文件: {temp_md_file}")
            if os.path.exists(header_file):
                os.remove(header_file)
                logger.debug(f"已删除临时文件: {header_file}")
        except Exception as e:
            logger.warning(f"清理临时文件时出错: {e}")
            
        # 添加结果文件位置提示
        if os.path.exists(output_file_path):
            logger.info(f"成功生成PDF: {output_file_path}")
            logger.info(f"PDF文件路径: {os.path.abspath(output_file_path)}")
        else:
            html_file = output_file_path.replace('.pdf', '.html')
            if os.path.exists(html_file):
                logger.info(f"生成了HTML文件: {html_file}")
                logger.info(f"HTML文件路径: {os.path.abspath(html_file)}")
            else:
                logger.warning("未生成PDF或HTML文件，请检查错误输出")


if __name__ == "__main__":
    main()
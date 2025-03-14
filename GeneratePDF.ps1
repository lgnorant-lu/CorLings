# CorLings PDF生成脚本 (优化版)
# 此脚本使用Microsoft Word将所有CorLings教程Markdown文件合并并生成PDF文档
# 优点：不需要安装额外软件，只要有Microsoft Word即可(大多数Windows系统已安装)
# 作者：lgnorant-lu

# 设置文件编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 配置参数
$outputFileName = "CorLings-完整教程.pdf"
$tempMergedFile = "temp_merged.md"
$tempHtmlFile = "temp_merged.html"
$chaptersPath = "."  # 当前目录

# 定义文件顺序（确保按正确顺序合并）
$fileOrder = @(
    "01-Introduction.md",
    "02-BasicSetup.md",
    "03-RuleComponents.md",
    "04-BasicRules.md",
    "05-AdvancedRules.md",
    "06-WorkflowIntegration-Part1.md",
    "06-WorkflowIntegration-Part2.md",
    "06-WorkflowIntegration-Part3.md",
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
    "10-FutureDirections.md",
    "UserGuide.md",
    "Troubleshooting.md",
    "Glossary.md"
)

Write-Host "开始生成PDF..." -ForegroundColor Cyan

# 检查是否安装了Microsoft Word
try {
    $null = New-Object -ComObject Word.Application
    Write-Host "已检测到Microsoft Word，可以继续执行" -ForegroundColor Green
}
catch {
    Write-Error "未检测到Microsoft Word。请安装Microsoft Word后再运行此脚本。"
    exit 1
}
finally {
    # 释放COM对象
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}

# 创建临时目录用于处理文件
$tempDir = ".\temp_pdf_build"
if (!(Test-Path -Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
}

# 创建封面页内容
$coverContent = @"
# Cursor Rules 教程系列 (CorLings)

![Cursor Logo](https://cursor.sh/brand/app-icon-512.png)

## 通过结构化学习掌握Cursor Rules的艺术

**版本:** 1.0
**生成日期:** $(Get-Date -Format "yyyy-MM-dd")

---

本PDF文档由CorLings项目自动生成，包含完整的Cursor Rules学习教程，从基础概念到高级应用。

"@

# 合并所有文件
Write-Host "合并Markdown文件..." -ForegroundColor Cyan
$allContent = $coverContent
$filesToMerge = @()

# 添加指定顺序的文件
foreach ($file in $fileOrder) {
    $filePath = Join-Path -Path $chaptersPath -ChildPath $file
    if (Test-Path $filePath) {
        $filesToMerge += $filePath
        Write-Host "  - 添加: $file" -ForegroundColor Gray
    }
    else {
        Write-Warning "文件未找到: $filePath"
    }
}

# 添加目录部分
$tocContent = @"

# 目录

"@

foreach ($file in $fileOrder) {
    $filePath = Join-Path -Path $chaptersPath -ChildPath $file
    if (Test-Path $filePath) {
        $fileContent = Get-Content -Path $filePath -Raw -Encoding UTF8
        if ($fileContent -match "^#\s+(.+)") {
            $title = $matches[1]
            $tocContent += "- [$title](#$($title.ToLower() -replace '[^a-z0-9\s]', '' -replace '\s+', '-'))`n"
        }
    }
}

$allContent += "`n`n$tocContent`n`n"

# 合并文件内容
$separator = "`n`n---`n`n"
foreach ($file in $filesToMerge) {
    $content = Get-Content -Path $file -Raw -Encoding UTF8
    
    # 处理相对路径的图片引用
    $fileDir = Split-Path -Parent $file
    $content = $content -replace '!\[(.*?)\]\((?!http)(.*?)\)', ('![$1](' + $fileDir + '/$2)')
    
    $allContent += $separator + $content
}

# 创建临时合并的MD文件
$allContent | Out-File -FilePath $tempMergedFile -Encoding UTF8

# 简单的Markdown到HTML转换函数
function Convert-MarkdownToHtml {
    param (
        [string]$markdown
    )

    # 基本的Markdown转HTML规则
    $html = $markdown
    
    # 添加HTML头
    $html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CorLings - Cursor Rules 教程系列</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 { 
            color: #0066cc; 
            margin-top: 24px;
        }
        h1 { font-size: 28px; border-bottom: 1px solid #eaecef; padding-bottom: 10px; }
        h2 { font-size: 24px; border-bottom: 1px solid #eaecef; padding-bottom: 8px; }
        h3 { font-size: 20px; }
        h4 { font-size: 18px; }
        h5 { font-size: 16px; }
        h6 { font-size: 16px; color: #6a737d; }
        p, ul, ol { margin-bottom: 16px; }
        code { 
            font-family: Consolas, "Courier New", monospace;
            padding: 2px 4px;
            background-color: #f6f8fa;
            border-radius: 3px;
        }
        pre { 
            background-color: #f6f8fa;
            border-radius: 3px;
            padding: 16px;
            overflow: auto;
        }
        pre code {
            background-color: transparent;
            padding: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }
        th, td {
            border: 1px solid #dfe2e5;
            padding: 8px 12px;
        }
        th {
            background-color: #f6f8fa;
            font-weight: 600;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        blockquote {
            margin: 0;
            padding: 0 16px;
            color: #6a737d;
            border-left: 4px solid #dfe2e5;
        }
        hr {
            height: 1px;
            background-color: #e1e4e8;
            border: none;
            margin: 24px 0;
        }
        .page-break {
            page-break-after: always;
        }
    </style>
</head>
<body>
"@

    # 处理标题（# 到 ######）
    $html += $markdown -replace '^#{6}\s+(.+)$', '<h6>$1</h6>' `
                      -replace '^#{5}\s+(.+)$', '<h5>$1</h5>' `
                      -replace '^#{4}\s+(.+)$', '<h4>$1</h4>' `
                      -replace '^#{3}\s+(.+)$', '<h3>$1</h3>' `
                      -replace '^#{2}\s+(.+)$', '<h2>$1</h2>' `
                      -replace '^#{1}\s+(.+)$', '<h1>$1</h1>'

    # 处理代码块
    $html = $html -replace '```([^`]+)```', '<pre><code>$1</code></pre>'
    
    # 处理行内代码
    $html = $html -replace '`([^`]+)`', '<code>$1</code>'
    
    # 处理粗体和斜体
    $html = $html -replace '\*\*([^*]+)\*\*', '<strong>$1</strong>' `
                 -replace '\*([^*]+)\*', '<em>$1</em>'
    
    # 处理链接
    $html = $html -replace '\[([^\]]+)\]\(([^)]+)\)', '<a href="$2">$1</a>'
    
    # 处理图片
    $html = $html -replace '!\[([^\]]*)\]\(([^)]+)\)', '<img src="$2" alt="$1">'
    
    # 处理列表
    $html = $html -replace '^\s*-\s+(.+)$', '<li>$1</li>' `
                 -replace '^\s*\d+\.\s+(.+)$', '<li>$1</li>'
                 
    # 处理段落
    $html = $html -replace '(\r?\n){2,}', '</p><p>'
    
    # 处理分隔线
    $html = $html -replace '^---$', '<hr>'
    
    # 关闭HTML
    $html += "</body></html>"
    
    return $html
}

# 将Markdown转换为HTML
Write-Host "正在生成HTML..." -ForegroundColor Cyan
$markdownText = Get-Content -Path $tempMergedFile -Raw -Encoding UTF8
$htmlContent = Convert-MarkdownToHtml -markdown $markdownText
$htmlContent | Out-File -FilePath $tempHtmlFile -Encoding UTF8

# 使用Word将HTML转换为PDF
Write-Host "使用Microsoft Word生成PDF..." -ForegroundColor Cyan

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    
    # 如果PDF文件已存在，先删除它
    if (Test-Path $outputFileName) {
        Remove-Item $outputFileName -Force
    }
    
    $doc = $word.Documents.Open((Resolve-Path $tempHtmlFile))
    $doc.SaveAs([ref] (Resolve-Path .).Path + "\$outputFileName", 17) # WdSaveFormat.wdFormatPDF = 17
    $doc.Close()
    $word.Quit()
    
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    
    Write-Host "PDF生成成功！文件: $outputFileName" -ForegroundColor Green
    
    # 计算文件大小
    $fileSize = (Get-Item $outputFileName).Length / 1MB
    $fileSize = [math]::Round($fileSize, 2)
    Write-Host "PDF文件大小: $fileSize MB" -ForegroundColor Cyan
}
catch {
    Write-Error "生成PDF时发生错误: $_"
}
finally {
    # 清理临时文件
    Write-Host "清理临时文件..." -ForegroundColor Cyan
    if (Test-Path $tempMergedFile) { Remove-Item $tempMergedFile -Force }
    if (Test-Path $tempHtmlFile) { Remove-Item $tempHtmlFile -Force }
    if (Test-Path -Path $tempDir) { Remove-Item -Path $tempDir -Recurse -Force }
}

Write-Host "\n完成！PDF文件已生成: $outputFileName" -ForegroundColor Green
Write-Host "注意: 此脚本需要Microsoft Word来生成PDF。如果未安装Word, 请考虑使用在线Markdown到PDF转换工具." -ForegroundColor Yellow
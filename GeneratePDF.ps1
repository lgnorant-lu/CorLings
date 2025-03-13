# CorLings PDF生成脚本
# 此脚本将所有CorLings教程markdown文件合并并生成一个完整的PDF文档
# 要求：安装Pandoc (https://pandoc.org) 和 wkhtmltopdf (https://wkhtmltopdf.org)

# 配置参数
$outputFileName = "CorLings-完整教程.pdf"
$tempMergedFile = "temp_merged.md"
$coverPageFile = "temp_cover.md"
$tocDepth = 3
$chaptersPath = "."  # 当前目录（应该包含所有CorLings目录）

# 创建封面页
$coverContent = @"
---
title: "Cursor Rules 教程系列 (CorLings)"
author: "CorLings 项目组"
date: "$(Get-Date -Format "yyyy-MM-dd")"
---

![Cursor Logo](https://cursor.sh/brand/app-icon-512.png)

# Cursor Rules 教程系列

*通过结构化学习掌握Cursor Rules的艺术*

**版本:** 1.0
**生成日期:** $(Get-Date -Format "yyyy-MM-dd")

---

本PDF文档由CorLings项目自动生成，包含完整的Cursor Rules学习教程，从基础概念到高级应用。

"@
$coverContent | Out-File -FilePath $coverPageFile -Encoding utf8

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
    "Troubleshooting.md"
)

Write-Host "开始生成PDF..."

# 检查Pandoc和wkhtmltopdf是否安装
try {
    $pandocVersion = pandoc --version | Select-Object -First 1
    Write-Host "已检测到Pandoc: $pandocVersion"
}
catch {
    Write-Error "未检测到Pandoc。请安装Pandoc后再运行此脚本: https://pandoc.org/installing.html"
    exit 1
}

try {
    $wkhtmltopdfVersion = wkhtmltopdf --version
    Write-Host "已检测到wkhtmltopdf: $wkhtmltopdfVersion"
}
catch {
    Write-Error "未检测到wkhtmltopdf。请安装wkhtmltopdf后再运行此脚本: https://wkhtmltopdf.org/downloads.html"
    exit 1
}

# 创建临时目录用于处理文件
$tempDir = ".\temp_pdf_build"
if (!(Test-Path -Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
}

# 合并文件
Write-Host "合并Markdown文件..."
$filesToMerge = @()
$filesToMerge += $coverPageFile

# 添加指定顺序的文件
foreach ($file in $fileOrder) {
    $filePath = Join-Path -Path $chaptersPath -ChildPath $file
    if (Test-Path $filePath) {
        $filesToMerge += $filePath
        Write-Host "  - 添加: $file"
    }
    else {
        Write-Warning "文件未找到: $filePath"
    }
}

# 合并所有文件
$separator = "`n`n---`n`n"
$allContent = ""

foreach ($file in $filesToMerge) {
    $content = Get-Content -Path $file -Raw -Encoding UTF8
    
    # 如果不是第一个文件，添加分隔符
    if ($allContent -ne "") {
        $allContent += $separator
    }
    
    # 处理相对路径的图片引用
    $fileDir = Split-Path -Parent $file
    $content = $content -replace '!\[(.*?)\]\((?!http)(.*?)\)', ('![$1](' + $fileDir + '/$2)')
    
    $allContent += $content
}

# 将合并后的内容写入临时文件
$allContent | Out-File -FilePath $tempMergedFile -Encoding UTF8

# 生成PDF
Write-Host "生成PDF文件..."
Write-Host "执行: pandoc $tempMergedFile -o $outputFileName --toc --toc-depth=$tocDepth --pdf-engine=wkhtmltopdf"

pandoc $tempMergedFile -o $outputFileName --toc --toc-depth=$tocDepth --pdf-engine=wkhtmltopdf

# 检查是否成功生成PDF
if (Test-Path $outputFileName) {
    $fileSize = (Get-Item $outputFileName).Length / 1MB
    $fileSize = [math]::Round($fileSize, 2)
    Write-Host "PDF生成成功! 文件: $outputFileName ($fileSize MB)"
}
else {
    Write-Error "PDF生成失败"
}

# 清理临时文件
Write-Host "清理临时文件..."
Remove-Item -Path $tempMergedFile -Force
Remove-Item -Path $coverPageFile -Force
if (Test-Path -Path $tempDir) {
    Remove-Item -Path $tempDir -Recurse -Force
}

Write-Host "`n完成! PDF文件已生成: $outputFileName"
Write-Host "注意: 生成PDF需要Pandoc和wkhtmltopdf软件。如果遇到问题，请确保这两个软件已正确安装。" 
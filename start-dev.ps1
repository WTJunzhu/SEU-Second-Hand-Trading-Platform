#!/usr/bin/env powershell

# ============================================
# 东南大学校园二手交易平台 - 前端开发启动脚本
# ============================================
# 
# 使用方法：./start-dev.ps1
# 或在 PowerShell 中运行：Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#           然后：./start-dev.ps1
#

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SEU 校园二手交易平台 - 前端开发启动" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 进入项目目录
Set-Location $PSScriptRoot

# 检查 Python
Write-Host "正在检查 Python 环境..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 错误：未找到 Python 环境" -ForegroundColor Red
    Write-Host "请确保 Python 已安装并添加到 PATH" -ForegroundColor Red
    Read-Host "按 Enter 键退出"
    exit
}

Write-Host "✅ $pythonVersion" -ForegroundColor Green
Write-Host ""

# 检查依赖
Write-Host "正在检查依赖..." -ForegroundColor Yellow
$flaskCheck = pip list 2>&1 | Select-String -Pattern "Flask" -Quiet
if (-not $flaskCheck) {
    Write-Host "⚠️  缺少 Flask 依赖，正在安装..." -ForegroundColor Yellow
    pip install -r requirements.txt
}
Write-Host "✅ 依赖检查完成" -ForegroundColor Green
Write-Host ""

# 显示信息
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  📍 访问地址: http://localhost:5000" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 使用 Mock API（无需后端）：" -ForegroundColor Blue
Write-Host "   1. 打开浏览器开发者工具（F12）" -ForegroundColor Blue
Write-Host "   2. 在 Console 输入：" -ForegroundColor Blue
Write-Host "      window.USE_MOCK_API = true" -ForegroundColor Magenta
Write-Host "   3. 刷新页面：" -ForegroundColor Blue
Write-Host "      location.reload()" -ForegroundColor Magenta
Write-Host ""
Write-Host "📖 查看测试指南：" -ForegroundColor Blue
Write-Host "   打开 TESTING_GUIDE.md 了解详细的测试方法" -ForegroundColor Blue
Write-Host ""
Write-Host "⏹️  按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 启动服务器
Write-Host "正在启动 Flask 开发服务器..." -ForegroundColor Yellow
Write-Host ""

# 尝试打开浏览器
try {
    Start-Process "http://localhost:5000"
}
catch {
    Write-Host "⚠️  无法自动打开浏览器，请手动访问 http://localhost:5000" -ForegroundColor Yellow
}

# 启动 Flask
python run.py

Read-Host "按 Enter 键退出"

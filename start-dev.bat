@echo off
REM ============================================
REM 东南大学校园二手交易平台 - 前端开发启动脚本
REM ============================================
REM 
REM 功能：
REM 1. 启动 Flask 开发服务器
REM 2. 自动打开浏览器
REM 3. 显示 Mock API 提示信息
REM

echo.
echo ============================================
echo  SEU 校园二手交易平台 - 前端开发启动
echo ============================================
echo.

REM 进入项目目录
cd /d "%~dp0"

REM 检查 Python 是否安装
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python 环境
    echo 请确保 Python 已安装并添加到 PATH
    pause
    exit /b 1
)

echo ✅ Python 环境正常
echo.

REM 检查依赖
echo 正在检查依赖...
pip list | findstr Flask > nul 2>&1
if errorlevel 1 (
    echo ❌ 缺少 Flask 依赖
    echo 正在安装依赖...
    pip install -r requirements.txt
)

echo ✅ 依赖检查完成
echo.

REM 启动 Flask
echo 正在启动 Flask 开发服务器...
echo.
echo ============================================
echo  📍 访问地址: http://localhost:5000
echo ============================================
echo.
echo 💡 使用 Mock API（无需后端）：
echo    1. 打开浏览器开发者工具（F12）
echo    2. 在 Console 输入：window.USE_MOCK_API = true
echo    3. 刷新页面：location.reload()
echo.
echo ⏹️  按 Ctrl+C 停止服务器
echo ============================================
echo.

REM 启动服务器（自动打开浏览器）
start http://localhost:5000
python run.py

pause

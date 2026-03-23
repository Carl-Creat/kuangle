@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo  启动中...
echo.

:: 检查 Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先运行 "一键安装旷了吗.bat"
    pause
    exit /b 1
)

:: 确保数据目录存在
if not exist "data" mkdir data
if not exist "logs" mkdir logs

:: 启动 Flask
echo  正在启动服务...
start "" "http://localhost:5000"
python app.py

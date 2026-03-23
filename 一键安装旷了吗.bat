@echo off
chcp 65001 >nul
echo.
echo  ╔══════════════════════════════════════════════════════╗
echo  ║                                                      ║
echo  ║              📚 旷了吗 - 学生安全签到工具              ║
echo  ║              一键安装程序 v1.0                       ║
echo  ║                                                      ║
echo  ╚══════════════════════════════════════════════════════╝
echo.

:: 检查 Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.9+
    echo.
    echo 请访问 https://www.python.org/downloads/ 下载安装
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

python --version >nul 2>&1
if %errorlevel% neq 0 (
    where py >nul 2>&1
    if %errorlevel% neq 0 (
        echo [错误] 无法运行 Python，请确认 Python 已正确安装
        pause
        exit /b 1
    )
)

:: 检查 pip
echo [1/4] 检查 pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 正在安装 pip...
    python -m ensurepip --default-pip
)

:: 安装依赖
echo [2/4] 安装依赖包（首次可能需要 1-3 分钟）...
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败，请检查网络连接后重试
    pause
    exit /b 1
)

:: 创建数据目录
echo [3/4] 初始化数据目录...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups

:: 初始化数据库
echo [4/4] 初始化数据库...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('[OK] 数据库初始化完成')" 2>nul

echo.
echo ═══════════════════════════════════════════════════════
echo.
echo  ✅ 安装完成！
echo.
echo  现在可以启动程序了：
echo.
echo      双击 启动旷了吗.bat
echo.
echo  或在命令行运行：
echo      python app.py
echo.
echo  启动后访问: http://localhost:5000
echo.
echo ═══════════════════════════════════════════════════════
echo.
echo  📌 首次使用请先注册账号（选"学生"角色）
echo  📌 注册后将你的用户名告诉家长，让家长注册"家长"账号
echo  📌 在学生端绑定家长后即可使用
echo.
pause

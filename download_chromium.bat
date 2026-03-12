@echo off
chcp 65001 >nul
echo ============================================
echo   下载 Playwright Chromium 到当前目录
echo ============================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.9+
    pause & exit /b 1
)

:: 安装 playwright
echo [1/2] 安装 playwright...
pip install playwright -q

:: 设置下载目录为当前目录下的 chromium 文件夹
set PLAYWRIGHT_BROWSERS_PATH=%~dp0chromium

echo [2/2] 下载 Chromium 到 %PLAYWRIGHT_BROWSERS_PATH% ...
playwright install chromium

echo.
echo ============================================
echo   完成！Chromium 已下载到:
echo   %~dp0chromium
echo.
echo   使用方式：
echo   将 chromium\ 文件夹与 run_tests.exe 放在同一目录
echo   运行前设置环境变量：
echo   set PLAYWRIGHT_BROWSERS_PATH=%~dp0chromium
echo ============================================
echo.
pause

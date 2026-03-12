@echo off
chcp 65001 >nul
echo ============================================
echo   Windows 自动化测试 - 打包为 exe
echo ============================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.9+
    pause & exit /b 1
)

:: 安装依赖
echo [1/4] 安装依赖...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause & exit /b 1
)

:: 安装 playwright 浏览器
echo [2/4] 安装 Playwright Chromium...
playwright install chromium
if errorlevel 1 (
    echo [警告] Playwright 浏览器安装失败，浏览器测试将无法运行
)

:: 安装 PyInstaller
echo [3/4] 安装 PyInstaller...
pip install pyinstaller -q

:: 清理旧的构建产物
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

:: 打包
echo [4/4] 打包中，请稍候...
pyinstaller run_tests.spec
if errorlevel 1 (
    echo.
    echo [错误] 打包失败，请查看上方错误信息
    pause & exit /b 1
)

:: 复制配置文件到 dist
echo.
echo 复制配置文件...
copy config.ini dist\config.ini >nul
echo.

echo ============================================
echo   打包成功！
echo.
echo   交付物位于: dist\
echo     run_tests.exe   -- 双击运行全部测试
echo     config.ini      -- 修改应用路径和素材路径
echo.
echo   使用说明：
echo     1. 将 dist\ 整个文件夹复制到目标 Windows 机器
echo     2. 编辑 config.ini，填写正确的应用路径
echo     3. 双击 run_tests.exe 开始测试
echo     4. 测试完成后查看 output\ 目录的报告和截图
echo ============================================
echo.
pause

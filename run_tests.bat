@echo off
cd /d "%~dp0"
echo ====================================
echo  Windows 自动化测试执行
echo ====================================

set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set REPORT=reports\report_%TIMESTAMP%.html

:: 创建报告目录
if not exist reports mkdir reports

:: 根据参数执行不同测试
if "%1"=="" (
    echo 执行全部测试...
    pytest --html=%REPORT% --self-contained-html
) else if "%1"=="window" (
    echo 执行窗口操作测试...
    pytest -m window --html=%REPORT% --self-contained-html
) else if "%1"=="player" (
    echo 执行本地播放器测试...
    pytest -m player --html=%REPORT% --self-contained-html
) else if "%1"=="browser" (
    echo 执行浏览器视频测试...
    pytest -m browser --html=%REPORT% --self-contained-html
) else if "%1"=="office" (
    echo 执行办公应用测试...
    pytest -m office --html=%REPORT% --self-contained-html
) else (
    echo 未知参数: %1
    echo 用法: run_tests.bat [window^|player^|browser^|office]
)

echo.
echo 报告已保存: %REPORT%
pause

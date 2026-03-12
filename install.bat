@echo off
echo ====================================
echo  Windows 自动化测试环境安装
echo ====================================

:: 安装 Python 依赖
pip install -r requirements.txt

:: 安装 Playwright 浏览器
playwright install chromium

echo.
echo 安装完成！
echo.
echo 运行方式：
echo   全部测试:          pytest
echo   仅窗口操作:        pytest -m window
echo   仅本地播放器:      pytest -m player
echo   仅浏览器视频:      pytest -m browser
echo   仅办公应用:        pytest -m office
echo   生成 HTML 报告:    pytest --html=reports/report.html
echo.
pause

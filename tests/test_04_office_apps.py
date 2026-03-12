"""
测试用例 04：办公应用测试
- WPS 文字：打开文档、编辑、滚动、保存
- WPS 表格：打开 Excel、滚动、切换 Sheet
- WPS 演示：打开 PPT、翻页
- 和彩云：启动、登录入口、文件列表浏览
"""
import os
import time
import pytest

from scripts.windows_automator import WindowsAutomator
from config.settings import SETTINGS


@pytest.mark.office
class TestWPS:

    def test_wps_writer_open_doc(self, automator: WindowsAutomator):
        """WPS 文字：打开 docx 文档"""
        exe = SETTINGS.apps["wps"]
        doc = SETTINGS.test_doc_word

        if not os.path.exists(exe):
            pytest.skip(f"WPS 未安装: {exe}")
        if not os.path.exists(doc):
            pytest.skip(f"测试文档不存在: {doc}")

        automator.launch_app_with_file(exe, doc, wait=SETTINGS.launch_wait)
        automator.screenshot("wps_writer_opened")

        automator.wait(2.0, "等待文档完全加载")
        automator.screenshot("wps_writer_loaded")

        # 最大化
        automator.maximize()
        automator.screenshot("wps_writer_maximized")

        # 向下滚动浏览文档
        automator.scroll_down(clicks=8)
        automator.wait(0.5)
        automator.screenshot("wps_writer_scrolled_down")

        automator.scroll_up(clicks=8)
        automator.wait(0.5)
        automator.screenshot("wps_writer_scrolled_up")

    def test_wps_writer_edit_and_save(self, automator: WindowsAutomator):
        """WPS 文字：编辑内容并保存"""
        # 在文档末尾追加文字
        automator.hotkey("ctrl", "end")  # 跳到末尾
        automator.wait(0.3)
        automator.press_key("enter")
        automator.type_text("自动化测试追加内容 - " + time.strftime("%Y%m%d %H:%M:%S"))
        automator.wait(0.5)
        automator.screenshot("wps_writer_edited")

        # 保存
        automator.hotkey("ctrl", "s")
        automator.wait(1.0)
        automator.screenshot("wps_writer_saved")

        # 关闭
        automator.hotkey("ctrl", "w")
        automator.wait(1.0)

    def test_wps_excel_open(self, automator: WindowsAutomator):
        """WPS 表格：打开 xlsx 文件"""
        exe = SETTINGS.apps["et"]
        doc = SETTINGS.test_doc_excel

        if not os.path.exists(exe):
            pytest.skip(f"WPS 表格未安装: {exe}")
        if not os.path.exists(doc):
            pytest.skip(f"测试 Excel 不存在: {doc}")

        automator.launch_app_with_file(exe, doc, wait=SETTINGS.launch_wait)
        automator.wait(2.0, "等待表格加载")
        automator.maximize()
        automator.screenshot("wps_excel_opened")

        # 滚动表格
        automator.scroll_down(clicks=5)
        automator.wait(0.5)
        automator.screenshot("wps_excel_scrolled_down")

        automator.scroll_right = lambda: automator.hotkey("ctrl", "right")
        automator.hotkey("ctrl", "end")   # 跳到最后一个有内容的单元格
        automator.wait(0.3)
        automator.screenshot("wps_excel_last_cell")

        automator.hotkey("ctrl", "home")  # 回到 A1
        automator.wait(0.3)
        automator.screenshot("wps_excel_home")

        # 关闭
        automator.hotkey("ctrl", "w")
        automator.wait(1.0)

    def test_wps_ppt_open_and_present(self, automator: WindowsAutomator):
        """WPS 演示：打开 PPT 并翻页"""
        exe = SETTINGS.apps["wpp"]
        doc = SETTINGS.test_doc_ppt

        if not os.path.exists(exe):
            pytest.skip(f"WPS 演示未安装: {exe}")
        if not os.path.exists(doc):
            pytest.skip(f"测试 PPT 不存在: {doc}")

        automator.launch_app_with_file(exe, doc, wait=SETTINGS.launch_wait)
        automator.wait(2.0, "等待 PPT 加载")
        automator.maximize()
        automator.screenshot("wps_ppt_opened")

        # 启动幻灯片放映（F5）
        automator.press_key("f5")
        automator.wait(2.0)
        automator.screenshot("wps_ppt_presenting")

        # 翻页（空格键或右方向键）
        for i in range(5):
            automator.press_key("space")
            automator.wait(0.8)
            automator.screenshot(f"wps_ppt_slide_{i+2}")

        # 退出放映
        automator.press_key("esc")
        automator.wait(1.0)
        automator.screenshot("wps_ppt_exit_present")

        # 关闭
        automator.hotkey("ctrl", "w")
        automator.wait(1.0)

    def test_wps_create_new_document(self, automator: WindowsAutomator):
        """WPS 文字：新建文档并输入内容"""
        exe = SETTINGS.apps["wps"]
        if not os.path.exists(exe):
            pytest.skip(f"WPS 未安装: {exe}")

        automator.launch_app(exe, wait=SETTINGS.launch_wait)
        automator.wait(2.0)
        automator.maximize()

        # 新建空白文档
        automator.hotkey("ctrl", "n")
        automator.wait(1.0)
        automator.screenshot("wps_new_doc")

        # 输入测试内容
        automator.type_text("Windows 自动化测试\n")
        automator.type_text("测试时间：" + time.strftime("%Y年%m月%d日 %H:%M:%S") + "\n")
        automator.type_text("这是一份由自动化脚本创建的测试文档。\n")
        automator.type_text("用于验证 WPS 办公软件的基本功能。\n")
        automator.screenshot("wps_new_doc_typed")

        # 关闭不保存
        automator.hotkey("ctrl", "w")
        automator.wait(1.0)
        automator.press_key("n")  # 不保存
        automator.wait(1.0)


@pytest.mark.office
class TestCaiyun:
    """和彩云办公应用测试"""

    def test_caiyun_launch(self, automator: WindowsAutomator):
        """启动和彩云应用"""
        exe = SETTINGS.apps["caiyun"]
        if not os.path.exists(exe):
            pytest.skip(f"和彩云未安装: {exe}")

        automator.launch_app(exe, wait=SETTINGS.launch_wait)
        automator.wait(3.0, "等待和彩云启动")
        automator.screenshot("caiyun_launched")

        automator.maximize()
        automator.screenshot("caiyun_maximized")

    def test_caiyun_ui_operations(self, automator: WindowsAutomator):
        """和彩云：基础 UI 操作（滚动、点击）"""
        exe = SETTINGS.apps["caiyun"]
        if not os.path.exists(exe):
            pytest.skip(f"和彩云未安装: {exe}")

        # 如果前一个测试已启动则直接操作
        try:
            automator.connect_app(title_re=".*彩云.*")
        except Exception:
            automator.launch_app(exe, wait=SETTINGS.launch_wait)
            automator.wait(3.0)

        automator.screenshot("caiyun_ui")

        # 滚动文件列表
        automator.scroll_down(clicks=3)
        automator.wait(0.5)
        automator.screenshot("caiyun_scrolled")

        # 最小化再还原
        automator.minimize()
        automator.wait(1.0)
        automator.restore()
        automator.wait(1.0)
        automator.screenshot("caiyun_restored")

        # 关闭
        automator.hotkey("alt", "f4")
        automator.wait(1.0)

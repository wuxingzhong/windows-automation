"""
测试用例 01：基础窗口操作
- 启动程序
- 最大化 / 最小化 / 还原
- 调整窗口大小
- 移动窗口
- 页面滚动
- 窗口拖拽滑动
"""
import time
import pytest

from scripts.windows_automator import WindowsAutomator
from config.settings import SETTINGS


@pytest.mark.window
class TestWindowOperations:

    def test_launch_and_maximize(self, automator: WindowsAutomator):
        """启动记事本并最大化"""
        automator.launch_app("notepad.exe", wait=2.0)
        automator.screenshot("notepad_launched")

        automator.maximize()
        automator.screenshot("notepad_maximized")
        automator.wait(1.0)

    def test_minimize_and_restore(self, automator: WindowsAutomator):
        """最小化再还原窗口"""
        automator.minimize()
        automator.screenshot("notepad_minimized")
        automator.wait(1.0)

        automator.restore()
        automator.screenshot("notepad_restored")
        automator.wait(1.0)

    def test_resize_window(self, automator: WindowsAutomator):
        """调整窗口为 800x600"""
        automator.restore()
        automator.resize_window(800, 600)
        automator.screenshot("notepad_resized_800x600")
        automator.wait(1.0)

        automator.resize_window(1024, 768)
        automator.screenshot("notepad_resized_1024x768")
        automator.wait(1.0)

    def test_move_window(self, automator: WindowsAutomator):
        """移动窗口位置"""
        automator.move_window(100, 100)
        automator.screenshot("notepad_moved_100_100")
        automator.wait(1.0)

        automator.move_window(400, 200)
        automator.screenshot("notepad_moved_400_200")
        automator.wait(1.0)

    def test_type_and_scroll(self, automator: WindowsAutomator):
        """在记事本中输入文字并滚动"""
        automator.maximize()
        automator.click(600, 400)  # 点击编辑区域
        automator.wait(0.3)

        # 输入多行文字制造可滚动内容
        for i in range(30):
            automator.type_text(f"第 {i+1} 行测试内容 - Windows 自动化测试\n")

        automator.screenshot("notepad_content_typed")
        automator.wait(0.5)

        # 向上滚动
        automator.scroll_up(clicks=5)
        automator.screenshot("scrolled_up")
        automator.wait(0.5)

        # 向下滚动
        automator.scroll_down(clicks=5)
        automator.screenshot("scrolled_down")
        automator.wait(0.5)

    def test_hotkeys(self, automator: WindowsAutomator):
        """测试常用快捷键"""
        # Ctrl+A 全选
        automator.hotkey("ctrl", "a")
        automator.wait(0.3)
        automator.screenshot("select_all")

        # Ctrl+C 复制
        automator.hotkey("ctrl", "c")
        automator.wait(0.3)

        # End 跳到末尾，Ctrl+V 粘贴
        automator.press_key("end")
        automator.hotkey("ctrl", "v")
        automator.wait(0.3)
        automator.screenshot("pasted")

    def test_close_notepad(self, automator: WindowsAutomator):
        """关闭记事本（不保存）"""
        automator.hotkey("alt", "f4")
        automator.wait(1.0)
        # 弹出是否保存对话框时，按 N 不保存
        automator.press_key("n")
        automator.wait(1.0)
        automator.screenshot("notepad_closed")

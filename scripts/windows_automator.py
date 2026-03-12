"""
Windows 桌面自动化核心工具类
封装 pywinauto + PyAutoGUI，提供统一操作接口
"""
import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Optional

import pyautogui
from pywinauto import Application, Desktop
from pywinauto.findwindows import ElementNotFoundError

logger = logging.getLogger(__name__)

# 全局安全设置：鼠标移到角落可中断脚本
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


class WindowsAutomator:
    """Windows 桌面应用自动化操作类"""

    def __init__(self, screenshot_dir: str = r"D:\test_reports\screenshots") -> None:
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self._app: Optional[Application] = None

    # -------------------------------------------------------------------------
    # 应用启动与连接
    # -------------------------------------------------------------------------

    def launch_app(self, exe_path: str, wait: float = 3.0) -> Application:
        """启动桌面应用并返回 Application 对象"""
        logger.info(f"启动应用: {exe_path}")
        self._app = Application(backend="uia").start(exe_path)
        time.sleep(wait)
        return self._app

    def launch_app_with_file(self, exe_path: str, file_path: str, wait: float = 3.0) -> Application:
        """用指定文件启动应用（如用播放器打开视频）"""
        logger.info(f"启动应用: {exe_path}，打开文件: {file_path}")
        self._app = Application(backend="uia").start(f'"{exe_path}" "{file_path}"')
        time.sleep(wait)
        return self._app

    def open_with_default_app(self, file_path: str, wait: float = 3.0) -> None:
        """用系统默认程序打开文件"""
        logger.info(f"用默认程序打开: {file_path}")
        os.startfile(file_path)
        time.sleep(wait)

    def connect_app(self, title_re: str = None, process: int = None) -> Application:
        """连接到已运行的应用"""
        kwargs = {"backend": "uia"}
        if title_re:
            kwargs["title_re"] = title_re
        if process:
            kwargs["process"] = process
        self._app = Application(**kwargs).connect()
        return self._app

    # -------------------------------------------------------------------------
    # 窗口操作
    # -------------------------------------------------------------------------

    def get_window(self, title_re: Optional[str] = None):
        """获取窗口（默认取最顶层窗口）"""
        if self._app is None:
            raise RuntimeError("请先调用 launch_app() 或 connect_app()")
        if title_re:
            return self._app.window(title_re=title_re)
        return self._app.top_window()

    def maximize(self, title_re: Optional[str] = None) -> None:
        """最大化窗口"""
        win = self.get_window(title_re)
        win.maximize()
        logger.info("窗口最大化")
        time.sleep(0.5)

    def minimize(self, title_re: Optional[str] = None) -> None:
        """最小化窗口"""
        win = self.get_window(title_re)
        win.minimize()
        logger.info("窗口最小化")
        time.sleep(0.5)

    def restore(self, title_re: Optional[str] = None) -> None:
        """还原窗口"""
        win = self.get_window(title_re)
        win.restore()
        logger.info("窗口还原")
        time.sleep(0.5)

    def close_window(self, title_re: Optional[str] = None) -> None:
        """关闭窗口"""
        win = self.get_window(title_re)
        win.close()
        logger.info("窗口关闭")
        time.sleep(0.5)

    def resize_window(self, width: int, height: int, title_re: Optional[str] = None) -> None:
        """调整窗口大小"""
        win = self.get_window(title_re)
        win.restore()
        win.resize_client(width, height)
        logger.info(f"窗口调整为 {width}x{height}")
        time.sleep(0.5)

    def move_window(self, x: int, y: int, title_re: Optional[str] = None) -> None:
        """移动窗口位置"""
        win = self.get_window(title_re)
        rect = win.rectangle()
        w = rect.width()
        h = rect.height()
        win.move_window(x=x, y=y, width=w, height=h)
        logger.info(f"窗口移动到 ({x}, {y})")
        time.sleep(0.5)

    # -------------------------------------------------------------------------
    # 鼠标操作
    # -------------------------------------------------------------------------

    def click(self, x: int, y: int) -> None:
        """鼠标左键单击坐标"""
        pyautogui.click(x, y)
        logger.info(f"点击坐标 ({x}, {y})")

    def double_click(self, x: int, y: int) -> None:
        """鼠标双击坐标"""
        pyautogui.doubleClick(x, y)
        logger.info(f"双击坐标 ({x}, {y})")

    def right_click(self, x: int, y: int) -> None:
        """鼠标右键单击"""
        pyautogui.rightClick(x, y)
        logger.info(f"右键点击 ({x}, {y})")

    def scroll_up(self, clicks: int = 5, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """向上滚动"""
        if x and y:
            pyautogui.moveTo(x, y)
        pyautogui.scroll(clicks)
        logger.info(f"向上滚动 {clicks} 格")

    def scroll_down(self, clicks: int = 5, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """向下滚动"""
        if x and y:
            pyautogui.moveTo(x, y)
        pyautogui.scroll(-clicks)
        logger.info(f"向下滚动 {clicks} 格")

    def drag(self, from_x: int, from_y: int, to_x: int, to_y: int, duration: float = 1.0) -> None:
        """拖拽（窗口滑动）"""
        pyautogui.drag(from_x, from_y, to_x - from_x, to_y - from_y, duration=duration)
        logger.info(f"拖拽 ({from_x},{from_y}) -> ({to_x},{to_y})")

    def swipe_window(self, direction: str = "left", distance: int = 300, duration: float = 0.8) -> None:
        """窗口滑动（left/right/up/down）"""
        x, y = pyautogui.position()
        screen_w, screen_h = pyautogui.size()
        cx, cy = screen_w // 2, screen_h // 2

        offsets = {
            "left":  (-distance, 0),
            "right": (distance, 0),
            "up":    (0, -distance),
            "down":  (0, distance),
        }
        dx, dy = offsets.get(direction, (0, 0))
        pyautogui.drag(cx, cy, dx, dy, duration=duration, button="left")
        logger.info(f"窗口向 {direction} 滑动 {distance}px")

    # -------------------------------------------------------------------------
    # 键盘操作
    # -------------------------------------------------------------------------

    def type_text(self, text: str, interval: float = 0.05) -> None:
        """输入文本"""
        pyautogui.typewrite(text, interval=interval)
        logger.info(f"输入文本: {text}")

    def press_key(self, key: str) -> None:
        """按键（如 'enter', 'esc', 'f11'）"""
        pyautogui.press(key)
        logger.info(f"按键: {key}")

    def hotkey(self, *keys: str) -> None:
        """组合键（如 'ctrl', 'w'）"""
        pyautogui.hotkey(*keys)
        logger.info(f"组合键: {'+'.join(keys)}")

    # -------------------------------------------------------------------------
    # 截图
    # -------------------------------------------------------------------------

    def screenshot(self, name: str = "") -> Path:
        """截图并保存"""
        ts = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{ts}.png" if name else f"screenshot_{ts}.png"
        path = self.screenshot_dir / filename
        pyautogui.screenshot(str(path))
        logger.info(f"截图保存: {path}")
        return path

    # -------------------------------------------------------------------------
    # 等待
    # -------------------------------------------------------------------------

    def wait(self, seconds: float, reason: str = "") -> None:
        """等待（可附加说明，便于日志追踪）"""
        msg = f"等待 {seconds}s" + (f"（{reason}）" if reason else "")
        logger.info(msg)
        time.sleep(seconds)

    def wait_for_window(self, title_re: str, timeout: int = 30) -> bool:
        """等待指定窗口出现"""
        logger.info(f"等待窗口出现: {title_re}")
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                Desktop(backend="uia").window(title_re=title_re).wait("visible", timeout=2)
                logger.info(f"窗口已出现: {title_re}")
                return True
            except Exception:
                time.sleep(1)
        logger.warning(f"等待窗口超时: {title_re}")
        return False

    # -------------------------------------------------------------------------
    # 进程管理
    # -------------------------------------------------------------------------

    def kill_process(self, process_name: str) -> None:
        """强制结束进程（如 chrome.exe）"""
        subprocess.run(["taskkill", "/f", "/im", process_name], capture_output=True)
        logger.info(f"结束进程: {process_name}")
        time.sleep(1)

    def is_process_running(self, process_name: str) -> bool:
        """检查进程是否在运行"""
        result = subprocess.run(
            ["tasklist", "/fi", f"imagename eq {process_name}"],
            capture_output=True, text=True
        )
        return process_name.lower() in result.stdout.lower()

"""
测试用例 03：浏览器在线视频播放
- Chrome 打开腾讯视频、爱奇艺、B站
- 页面滚动、视频点击播放
- 全屏操作
"""
import time
import pytest
from playwright.sync_api import sync_playwright, Page, Browser

from scripts.windows_automator import WindowsAutomator
from config.settings import SETTINGS


# ---------------------------------------------------------------------------
# Chrome 测试（Playwright 控制）
# ---------------------------------------------------------------------------

@pytest.mark.browser
class TestChromeOnlineVideo:

    @pytest.fixture(scope="class")
    def browser_page(self):
        """启动 Chrome 并创建页面"""
        with sync_playwright() as p:
            # 优先使用配置文件中的 Chrome 路径
            chrome_path = SETTINGS.apps.get("chrome", "")

            try:
                if chrome_path and chrome_path.endswith("chrome.exe"):
                    # 使用配置的 Chrome 可执行文件
                    browser = p.chromium.launch(
                        headless=False,
                        executable_path=chrome_path,
                        args=["--start-maximized"],
                    )
                else:
                    # 尝试使用系统 Chrome
                    browser = p.chromium.launch(
                        headless=False,
                        channel="chrome",
                        args=["--start-maximized"],
                    )
            except Exception:
                # 最后尝试使用 Playwright 自带的 Chromium
                browser = p.chromium.launch(
                    headless=False,
                    args=["--start-maximized"],
                )

            context = browser.new_context(no_viewport=True)
            page = context.new_page()
            yield page
            browser.close()

    def _goto_and_screenshot(
        self,
        page: Page,
        url: str,
        automator: WindowsAutomator,
        name: str,
        wait: float = 5.0,
    ) -> None:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(int(wait * 1000))
        automator.screenshot(name)

    def test_qqvideo_homepage(self, browser_page: Page, automator: WindowsAutomator):
        """打开腾讯视频首页"""
        self._goto_and_screenshot(
            browser_page, SETTINGS.urls["qqvideo"], automator, "qqvideo_homepage"
        )

        # 滚动浏览
        for _ in range(3):
            browser_page.keyboard.press("PageDown")
            browser_page.wait_for_timeout(800)
        automator.screenshot("qqvideo_scrolled")

    def test_qqvideo_play_video(self, browser_page: Page, automator: WindowsAutomator):
        """腾讯视频：点击视频并播放"""
        self._goto_and_screenshot(
            browser_page, SETTINGS.urls["qqvideo"], automator, "qqvideo_before_play"
        )

        try:
            browser_page.locator(".result_item, .cover-small, a.item").first.click(timeout=5000)
        except Exception:
            browser_page.goto("https://v.qq.com/x/cover/mzc00200mp2zo4y/v0043ri2gje.html")

        browser_page.wait_for_timeout(5000)
        automator.screenshot("qqvideo_video_page")

        # 录屏观察
        automator.wait(SETTINGS.video_play_wait, "录屏观察腾讯视频在线播放")
        automator.screenshot("qqvideo_after_10s")

    def test_bilibili_homepage(self, browser_page: Page, automator: WindowsAutomator):
        """B站首页浏览（仅浏览，不点击视频）"""
        self._goto_and_screenshot(
            browser_page, SETTINGS.urls["bilibili"], automator, "bilibili_homepage"
        )

        # 滚动浏览
        for _ in range(3):
            browser_page.keyboard.press("PageDown")
            browser_page.wait_for_timeout(800)
        automator.screenshot("bilibili_scrolled")

        # 回到顶部
        browser_page.keyboard.press("Home")
        browser_page.wait_for_timeout(500)
        automator.screenshot("bilibili_back_to_top")

    def test_page_scroll_operations(self, browser_page: Page, automator: WindowsAutomator):
        """页面滚动操作专项测试"""
        browser_page.goto(SETTINGS.urls["iqiyi"], wait_until="domcontentloaded")
        browser_page.wait_for_timeout(3000)
        automator.screenshot("iqiyi_homepage")

        # 多种滚动方式
        browser_page.mouse.wheel(0, 500)   # 鼠标滚轮向下
        browser_page.wait_for_timeout(500)
        automator.screenshot("iqiyi_scroll_wheel_down")

        browser_page.mouse.wheel(0, -500)  # 鼠标滚轮向上
        browser_page.wait_for_timeout(500)
        automator.screenshot("iqiyi_scroll_wheel_up")

        browser_page.keyboard.press("End")  # 直接跳到底部
        browser_page.wait_for_timeout(1000)
        automator.screenshot("iqiyi_scroll_end")

        browser_page.keyboard.press("Home")  # 回到顶部
        browser_page.wait_for_timeout(500)
        automator.screenshot("iqiyi_scroll_home")



"""
测试用例 02：本地播放器播放视频
- 用系统默认播放器打开 720P 视频
- 用腾讯视频客户端打开视频
- 播放控制：全屏、暂停、恢复、快进、音量调节
"""
import os
import time
import pytest

from scripts.windows_automator import WindowsAutomator
from config.settings import SETTINGS


@pytest.mark.player
class TestLocalPlayer:

    def test_open_video_default_player(self, automator: WindowsAutomator):
        """用系统默认播放器打开 720P 视频（录屏验证播放效果）"""
        video_path = SETTINGS.test_video_720p
        assert os.path.exists(video_path), f"测试视频不存在: {video_path}"

        automator.open_with_default_app(video_path, wait=SETTINGS.launch_wait)
        automator.screenshot("default_player_opened")

        # 等待播放器完全加载
        automator.wait(3.0, "等待播放器加载")
        automator.screenshot("default_player_playing")

        # 全屏播放（F 键或 Enter，各播放器不同）
        automator.press_key("f")
        automator.wait(1.0)
        automator.screenshot("default_player_fullscreen")

        # 录屏观察 10 秒
        automator.wait(SETTINGS.video_play_wait, "录屏观察视频播放")
        automator.screenshot("default_player_after_10s")

        # 退出全屏
        automator.press_key("esc")
        automator.wait(1.0)

        # 关闭播放器
        automator.hotkey("alt", "f4")
        automator.wait(1.0)

    def test_qqvideo_player(self, automator: WindowsAutomator):
        """腾讯视频客户端播放本地视频"""
        exe = SETTINGS.apps["qqvideo"]
        video = SETTINGS.test_video_720p

        if not os.path.exists(exe):
            pytest.skip(f"腾讯视频未安装: {exe}")
        if not os.path.exists(video):
            pytest.skip(f"测试视频不存在: {video}")

        automator.launch_app_with_file(exe, video, wait=SETTINGS.launch_wait)
        automator.screenshot("qqvideo_opened")

        automator.wait(3.0, "等待腾讯视频加载")
        automator.screenshot("qqvideo_playing")

        # 全屏（腾讯视频用双击或 Alt+Enter）
        screen_w, screen_h = 1920, 1080  # 根据实际分辨率
        automator.double_click(screen_w // 2, screen_h // 2)
        automator.wait(1.0)
        automator.screenshot("qqvideo_fullscreen")

        # 录屏观察
        automator.wait(SETTINGS.video_play_wait, "录屏观察腾讯视频播放")
        automator.screenshot("qqvideo_after_10s")

        # 暂停（空格键）
        automator.press_key("space")
        automator.wait(1.0)
        automator.screenshot("qqvideo_paused")

        # 恢复播放
        automator.press_key("space")
        automator.wait(1.0)
        automator.screenshot("qqvideo_resumed")

        # 快进（右方向键）
        automator.press_key("right")
        automator.wait(1.0)
        automator.screenshot("qqvideo_fast_forward")

        # 音量调节（上/下方向键）
        automator.press_key("up")
        automator.wait(0.5)
        automator.press_key("up")
        automator.wait(0.5)
        automator.screenshot("qqvideo_volume_up")

        # 退出全屏后关闭
        automator.press_key("esc")
        automator.wait(0.5)
        automator.hotkey("alt", "f4")
        automator.wait(1.0)

    def test_window_operations_during_playback(self, automator: WindowsAutomator):
        """播放过程中对窗口进行操作（窗口化、大小化）"""
        video = SETTINGS.test_video_720p
        if not os.path.exists(video):
            pytest.skip(f"测试视频不存在: {video}")

        automator.open_with_default_app(video, wait=SETTINGS.launch_wait)
        automator.wait(3.0, "等待播放器加载")
        automator.screenshot("player_normal")

        # 最大化
        automator.maximize()
        automator.screenshot("player_maximized")
        automator.wait(2.0)

        # 还原
        automator.restore()
        automator.screenshot("player_restored")
        automator.wait(2.0)

        # 调整大小
        automator.resize_window(960, 540)
        automator.screenshot("player_resized_960x540")
        automator.wait(2.0)

        # 最小化
        automator.minimize()
        automator.wait(1.0)
        automator.restore()
        automator.screenshot("player_after_minimize_restore")
        automator.wait(1.0)

        automator.hotkey("alt", "f4")
        automator.wait(1.0)

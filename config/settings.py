# Windows 自动化测试配置
# 优先从 exe 同级目录的 config.ini 读取，找不到则使用默认值
import configparser
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path


def _get_base_dir() -> Path:
    """获取 exe 或脚本所在目录（兼容 PyInstaller 打包和直接运行）"""
    if getattr(sys, "frozen", False):
        # PyInstaller 打包后，exe 所在目录
        return Path(sys.executable).parent
    # 直接运行时，项目根目录
    return Path(__file__).parent.parent


def _load_ini(base_dir: Path) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    ini_path = base_dir / "config.ini"
    if ini_path.exists():
        cfg.read(ini_path, encoding="utf-8")
    return cfg


def _get(cfg: configparser.ConfigParser, section: str, key: str, fallback: str) -> str:
    return cfg.get(section, key, fallback=fallback)


BASE_DIR = _get_base_dir()
_cfg = _load_ini(BASE_DIR)


@dataclass(frozen=True)
class Settings:
    # 应用路径
    apps: dict = field(default_factory=lambda: {
        "wps":     _get(_cfg, "apps", "wps",     r"C:\Program Files\WPS Office\office6\wps.exe"),
        "wpp":     _get(_cfg, "apps", "wpp",     r"C:\Program Files\WPS Office\office6\wpp.exe"),
        "et":      _get(_cfg, "apps", "et",      r"C:\Program Files\WPS Office\office6\et.exe"),
        "qqvideo": _get(_cfg, "apps", "qqvideo", r"C:\Program Files (x86)\Tencent\QQlive\QQlive.exe"),
        "chrome":  _get(_cfg, "apps", "chrome",  r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        "ie":      _get(_cfg, "apps", "ie",      r"C:\Program Files\Internet Explorer\iexplore.exe"),
        "caiyun":  _get(_cfg, "apps", "caiyun",  r"C:\Program Files\ChinaMobile\HeyCloud\HeyCloud.exe"),
    })

    # 测试素材路径
    test_video_720p:  str = field(default_factory=lambda: _get(_cfg, "media", "test_video_720p",  r"D:\test_videos\test_720p.mp4"))
    test_video_1080p: str = field(default_factory=lambda: _get(_cfg, "media", "test_video_1080p", r"D:\test_videos\test_1080p.mp4"))
    test_doc_word:    str = field(default_factory=lambda: _get(_cfg, "media", "test_doc_word",    r"D:\test_docs\test.docx"))
    test_doc_excel:   str = field(default_factory=lambda: _get(_cfg, "media", "test_doc_excel",   r"D:\test_docs\test.xlsx"))
    test_doc_ppt:     str = field(default_factory=lambda: _get(_cfg, "media", "test_doc_ppt",     r"D:\test_docs\test.pptx"))

    # 在线视频 URL
    urls: dict = field(default_factory=lambda: {
        "qqvideo":  "https://v.qq.com",
        "iqiyi":    "https://www.iqiyi.com",
        "bilibili": "https://www.bilibili.com",
    })

    # 等待时间（秒）
    launch_wait:     float = field(default_factory=lambda: float(_get(_cfg, "timing", "launch_wait",     "3.0")))
    page_load_wait:  float = field(default_factory=lambda: float(_get(_cfg, "timing", "page_load_wait",  "5.0")))
    action_wait:     float = field(default_factory=lambda: float(_get(_cfg, "timing", "action_wait",     "0.5")))
    video_play_wait: float = field(default_factory=lambda: float(_get(_cfg, "timing", "video_play_wait", "10.0")))

    # 输出目录（默认放到 exe 同级的 output 文件夹）
    screenshot_dir: str = field(default_factory=lambda: _get(
        _cfg, "output", "screenshot_dir",
        str(BASE_DIR / "output" / "screenshots")
    ))
    report_dir: str = field(default_factory=lambda: _get(
        _cfg, "output", "report_dir",
        str(BASE_DIR / "output")
    ))


SETTINGS = Settings()

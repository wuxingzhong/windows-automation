"""
Windows 应用自动探测
通过注册表、PATH 环境变量、常见安装目录三种方式查找应用路径
"""
import os
import shutil
import winreg
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# 每个应用的搜索规则
# key: config.ini 中的键名
# candidates: 常见安装路径列表（按优先级排列）
# reg_keys: 注册表路径列表，值为 exe 路径或安装目录
# path_name: PATH 中的可执行文件名
# ---------------------------------------------------------------------------
APP_RULES: dict[str, dict] = {
    "wps": {
        "candidates": [
            r"C:\Program Files\WPS Office\office6\wps.exe",
            r"C:\Program Files (x86)\WPS Office\office6\wps.exe",
            r"D:\Program Files\WPS Office\office6\wps.exe",
        ],
        "reg_keys": [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Kingsoft\WPS Office", "InstallLocation"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Kingsoft\WPS Office", "InstallLocation"),
        ],
        "reg_subpath": r"office6\wps.exe",
        "path_name": "wps.exe",
    },
    "wpp": {
        "candidates": [
            r"C:\Program Files\WPS Office\office6\wpp.exe",
            r"C:\Program Files (x86)\WPS Office\office6\wpp.exe",
        ],
        "reg_keys": [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Kingsoft\WPS Office", "InstallLocation"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Kingsoft\WPS Office", "InstallLocation"),
        ],
        "reg_subpath": r"office6\wpp.exe",
        "path_name": "wpp.exe",
    },
    "et": {
        "candidates": [
            r"C:\Program Files\WPS Office\office6\et.exe",
            r"C:\Program Files (x86)\WPS Office\office6\et.exe",
        ],
        "reg_keys": [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Kingsoft\WPS Office", "InstallLocation"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Kingsoft\WPS Office", "InstallLocation"),
        ],
        "reg_subpath": r"office6\et.exe",
        "path_name": "et.exe",
    },
    "qqvideo": {
        "candidates": [
            r"C:\Program Files (x86)\Tencent\QQlive\QQlive.exe",
            r"C:\Program Files\Tencent\QQlive\QQlive.exe",
            r"D:\Program Files\Tencent\QQlive\QQlive.exe",
            r"C:\Program Files (x86)\Tencent\QQPlayer\QQPlayer.exe",
            r"C:\Program Files\Tencent\QQPlayer\QQPlayer.exe",
            r"D:\Program Files\Tencent\QQPlayer\QQPlayer.exe",
            r"C:\Program Files (x86)\Tencent\Video\Video.exe",
            r"C:\Program Files\Tencent\Video\Video.exe",
        ],
        "reg_keys": [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Tencent\QQlive", "InstallPath"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Tencent\QQlive", "InstallPath"),
            (winreg.HKEY_CURRENT_USER,  r"SOFTWARE\Tencent\QQlive", "InstallPath"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Tencent\QQPlayer", "InstallPath"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Tencent\QQPlayer", "InstallPath"),
            (winreg.HKEY_CURRENT_USER,  r"SOFTWARE\Tencent\QQPlayer", "InstallPath"),
        ],
        "reg_subpath": "QQlive.exe",
        "path_name": "QQlive.exe",
    },
    "chrome": {
        "candidates": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        ],
        "reg_keys": [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe", ""),
            (winreg.HKEY_CURRENT_USER,  r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe", ""),
        ],
        "reg_subpath": None,
        "path_name": "chrome.exe",
    },
    "ie": {
        "candidates": [
            r"C:\Program Files\Internet Explorer\iexplore.exe",
            r"C:\Program Files (x86)\Internet Explorer\iexplore.exe",
        ],
        "reg_keys": [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\iexplore.exe", ""),
        ],
        "reg_subpath": None,
        "path_name": "iexplore.exe",
    },
    "caiyun": {
        "candidates": [
            r"C:\Program Files\ChinaMobile\HeyCloud\HeyCloud.exe",
            r"C:\Program Files (x86)\ChinaMobile\HeyCloud\HeyCloud.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\ChinaMobile\HeyCloud\HeyCloud.exe"),
        ],
        "reg_keys": [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\ChinaMobile\HeyCloud", "InstallPath"),
            (winreg.HKEY_CURRENT_USER,  r"SOFTWARE\ChinaMobile\HeyCloud", "InstallPath"),
        ],
        "reg_subpath": "HeyCloud.exe",
        "path_name": "HeyCloud.exe",
    },
}


def _find_via_registry(hive: int, subkey: str, value_name: str, subpath: Optional[str]) -> Optional[str]:
    """从注册表读取安装路径"""
    try:
        with winreg.OpenKey(hive, subkey) as key:
            val, _ = winreg.QueryValueEx(key, value_name)
            if not val:
                return None
            # 值本身就是 exe 路径
            if val.lower().endswith(".exe") and Path(val).exists():
                return val
            # 值是安装目录，拼接子路径
            if subpath:
                exe = Path(val) / subpath
                if exe.exists():
                    return str(exe)
    except (FileNotFoundError, OSError, PermissionError):
        pass
    return None


def _find_via_path(exe_name: str) -> Optional[str]:
    """从 PATH 环境变量查找"""
    result = shutil.which(exe_name)
    return result if result else None


def _find_via_candidates(candidates: list[str]) -> Optional[str]:
    """遍历常见安装路径"""
    for c in candidates:
        if c and Path(c).exists():
            return c
    return None


def find_app(key: str) -> Optional[str]:
    """
    综合三种方式查找应用路径，返回找到的第一个有效路径。
    优先级：注册表 > PATH > 常见路径
    """
    rule = APP_RULES.get(key)
    if not rule:
        return None

    # 1. 注册表
    for hive, subkey, value_name in rule.get("reg_keys", []):
        result = _find_via_registry(hive, subkey, value_name, rule.get("reg_subpath"))
        if result:
            return result

    # 2. PATH
    if rule.get("path_name"):
        result = _find_via_path(rule["path_name"])
        if result:
            return result

    # 3. 常见路径
    return _find_via_candidates(rule.get("candidates", []))


def find_all_apps() -> dict[str, Optional[str]]:
    """搜索所有应用，返回 {key: path_or_None} 字典"""
    return {key: find_app(key) for key in APP_RULES}


def print_search_result(results: dict[str, Optional[str]]) -> None:
    """打印搜索结果"""
    found = {k: v for k, v in results.items() if v}
    missing = [k for k, v in results.items() if not v]

    print(f"  找到 {len(found)}/{len(results)} 个应用：")
    for k, v in found.items():
        print(f"    ✓ {k:<10} {v}")
    if missing:
        print(f"  未找到（将跳过相关测试）：")
        for k in missing:
            print(f"    ✗ {k}")

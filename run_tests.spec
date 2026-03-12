# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 打包配置
# 运行: pyinstaller run_tests.spec

import os
from pathlib import Path

project_dir = Path(SPECPATH)
block_cipher = None

import glob
import sysconfig

# 收集所有已安装包的 dist-info（含 entry_points.txt），让 pytest 能发现插件
def collect_dist_info():
    result = []
    site_packages = sysconfig.get_paths()["purelib"]
    for dist_info in glob.glob(f"{site_packages}/*.dist-info"):
        result.append((dist_info, "."))
    return result

a = Analysis(
    [str(project_dir / 'main.py')],
    pathex=[str(project_dir)],
    binaries=[],
    datas=[
        (str(project_dir / 'tests'), 'tests'),
        *collect_dist_info(),
    ],
    hiddenimports=[
        'pytest',
        '_pytest',
        '_pytest.logging',
        '_pytest.capture',
        '_pytest.terminal',
        'pluggy',
        'pywinauto',
        'pywinauto.application',
        'pywinauto.controls',
        'pywinauto.controls.uia_controls',
        'pywinauto.controls.win32_controls',
        'pywinauto.findwindows',
        'pywinauto.keyboard',
        'pywinauto.mouse',
        'pywinauto.desktop',
        'pywinauto.base_wrapper',
        'pywinauto.win32structures',
        'pyautogui',
        'pyscreeze',
        'pymsgbox',
        'pytweening',
        'playwright',
        'playwright.sync_api',
        'playwright._impl._api_types',
        'playwright._impl._browser',
        'playwright._impl._browser_context',
        'playwright._impl._page',
        'config',
        'config.settings',
        'config.app_finder',
        'winreg',
        'scripts',
        'scripts.windows_automator',
        'tests.conftest',
        'tests.test_01_window_operations',
        'tests.test_02_local_player',
        'tests.test_03_browser_video',
        'tests.test_04_office_apps',
        'configparser',
        'dataclasses',
        'importlib',
        'shutil',
        'subprocess',
        'pathlib',
        'logging',
        'typing',
        'time',
        'os',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='run_tests',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

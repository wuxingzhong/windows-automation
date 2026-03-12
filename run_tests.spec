# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 打包配置
# 运行: pyinstaller run_tests.spec

import os
from pathlib import Path

project_dir = Path(SPECPATH)

block_cipher = None

a = Analysis(
    [str(project_dir / 'main.py')],
    pathex=[str(project_dir)],
    binaries=[],
    datas=[
        # 将 tests 目录整体打入 exe
        (str(project_dir / 'tests'), 'tests'),
        # pytest 插件需要的数据文件
    ],
    hiddenimports=[
        # pytest 及插件
        'pytest',
        'pytest_html',
        '_pytest',
        '_pytest.logging',
        '_pytest.capture',
        '_pytest.terminal',
        'pluggy',
        # pywinauto
        'pywinauto',
        'pywinauto.application',
        'pywinauto.controls',
        'pywinauto.controls.uia_controls',
        'pywinauto.controls.win32_controls',
        'pywinauto.findwindows',
        'pywinauto.keyboard',
        'pywinauto.mouse',
        # pyautogui
        'pyautogui',
        'pyscreeze',
        'pymsgbox',
        'pytweening',
        # playwright
        'playwright',
        'playwright.sync_api',
        # 项目自身模块
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
        # 标准库补充
        'configparser',
        'dataclasses',
        'subprocess',
        'pathlib',
        'logging',
        'time',
        'os',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
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
    name='run_tests',           # 生成 run_tests.exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                   # 压缩，减小体积（需安装 UPX）
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,               # 保留控制台窗口，方便查看日志
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',          # 可选：自定义图标
)

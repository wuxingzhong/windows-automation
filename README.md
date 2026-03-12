# Windows 自动化测试套件

基于 pywinauto + PyAutoGUI + Playwright 实现的 Windows 桌面自动化测试。
支持打包为单个 exe，复制到目标机器双击即运行。

## 目录结构

```
windows-automation/
├── config/
│   └── settings.py              # 配置加载逻辑（自动读取 config.ini）
├── scripts/
│   └── windows_automator.py     # 核心自动化工具类
├── tests/
│   ├── conftest.py                      # pytest fixtures
│   ├── test_01_window_operations.py     # 窗口操作测试
│   ├── test_02_local_player.py          # 本地播放器测试
│   ├── test_03_browser_video.py         # 浏览器在线视频测试
│   └── test_04_office_apps.py           # 办公应用测试
├── main.py                      # exe 入口
├── run_tests.spec               # PyInstaller 打包配置
├── config.ini                   # 用户配置文件（路径、等待时间）
├── build.bat                    # 一键打包为 exe
├── requirements.txt
└── README.md
```

---

## 方式一：直接打包成 exe（推荐）

### 打包步骤（在任意 Windows 开发机上执行一次）

```bat
build.bat
```

打包完成后，`dist\` 目录包含：

```
dist\
├── run_tests.exe    ← 双击运行全部测试
└── config.ini       ← 修改应用路径和素材路径
```

### 部署到目标机器

1. 将 `dist\` 整个文件夹复制到目标 Windows 机器
2. 编辑 `config.ini`，填写目标机器上实际的应用路径
3. 双击 `run_tests.exe`

测试完成后，`exe` 同级目录会生成 `output\` 文件夹：

```
output\
├── report_20240101_120000.html  ← HTML 测试报告（浏览器打开）
├── log_20240101_120000.txt      ← 详细日志
└── screenshots\                 ← 每步操作截图
    ├── notepad_launched_...png
    ├── wps_writer_opened_...png
    └── ...
```

---

## 方式二：直接用 Python 运行（开发调试）

```bat
pip install -r requirements.txt
playwright install chromium
pytest -v
```

---

## config.ini 配置说明

```ini
[apps]
wps     = C:\Program Files\WPS Office\office6\wps.exe
chrome  = C:\Program Files\Google\Chrome\Application\chrome.exe
# ... 根据实际安装路径修改

[media]
test_video_720p = D:\test_videos\test_720p.mp4
test_doc_word   = D:\test_docs\test.docx
# ... 测试素材路径

[timing]
launch_wait     = 3.0   # 启动等待（秒），机器慢可调大
video_play_wait = 10.0  # 视频录屏观察时间

[output]
# 留空则自动输出到 exe 同级的 output\ 目录
screenshot_dir =
report_dir     =
```

---

## 测试覆盖范围

| 模块 | 测试内容 |
|------|---------|
| test_01 窗口操作 | 启动、最大化/最小化/还原、调整大小、移动、滚动、快捷键 |
| test_02 本地播放器 | 默认播放器/腾讯视频/优酷客户端打开 720P 视频，全屏/暂停/快进 |
| test_03 浏览器视频 | Chrome 打开优酷/腾讯/爱奇艺/B站，IE 打开在线视频 |
| test_04 办公应用 | WPS 文字/表格/演示，和彩云启动与 UI 操作 |

## 注意事项

- 未安装的应用会自动 `skip`，不影响其他测试
- 鼠标移到屏幕**左上角**可立即中断脚本（PyAutoGUI FAILSAFE）
- 视频播放效果通过**录屏人工验证**，脚本负责操作，不做自动判断
- Playwright 的 Chromium 浏览器已打包进 exe，无需单独安装

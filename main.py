"""
Windows 自动化测试入口
双击 run_tests.exe 即可运行所有测试
"""
import configparser
import os
import sys
import time
from pathlib import Path


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


def setup_paths(base_dir: Path) -> None:
    for p in [str(base_dir), str(base_dir / "tests")]:
        if p not in sys.path:
            sys.path.insert(0, p)
    if getattr(sys, "frozen", False):
        meipass = Path(sys._MEIPASS)
        for p in [str(meipass), str(meipass / "tests")]:
            if p not in sys.path:
                sys.path.insert(0, p)


def auto_detect_and_update_ini(base_dir: Path) -> None:
    """自动搜索应用路径，将结果写入 config.ini（不覆盖用户已填写的值）"""
    from config.app_finder import find_all_apps, print_search_result

    print("正在自动搜索已安装的应用...")
    results = find_all_apps()
    print_search_result(results)

    ini_path = base_dir / "config.ini"
    cfg = configparser.ConfigParser()
    if ini_path.exists():
        cfg.read(ini_path, encoding="utf-8")

    if not cfg.has_section("apps"):
        cfg.add_section("apps")

    updated = []
    for key, path in results.items():
        if path:
            existing = cfg.get("apps", key, fallback="").strip()
            # 只在用户未填写、或填写的路径不存在时才更新
            if not existing or not Path(existing).exists():
                cfg.set("apps", key, path)
                updated.append(key)

    if updated:
        with open(ini_path, "w", encoding="utf-8") as f:
            cfg.write(f)
        print(f"  已自动更新 config.ini: {', '.join(updated)}")
    else:
        print("  config.ini 无需更新")
    print()


def main() -> int:
    base_dir = get_base_dir()
    setup_paths(base_dir)

    print("=" * 60)
    print("  Windows 自动化测试")
    print(f"  时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    # 自动探测应用路径并更新 config.ini
    auto_detect_and_update_ini(base_dir)

    # 重新加载配置（拿到最新的探测结果）
    import importlib
    import config.settings as _settings_mod
    importlib.reload(_settings_mod)

    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)
    (output_dir / "screenshots").mkdir(exist_ok=True)

    ts = time.strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"report_{ts}.html"
    log_path = output_dir / f"log_{ts}.txt"

    print(f"  报告: {report_path}")
    print(f"  截图: {output_dir / 'screenshots'}")
    print()

    if getattr(sys, "frozen", False):
        tests_dir = str(Path(sys._MEIPASS) / "tests")
    else:
        tests_dir = str(base_dir / "tests")

    import pytest

    args = [
        tests_dir,
        "-v",
        "--tb=short",
        f"--html={report_path}",
        "--self-contained-html",
        f"--log-file={log_path}",
        "--log-file-level=INFO",
        "--log-file-format=%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    ]

    exit_code = pytest.main(args)

    print()
    print("=" * 60)
    print(f"  测试完成，退出码: {exit_code}")
    print(f"  HTML 报告: {report_path}")
    print(f"  日志文件: {log_path}")
    print("=" * 60)
    print()
    input("按 Enter 键退出...")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())

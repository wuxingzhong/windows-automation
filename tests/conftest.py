"""
pytest 公共 fixtures
"""
import logging
import time
from pathlib import Path
from typing import Generator

import pytest

from scripts.windows_automator import WindowsAutomator
from config.settings import SETTINGS

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%H:%M:%S",
)


@pytest.fixture(scope="session")
def automator() -> Generator[WindowsAutomator, None, None]:
    """session 级别的自动化工具实例"""
    bot = WindowsAutomator(screenshot_dir=SETTINGS.screenshot_dir)
    yield bot


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, automator: WindowsAutomator):
    """测试失败时自动截图"""
    yield
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        name = request.node.name.replace("/", "_")
        automator.screenshot(f"FAIL_{name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """给 fixture 提供测试结果"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

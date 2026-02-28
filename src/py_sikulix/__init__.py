"""
Py-SikuliX: Python 客户端库，用于 SikuliX GUI 自动化。

通过 Py4J 与 SikuliX Java 后端交互，提供图像识别、
键盘鼠标操作、应用程序控制等功能。

示例:
    from py_sikulix import Screen, Pattern, Key

    screen = Screen()
    if match := screen.find("button.png"):
        match.click()
"""

__version__ = '0.1.1'

from py_sikulix.app import App
from py_sikulix.client import reg_exit_listener
from py_sikulix.keys import Btn, Key
from py_sikulix.location import Location
from py_sikulix.pattern import Pattern
from py_sikulix.region import Match, Region
from py_sikulix.screen import Screen
from py_sikulix.settings import Setting

# 公共 API
__all__ = [
    '__version__',
    # 客户端工具
    'reg_exit_listener',
    # 区域
    'Region',
    'Screen',
    'Match',
    # 元素
    'Pattern',
    'Location',
    'App',
    # 常量
    'Btn',
    'Key',
    # 配置
    'Setting',
]

#!/usr/bin/env python3
"""
键盘按键和鼠标按键常量模块。

Keyboard and mouse button constant modules.

首次访问时从 JVM 获取常量值。

参考: https://raiman.github.io/SikuliX1/javadocs/org/sikuli/script/Key.html
"""

from py_sikulix.client import get_cli


class LazyProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner) -> str | int:
        # 访问时触发这里
        return self.func(owner)


# 便捷类 - 用于类型提示和 IDE 补全
class Key:
    """
    键盘按键常量类。必须要创建实例后才能调用，为了兼容延迟加载只能折中采用实例化方案

    Keyboard key constant class.

    定义了键盘操作的按键常量，包括方向键、功能键、控制键和小键盘按键。
    """

    # 方向键
    UP: str = LazyProperty(lambda _: get_cli().Key.UP)  # type: ignore
    DOWN: str = LazyProperty(lambda _: get_cli().Key.DOWN)  # type: ignore
    LEFT: str = LazyProperty(lambda _: get_cli().Key.LEFT)  # type: ignore
    RIGHT: str = LazyProperty(lambda _: get_cli().Key.RIGHT)  # type: ignore

    # 功能键
    F1: str = LazyProperty(lambda _: get_cli().Key.F1)  # type: ignore
    F2: str = LazyProperty(lambda _: get_cli().Key.F2)  # type: ignore
    F3: str = LazyProperty(lambda _: get_cli().Key.F3)  # type: ignore
    F4: str = LazyProperty(lambda _: get_cli().Key.F4)  # type: ignore
    F5: str = LazyProperty(lambda _: get_cli().Key.F5)  # type: ignore
    F6: str = LazyProperty(lambda _: get_cli().Key.F6)  # type: ignore
    F7: str = LazyProperty(lambda _: get_cli().Key.F7)  # type: ignore
    F8: str = LazyProperty(lambda _: get_cli().Key.F8)  # type: ignore
    F9: str = LazyProperty(lambda _: get_cli().Key.F9)  # type: ignore
    F10: str = LazyProperty(lambda _: get_cli().Key.F10)  # type: ignore
    F11: str = LazyProperty(lambda _: get_cli().Key.F11)  # type: ignore
    F12: str = LazyProperty(lambda _: get_cli().Key.F12)  # type: ignore
    F13: str = LazyProperty(lambda _: get_cli().Key.F13)  # type: ignore
    F14: str = LazyProperty(lambda _: get_cli().Key.F14)  # type: ignore
    F15: str = LazyProperty(lambda _: get_cli().Key.F15)  # type: ignore

    # 控制键
    ALT: str = LazyProperty(lambda _: get_cli().Key.ALT)  # type: ignore
    BACKSPACE: str = LazyProperty(lambda _: get_cli().Key.BACKSPACE)  # type: ignore
    DELETE: str = LazyProperty(lambda _: get_cli().Key.DELETE)  # type: ignore
    END: str = LazyProperty(lambda _: get_cli().Key.END)  # type: ignore
    ENTER: str = LazyProperty(lambda _: get_cli().Key.ENTER)  # type: ignore
    ESC: str = LazyProperty(lambda _: get_cli().Key.ESC)  # type: ignore
    HOME: str = LazyProperty(lambda _: get_cli().Key.HOME)  # type: ignore
    INSERT: str = LazyProperty(lambda _: get_cli().Key.INSERT)  # type: ignore
    CAPS_LOCK: str = LazyProperty(lambda _: get_cli().Key.CAPS_LOCK)  # type: ignore
    CMD: str = LazyProperty(lambda _: get_cli().Key.CMD)  # type: ignore
    CTRL: str = LazyProperty(lambda _: get_cli().Key.CTRL)  # type: ignore
    PAGE_DOWN: str = LazyProperty(lambda _: get_cli().Key.PAGE_DOWN)  # type: ignore
    PAGE_UP: str = LazyProperty(lambda _: get_cli().Key.PAGE_UP)  # type: ignore
    PAUSE: str = LazyProperty(lambda _: get_cli().Key.PAUSE)  # type: ignore
    PRINTSCREEN: str = LazyProperty(lambda _: get_cli().Key.PRINTSCREEN)  # type: ignore
    SCROLL_LOCK: str = LazyProperty(lambda _: get_cli().Key.SCROLL_LOCK)  # type: ignore
    SEPARATOR: str = LazyProperty(lambda _: get_cli().Key.SEPARATOR)  # type: ignore
    SHIFT: str = LazyProperty(lambda _: get_cli().Key.SHIFT)  # type: ignore
    SPACE: str = LazyProperty(lambda _: get_cli().Key.SPACE)  # type: ignore
    TAB: str = LazyProperty(lambda _: get_cli().Key.TAB)  # type: ignore
    WIN: str = LazyProperty(lambda _: get_cli().Key.WIN)  # type: ignore

    # 小键盘
    NUM_LOCK: str = LazyProperty(lambda _: get_cli().Key.NUM_LOCK)  # type: ignore
    ADD: str = LazyProperty(lambda _: get_cli().Key.ADD)  # type: ignore # 小键盘加号
    MINUS: str = LazyProperty(lambda _: get_cli().Key.MINUS)  # type: ignore # 小键盘减号
    DIVIDE: str = LazyProperty(lambda _: get_cli().Key.DIVIDE)  # type: ignore # 小键盘除号
    MULTIPLY: str = LazyProperty(lambda _: get_cli().Key.MULTIPLY)  # type: ignore # 小键盘乘号
    DECIMAL: str = LazyProperty(lambda _: get_cli().Key.DECIMAL)  # type: ignore # 小键盘小数点
    NUM0: str = LazyProperty(lambda _: get_cli().Key.NUM0)  # type: ignore
    NUM1: str = LazyProperty(lambda _: get_cli().Key.NUM1)  # type: ignore
    NUM2: str = LazyProperty(lambda _: get_cli().Key.NUM2)  # type: ignore
    NUM3: str = LazyProperty(lambda _: get_cli().Key.NUM3)  # type: ignore
    NUM4: str = LazyProperty(lambda _: get_cli().Key.NUM4)  # type: ignore
    NUM5: str = LazyProperty(lambda _: get_cli().Key.NUM5)  # type: ignore
    NUM6: str = LazyProperty(lambda _: get_cli().Key.NUM6)  # type: ignore
    NUM7: str = LazyProperty(lambda _: get_cli().Key.NUM7)  # type: ignore
    NUM8: str = LazyProperty(lambda _: get_cli().Key.NUM8)  # type: ignore
    NUM9: str = LazyProperty(lambda _: get_cli().Key.NUM9)  # type: ignore


class Btn:
    """
    鼠标按键常量类。必须要创建实例后才能调用，为了兼容延迟加载只能折中采用实例化方案

    Mouse button constant class.

    定义了鼠标操作的按键常量，包括左键、右键、中键和滚轮方向。
    这些是固定的整数值，不需要从 JVM 获取。
    """

    LEFT: int = LazyProperty(lambda _: get_cli().Button.LEFT)  # type: ignore
    MIDDLE: int = LazyProperty(lambda _: get_cli().Button.MIDDLE)  # type: ignore
    RIGHT: int = LazyProperty(lambda _: get_cli().Button.RIGHT)  # type: ignore
    WHEEL_DOWN: int = LazyProperty(lambda _: get_cli().Button.WHEEL_DOWN)  # type: ignore
    WHEEL_UP: int = LazyProperty(lambda _: get_cli().Button.WHEEL_UP)  # type: ignore


if __name__ == '__main__':
    print('方向键:')
    print(f'UP: {Key.UP}')
    print(f'DOWN: {Key.DOWN}')
    print(f'LEFT: {Key.LEFT}')
    print(f'RIGHT: {Key.RIGHT}')

    print('\n功能键:')
    print(f'F1: {Key.F1}')
    print(f'F2: {Key.F2}')

    print('\n控制键:')
    print(f'ENTER: {Key.ENTER}')
    print(f'TAB: {Key.TAB}')
    print(f'ESC: {Key.ESC}')

    print('\n小键盘:')
    print(f'ADD: {Key.ADD}')
    print(f'MINUS: {Key.MINUS}')

    print('\n鼠标键:')
    print(f'LEFT: {Btn.LEFT}')
    print(f'RIGHT: {Btn.RIGHT}')
    print(f'MIDDLE: {Btn.MIDDLE}')
    print(f'WHEEL_UP: {Btn.WHEEL_UP}')
    print(f'WHEEL_DOWN: {Btn.WHEEL_DOWN}')

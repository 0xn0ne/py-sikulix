from py_sikulix.client import CLIENT


class Key:
    """键盘按键常量类。

    定义了键盘操作的按键常量，包括方向键、功能键、控制键和小键盘按键。
    参考: https://javadoc.io/static/com.sikulix/sikulixapi/2.0.5/org/sikuli/script/Key.html
    """

    # 方向键
    UP: str = CLIENT.Key.UP  # type: ignore
    DOWN: str = CLIENT.Key.DOWN  # type: ignore
    LEFT: str = CLIENT.Key.LEFT  # type: ignore
    RIGHT: str = CLIENT.Key.RIGHT  # type: ignore

    # 功能键
    F1: str = CLIENT.Key.F1  # type: ignore
    F2: str = CLIENT.Key.F2  # type: ignore
    F3: str = CLIENT.Key.F3  # type: ignore
    F4: str = CLIENT.Key.F4  # type: ignore
    F5: str = CLIENT.Key.F5  # type: ignore
    F6: str = CLIENT.Key.F6  # type: ignore
    F7: str = CLIENT.Key.F7  # type: ignore
    F8: str = CLIENT.Key.F8  # type: ignore
    F9: str = CLIENT.Key.F9  # type: ignore
    F10: str = CLIENT.Key.F10  # type: ignore
    F11: str = CLIENT.Key.F11  # type: ignore
    F12: str = CLIENT.Key.F12  # type: ignore
    F13: str = CLIENT.Key.F13  # type: ignore
    F14: str = CLIENT.Key.F14  # type: ignore
    F15: str = CLIENT.Key.F15  # type: ignore

    # 控制键
    ALT: str = CLIENT.Key.ALT  # type: ignore
    BACKSPACE: str = CLIENT.Key.BACKSPACE  # type: ignore
    DELETE: str = CLIENT.Key.DELETE  # type: ignore
    END: str = CLIENT.Key.END  # type: ignore
    ENTER: str = CLIENT.Key.ENTER  # type: ignore
    ESC: str = CLIENT.Key.ESC  # type: ignore
    HOME: str = CLIENT.Key.HOME  # type: ignore
    INSERT: str = CLIENT.Key.INSERT  # type: ignore
    CAPS_LOCK: str = CLIENT.Key.CAPS_LOCK  # type: ignore
    CMD: str = CLIENT.Key.CMD  # type: ignore
    CTRL: str = CLIENT.Key.CTRL  # type: ignore
    PAGE_DOWN: str = CLIENT.Key.PAGE_DOWN  # type: ignore
    PAGE_UP: str = CLIENT.Key.PAGE_UP  # type: ignore
    PAUSE: str = CLIENT.Key.PAUSE  # type: ignore
    PRINTSCREEN: str = CLIENT.Key.PRINTSCREEN  # type: ignore
    SCROLL_LOCK: str = CLIENT.Key.SCROLL_LOCK  # type: ignore
    SEPARATOR: str = CLIENT.Key.SEPARATOR  # type: ignore
    SHIFT: str = CLIENT.Key.SHIFT  # type: ignore
    SPACE: str = CLIENT.Key.SPACE  # type: ignore
    TAB: str = CLIENT.Key.TAB  # type: ignore
    WIN: str = CLIENT.Key.WIN  # type: ignore

    # 小键盘
    NUM_LOCK: str = CLIENT.Key.NUM_LOCK  # type: ignore
    ADD: str = CLIENT.Key.ADD  # type: ignore 小键盘加号
    MINUS: str = CLIENT.Key.MINUS  # type: ignore 小键盘减号
    DIVIDE: str = CLIENT.Key.DIVIDE  # type: ignore 小键盘除号
    MULTIPLY: str = CLIENT.Key.MULTIPLY  # type: ignore 小键盘乘号
    DECIMAL: str = CLIENT.Key.DECIMAL  # type: ignore 小键盘小数点
    NUM0: str = CLIENT.Key.NUM0  # type: ignore
    NUM1: str = CLIENT.Key.NUM1  # type: ignore
    NUM2: str = CLIENT.Key.NUM2  # type: ignore
    NUM3: str = CLIENT.Key.NUM3  # type: ignore
    NUM4: str = CLIENT.Key.NUM4  # type: ignore
    NUM5: str = CLIENT.Key.NUM5  # type: ignore
    NUM6: str = CLIENT.Key.NUM6  # type: ignore
    NUM7: str = CLIENT.Key.NUM7  # type: ignore
    NUM8: str = CLIENT.Key.NUM8  # type: ignore
    NUM9: str = CLIENT.Key.NUM9  # type: ignore


class Btn:
    """
    鼠标按键常量类

    定义了鼠标操作的按键常量，包括左键、右键、中键和滚轮方向。
    参考: https://javadoc.io/static/com.sikulix/sikulixapi/2.0.5/org/sikuli/script/Button.html
    """

    LEFT: int = CLIENT.Button.LEFT  # type: ignore
    MIDDLE: int = CLIENT.Button.MIDDLE  # type: ignore
    RIGHT: int = CLIENT.Button.RIGHT  # type: ignore
    WHEEL_DOWN: int = CLIENT.Button.WHEEL_DOWN  # type: ignore
    WHEEL_UP: int = CLIENT.Button.WHEEL_UP  # type: ignore


if __name__ == '__main__':
    print('方向键：')
    print(f'UP: {ord(Key.UP)}')
    print(f'DOWN: {ord(Key.DOWN)}')
    print(f'LEFT: {ord(Key.LEFT)}')
    print(f'RIGHT: {ord(Key.RIGHT)}')

    print('\n功能键：')
    print(f'F1: {ord(Key.F1)}')
    print(f'F2: {ord(Key.F2)}')
    print(f'F3: {ord(Key.F3)}')
    print(f'F4: {ord(Key.F4)}')
    print(f'F5: {ord(Key.F5)}')
    print(f'F6: {ord(Key.F6)}')
    print(f'F7: {ord(Key.F7)}')
    print(f'F8: {ord(Key.F8)}')
    print(f'F9: {ord(Key.F9)}')
    print(f'F10: {ord(Key.F10)}')
    print(f'F11: {ord(Key.F11)}')
    print(f'F12: {ord(Key.F12)}')
    print(f'F13: {ord(Key.F13)}')
    print(f'F14: {ord(Key.F14)}')
    print(f'F15: {ord(Key.F15)}')

    print('\n控制键：')
    print(f'ALT: {ord(Key.ALT)}')
    print(f'BACKSPACE: {ord(Key.BACKSPACE)}')
    print(f'DELETE: {ord(Key.DELETE)}')
    print(f'END: {ord(Key.END)}')
    print(f'ENTER: {ord(Key.ENTER)}')
    print(f'ESC: {ord(Key.ESC)}')
    print(f'HOME: {ord(Key.HOME)}')
    print(f'INSERT: {ord(Key.INSERT)}')
    print(f'CAPS_LOCK: {ord(Key.CAPS_LOCK)}')
    print(f'CMD: {ord(Key.CMD)}')
    print(f'CTRL: {ord(Key.CTRL)}')
    print(f'PAGE_DOWN: {ord(Key.PAGE_DOWN)}')
    print(f'PAGE_UP: {ord(Key.PAGE_UP)}')
    print(f'PAUSE: {ord(Key.PAUSE)}')
    print(f'PRINTSCREEN: {ord(Key.PRINTSCREEN)}')
    print(f'SCROLL_LOCK: {ord(Key.SCROLL_LOCK)}')
    print(f'SEPARATOR: {ord(Key.SEPARATOR)}')
    print(f'SHIFT: {ord(Key.SHIFT)}')
    print(f'SPACE: {ord(Key.SPACE)}')
    print(f'TAB: {ord(Key.TAB)}')
    print(f'WIN: {ord(Key.WIN)}')

    print('\n小键盘：')
    print(f'NUM_LOCK: {ord(Key.NUM_LOCK)}')
    print(f'ADD: {ord(Key.ADD)}')
    print(f'MINUS: {ord(Key.MINUS)}')
    print(f'DIVIDE: {ord(Key.DIVIDE)}')
    print(f'MULTIPLY: {ord(Key.MULTIPLY)}')
    print(f'DECIMAL: {ord(Key.DECIMAL)}')
    print(f'NUM0: {ord(Key.NUM0)}')
    print(f'NUM1: {ord(Key.NUM1)}')
    print(f'NUM2: {ord(Key.NUM2)}')
    print(f'NUM3: {ord(Key.NUM3)}')
    print(f'NUM4: {ord(Key.NUM4)}')
    print(f'NUM5: {ord(Key.NUM5)}')
    print(f'NUM6: {ord(Key.NUM6)}')
    print(f'NUM7: {ord(Key.NUM7)}')
    print(f'NUM8: {ord(Key.NUM8)}')
    print(f'NUM9: {ord(Key.NUM9)}')

    print('鼠标键：')
    print(f'鼠标左键: {Btn.LEFT}')
    print(f'鼠标右键: {Btn.RIGHT}')
    print(f'鼠标中键: {Btn.MIDDLE}')
    print(f'鼠标滚轮上: {Btn.WHEEL_DOWN}')
    print(f'鼠标滚轮下: {Btn.WHEEL_UP}')

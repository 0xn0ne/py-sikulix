#!/usr/bin/env python3
#
"""
BaseRegion 基础区域类

这是 Region 和 Match 的共同基类，提取了两者共有的属性和方法。
通过继承这个基类，Region 和 Match 可以共享基础功能，避免代码重复。
"""

import logging
import pathlib
from typing import TYPE_CHECKING, Optional, Union

from py4j.java_gateway import JavaObject

from py_sikulix.client import CLIENT
from py_sikulix.keys import Btn
from py_sikulix.location import Location
from py_sikulix.pattern import Pattern

logger = logging.getLogger(__name__)

# 使用 TYPE_CHECKING 避免循环导入
if TYPE_CHECKING:
    from py_sikulix.match import Match


class BaseRegion:
    """
    BaseRegion 基础区域类

    这是 Region 和 Match 的共同基类，包含了区域的基本属性和交互操作方法。
    Region 和 Match 都继承这个类，从而共享基础功能。
    """

    def __init__(self, java_obj: JavaObject):
        """
        初始化对象。

        Args:
            java_instance: Java 对象实例
        """
        self._raw = java_obj  # type: ignore

    @staticmethod
    def _handle_psmrl(
        psmrl: Optional[Union[Pattern, str, pathlib.Path, 'BaseRegion', Location]],
    ) -> Optional[Union[str, JavaObject]]:
        """
        处理传入的 psmrl 参数，将其转换为统一的格式并返回。

        参数:
            psmrl (Optional[Union[Pattern, str, pathlib.Path, 'BaseRegion', Location]]):
                输入的参数，可以是 Pattern、字符串、路径对象、BaseRegion 或 Location 类型，
                也可以是 None。

        返回:
            Optional[Union[str, JavaObject]]:
                处理后的结果，可能是字符串、路径对象或其他原始类型，也可能为 None。
        """
        # 如果输入为空，直接返回 None
        if not psmrl:
            return

        # 如果输入是字符串，将其转换为 Path 对象
        if isinstance(psmrl, str):
            psmrl = pathlib.Path(psmrl)
        # 如果输入对象具有 '_raw' 属性，则提取其原始数据
        elif hasattr(psmrl, '_raw'):
            # 处理 Match, Pattern, BaseRegion, Location 的对象
            psmrl = psmrl._raw  # type: ignore

        # 如果输入是 Path 对象，将其转换为绝对路径的字符串形式
        if isinstance(psmrl, pathlib.Path):
            psmrl = str(psmrl.absolute())

        # 返回处理后的结果
        return psmrl  # type: ignore

    # ==================== 位置属性访问器 ====================

    @property
    def x(self) -> int:
        """
        获取区域左上角 X 坐标。

        Returns:
            X 坐标值
        """
        return self._raw.getX()  # type: ignore

    @x.setter
    def x(self, value: int):
        self._raw.setX(value)  # type: ignore

    @property
    def y(self) -> int:
        """
        获取区域左上角 Y 坐标。

        Returns:
            Y 坐标值
        """
        return self._raw.getY()  # type: ignore

    @y.setter
    def y(self, value: int):
        self._raw.setY(value)  # type: ignore

    @property
    def w(self) -> int:
        """
        获取区域宽度。

        Returns:
            宽度值
        """
        return self._raw.getW()  # type: ignore

    @w.setter
    def w(self, value: int):
        self._raw.setW(value)  # type: ignore

    @property
    def h(self) -> int:
        """
        获取区域高度。

        Returns:
            高度值
        """
        return self._raw.getH()  # type: ignore

    @h.setter
    def h(self, value: int):
        self._raw.setH(value)  # type: ignore

    def get_x(self) -> int:
        return self.x  # type: ignore

    def get_y(self) -> int:
        return self.y  # type: ignore

    def get_w(self) -> int:
        return self.w  # type: ignore

    def get_h(self) -> int:
        return self.h  # type: ignore

    def get_bounds(self) -> tuple[int, int, int, int]:
        """
        获取区域的边界坐标和尺寸。

        Returns:
            返回一个四元组，分别表示区域的 (x坐标, y坐标, 宽度, 高度)
        """
        return self.x, self.y, self.w, self.h  # type: ignore

    # ==================== 几何方法 ====================

    def get_center(self) -> Location:
        """
        获取区域中心位置点。

        Returns:
            区域中心点的 Location 对象
        """
        return Location(self._raw.getCenter())  # type: ignore

    def get_top_left(self) -> Location:
        """
        获取区域左上角位置点。

        Returns:
            区域左上角点的 Location 对象
        """
        return Location(self._raw.getTopLeft())  # type: ignore

    def get_top_right(self) -> Location:
        """
        获取区域右上角位置点。

        Returns:
            区域右上角点的 Location 对象
        """
        return Location(self._raw.getTopRight())  # type: ignore

    def get_bottom_left(self) -> Location:
        """
        获取区域左下角位置点。

        Returns:
            区域左下角点的 Location 对象
        """
        return Location(self._raw.getBottomLeft())  # type: ignore

    def get_bottom_right(self) -> Location:
        """
        获取区域右下角位置点。

        Returns:
            区域右下角点的 Location 对象
        """
        return Location(self._raw.getBottomRight())  # type: ignore

    # ==================== 鼠标操作方法 ====================

    def click(
        self,
        psmrl: Optional[Union[Pattern, str, pathlib.Path, 'BaseRegion', 'Match', Location]] = None,
        key: Optional[int] = None,
    ) -> int:
        """
        使用左键点击区域内对象。

        Args:
            psmrl: 目标点的图片路径、Pattern 对象、BaseRegion 对象、Match 对象或 Location 对象。如果为 None，则点击区域中心。
            key: 要使用其他点击的键，可选参数，默认为 None。

        Returns:
            点击的次数（通常为 1）。返回 0 表示由于某些原因未能执行点击。
        """
        try:
            psmrl = self._handle_psmrl(psmrl)
            if psmrl is None:
                # 点击区域中心
                if key is None:
                    result = self._raw.click()  # type: ignore
                else:
                    result = self._raw.click(key)  # type: ignore
            else:
                if key is None:
                    result = self._raw.click(psmrl)  # type: ignore
                else:
                    result = self._raw.click(psmrl, key)  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f"click 操作失败: {e}")
            return 0
    def double_click(
        self,
        psmrl: Optional[Union[Pattern, str, pathlib.Path, 'BaseRegion', Location]] = None,
        key: Optional[int] = None,
    ) -> int:
        """
        双击区域内找到的目标对象。

        Args:
            psmrl: 目标点的图片路径、Pattern 对象、BaseRegion 对象或 Location 对象。
                如果为 None，则双击区域中心。
            key: 要使用其他点击的键，可选参数，默认为 None。

        Returns:
            双击次数（通常为 1 次）。若为 0 则表示由于某些原因未能执行点击。
        """
        psmrl = self._handle_psmrl(psmrl)  # type: ignore
        if psmrl is None:
            # 点击区域中心
            if key is None:
                return self._raw.doubleClick()  # type: ignore
            return self._raw.doubleClick(key)  # type: ignore

        if key is None:
            return self._raw.doubleClick(psmrl)  # type: ignore
        return self._raw.doubleClick(psmrl, key)  # type: ignore

    def right_click(
        self,
        psmrl: Optional[Union[Pattern, str, pathlib.Path, 'BaseRegion', Location]] = None,
        key: Optional[int] = None,
    ) -> int:
        """
        右键点击区域内找到的目标图像。

        Args:
            psmrl: 目标点的图片路径、Pattern 对象、BaseRegion 对象或 Location 对象。
                如果为 None，则右键点击区域中心。
            key: 要使用其他点击的键，可选参数，默认为 None。

        Returns:
            点击的次数（通常为 1）。返回 0 表示由于某些原因未能执行点击。
        """
        psmrl = self._handle_psmrl(psmrl)  # type: ignore
        if psmrl is None:
            # 点击区域中心
            if key is None:
                return self._raw.rightClick()  # type: ignore
            return self._raw.rightClick(key)  # type: ignore

        if key is None:
            return self._raw.rightClick(psmrl)  # type: ignore
        return self._raw.rightClick(psmrl, key)  # type: ignore

    def hover(
        self,
        psmrl: Optional[Union[Pattern, str, pathlib.Path, 'BaseRegion', Location]] = None,
    ) -> int:
        """
        将鼠标悬停在区域内找到的目标上。

        Args:
            psmrl: 目标点的图片路径、Pattern 对象、BaseRegion 对象或 Location 对象。
                如果为 None，则悬停在区域中心。

        Returns:
            若鼠标指针可移动至点击点，则返回数字 1。返回 0 表示因某些原因无法执行移动操作。
        """
        psmrl = self._handle_psmrl(psmrl)  # type: ignore
        if psmrl is None:
            # 点击区域中心
            self._raw.hover()  # type: ignore

        return self._raw.hover(psmrl)  # type: ignore

    def drag_drop(
        self,
        drag_from: Union[Pattern, str, pathlib.Path, 'BaseRegion', Location],
        drop_dest: Union[Pattern, str, pathlib.Path, 'BaseRegion', Location],
    ) -> int:
        """
        在区域内执行拖放操作，将对象从源位置拖动到目标位置。

        Args:
            drag_from: 拖动源 - 图片路径、Pattern 对象、BaseRegion 对象或 Location 对象。
            drop_to: 放置目标 - 图片路径、Pattern 对象、BaseRegion 对象或 Location 对象。

        Returns:
            操作成功返回 1，失败返回 0。
        """
        drag_from = self._handle_psmrl(drag_from)  # type: ignore
        drop_dest = self._handle_psmrl(drop_dest)  # type: ignore
        if not drag_from or not drop_dest:
            raise ValueError('"drag_from" and "drop_dest" cannot be none.')

        return self._raw.dragDrop(drag_from, drop_dest)  # type: ignore

    def mouse_down(self, button: int = Btn.LEFT) -> int:
        """
        按下鼠标按钮。

        Args:
            button: 按钮常量 Btn.LEFT、Btn.MIDDLE 或 Btn.RIGHT。

        Returns:
            若操作成功则返回数字 1，否则返回 0。
        """
        try:
            result = self._raw.mouseDown(button)  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f"mouse_down 操作失败: {e}")
            return 0

    def mouse_up(self, button: int = Btn.LEFT) -> int:
        """
        释放鼠标按钮。

        Args:
            button: 按钮常量 Btn.LEFT、Btn.MIDDLE 或 Btn.RIGHT。

        Returns:
            若操作成功则返回数字 1，否则返回 0。
        """
        try:
            result = self._raw.mouseUp(button)  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f"mouse_up 操作失败: {e}")
            return 0

    def mouse_move(
        self,
        psmrl_or_xoff: Optional[Union[Pattern, str, 'BaseRegion', Location, int]],
        yoff: Optional[int] = None,
    ) -> int:
        """
        移动鼠标到目标位置。

        当参数 psmrl_or_xoff 和 yoff 都是数字时，则将鼠标移动到起始点相对偏移psmrl_or_xoff, yoff的位置
        （<0 向左/上，>0 向右/下）。

        Args:
            psmrl_or_xoff: 目标点的图片路径、Pattern 对象、BaseRegion 对象、Location 对象，
                或鼠标 X 坐标偏移量。如果为 None，则移动到区域中心。
            yoff: 鼠标 Y 坐标偏移量。

        Returns:
            若操作成功则返回数字 1，否则返回 0。
        """
        if psmrl_or_xoff is None:
            # 移动到区域中心
            return self._raw.mouseMove()  # type: ignore

        if isinstance(psmrl_or_xoff, int) and isinstance(yoff, int):
            return self._raw.mouseMove(psmrl_or_xoff, yoff)  # type: ignore

        psmrl_or_xoff = self._handle_psmrl(psmrl_or_xoff)  # type: ignore
        return self._raw.mouseMove(psmrl_or_xoff)  # type: ignore

    def wheel(
        self,
        psmrl: Optional[Union[Pattern, str, 'BaseRegion', Location]] = None,
        direction: int = Btn.WHEEL_DOWN,
        steps: int = 3,
    ) -> int:
        """
        将鼠标指针移动到 PSRML 指示的位置，并按指定方向转动鼠标滚轮指定步数。

        Args:
            psmrl: 目标点图片路径、Pattern 对象、BaseRegion 对象或 Location 对象。
                如果为 None，则在区域中心执行滚轮操作。
            direction: 滚轮方向的按钮常量 Button.WHEEL_DOWN 或 Button.WHEEL_UP。
            steps: 滚动步数。

        Returns:
            操作成功返回 1，失败返回 0。
        """
        try:
            if psmrl is None:
                # 在区域中心执行滚轮操作
                result = self._raw.wheel(direction, steps)  # type: ignore
            else:
                psmrl = self._handle_psmrl(psmrl)
                result = self._raw.wheel(psmrl, direction, steps)  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f"wheel 操作失败: {e}")
            return 0

    # ==================== 键盘操作方法 ====================

    def type(
        self,
        text: str,
        psmrl: Optional[Union[Pattern, str, 'BaseRegion', Location]] = None,
    ) -> int:
        """
        在区域内输入文本。

        Args:
            text: 文本内容。
            psmrl: 目标点的图片路径、Pattern 对象、BaseRegion 对象或 Location 对象。
                如果为 None，则在区域中心输入文本。

        Returns:
            若操作可执行则返回数字 1，否则返回 0。
        """
        psmrl = self._handle_psmrl(psmrl)  # type: ignore
        if psmrl is None:
            return self._raw.type(text)  # type: ignore
        return self._raw.type(psmrl, text)  # type: ignore

    def paste(
        self,
        text: str,
        psmrl: Optional[Union[Pattern, str, 'BaseRegion', Location]] = None,
    ) -> int:
        """
        在区域内粘贴文本（使用系统剪贴板）。

        Args:
            text: 文本内容。
            psmrl: 目标点的图片路径、Pattern 对象、BaseRegion 对象或 Location 对象。
                如果为 None，则在区域中心粘贴文本。

        Returns:
            操作成功返回 1，失败返回 0。
        """
        psmrl = self._handle_psmrl(psmrl)  # type: ignore
        if psmrl is None:
            return self._raw.paste(text)  # type: ignore
        return self._raw.paste(psmrl, text)  # type: ignore

    def key_down(self, keys: Union[str, list[str]]) -> int:
        """
        按下键盘按键。

        Args:
            keys: 一个或多个按键按键常量，Key 类的静态成员变量。

        Returns:
            若操作成功则返回数字 1，否则返回 0。
        """
        try:
            if isinstance(keys, list):
                keys = CLIENT.list2java_array(keys)  # type: ignore
            result = self._raw.keyDown(keys)  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f"key_down 操作失败: {e}")
            return 0

    def key_up(self, keys: Union[str, list[str]]) -> int:
        """
        释放键盘按键。

        Args:
            keys: 一个或多个按键按键常量，Key 类的静态成员变量。

        Returns:
            若操作成功则返回数字 1，否则返回 0。
        """
        try:
            if isinstance(keys, list):
                keys = CLIENT.list2java_array(keys)  # type: ignore
            result = self._raw.keyUp(keys)  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f"key_up 操作失败: {e}")
            return 0


    # ==================== 其他方法 ====================

    def highlight(self, color: str = 'red') -> int:
        """
        高亮当前区域，切换（若关闭则开启，反之亦然）。

        Args:
            color: 高亮颜色。
                可以是颜色名称（大小写可混合使用，内部将自动转换大写）：
                black, blue, cyan, gray, green, magenta, orange, pink, red, white, yellow。
                以下颜色名称必须严格遵守大小写：lightGray、LIGHT_GRAY、darkGray、DARK_GRAY。
                十六进制值的 RGB 颜色值，格式为#RRGGBB：如 #FF0000 表示红色。
                十进制值的 RGB 颜色值，格式为#RRRGGGBBB：如 #255255255 表示白色，
                是 0 到 255 范围内的整数值，必要时用前导零补齐。
            seconds: 高亮持续时间（秒），默认为 None，表示高亮 indefinitely（无限期），
                设置秒数的情况下脚本在此期间暂停执行。

        Returns:
            操作成功返回 1，失败返回 0。
        """
        return self._raw.highlight(color)  # type: ignore

    def highlight_all_off(self):
        return self._raw.highlightAllOff()  # type: ignore

    def text(self) -> str:
        """
        使用 OCR 提取区域内的文本内容。

        Returns:
            提取的文本内容（Unicode 编码）。
        """
        return self._raw.text()  # type: ignore

    def __repr__(self) -> str:
        """
        返回对象的字符串表示。

        Returns:
            对象的字符串表示
        """
        return f'<class {self.__class__.__name__} at {hex(id(self))}, [{self.x},{self.y} {self.w}x{self.h}]>'


if __name__ == '__main__':
    # 示例代码 - BaseRegion 类测试示例
    pass

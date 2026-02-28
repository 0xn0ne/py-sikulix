from __future__ import annotations

import contextlib
import logging
import pathlib
import time
from typing import Optional, Union

from py4j.java_gateway import JavaObject
from py4j.protocol import Py4JJavaError

from py_sikulix.client import get_cli
from py_sikulix.keys import Btn
from py_sikulix.location import Location
from py_sikulix.pattern import Pattern

logger = logging.getLogger(__name__)


class Region:
    """
    Region 类表示屏幕上的一个矩形区域，可以在此区域内进行图像搜索和其他操作。
    文档地址：https://sikulix-2014.readthedocs.io/en/latest/region.html
    """

    def __init__(
        self,
        x_or_java_obj: Union[int, JavaObject],
        y: Optional[int] = None,
        w: Optional[int] = None,
        h: Optional[int] = None,
    ):
        """
        创建一个新的 Region 对象。

        Args:
            x_or_java_obj: 区域左上角 X 坐标，或者为JavaObject
            y: 区域左上角 Y 坐标
            w: 区域宽度
            h: 区域高度

        Returns:
            新的 Region 对象
        """
        if all([isinstance(x_or_java_obj, int), isinstance(y, int), isinstance(w, int), isinstance(h, int)]):
            x_or_java_obj = get_cli().Region(x_or_java_obj, y, w, h)  # type: ignore
        if not isinstance(x_or_java_obj, JavaObject):
            raise ValueError(
                'please pass in the correct types of x, y, w, h parameters. do not directly pass in JavaObject to create the Class.'
            )
        self._raw = x_or_java_obj  # type: ignore

    def set_x(self, x: int) -> Region:
        """
        设置区域左上角 X 坐标。

        Args:
            x: 新的 X 坐标

        Returns:
            当前 Region 对象（支持链式调用）
        """
        self.x = x
        return self

    def set_y(self, y: int) -> Region:
        """
        设置区域左上角 Y 坐标。

        Args:
            y: 新的 Y 坐标

        Returns:
            当前 Region 对象（支持链式调用）
        """
        self.y = y
        return self

    def set_w(self, w: int) -> Region:
        """
        设置区域宽度。

        Args:
            w: 新的宽度

        Returns:
            当前 Region 对象（支持链式调用）
        """
        self.w = w
        return self

    def set_h(self, h: int) -> Region:
        """
        设置区域高度。

        Args:
            h: 新的高度

        Returns:
            当前 Region 对象（支持链式调用）
        """
        self.h = h
        return self

    @staticmethod
    def _handle_psmrl(
        psmrl: Optional[Union[Pattern, str, pathlib.Path, Region, Location]],
    ) -> Optional[Union[str, JavaObject]]:
        """
        处理传入的 psmrl 参数，将其转换为统一的格式并返回。

        参数:
            psmrl (Optional[Union[Pattern, str, pathlib.Path, 'Region', Location]]):
                输入的参数，可以是 Pattern、字符串、路径对象、Region 或 Location 类型，
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
            # 处理 Match, Pattern, Region, Location 的对象
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
        psmrl: Optional[Union[Pattern, str, pathlib.Path, Region, Match, Location]] = None,
        key: Optional[int] = None,
    ) -> int:
        """
        使用左键点击区域内对象。

        Args:
            psmrl: 目标点的图片路径、Pattern 对象、Region 对象、Match 对象或 Location 对象。如果为 None，则点击区域中心。
            key: 要使用其他点击的键，可选参数，默认为 None。

        Returns:
            点击的次数（通常为 1）。返回 0 表示由于某些原因未能执行点击。
        """
        try:
            psmrl = self._handle_psmrl(psmrl)  # type: ignore
            if psmrl is None:
                # 点击区域中心
                result = self._raw.click() if key is None else self._raw.click(key)  # type: ignore
            else:
                result = self._raw.click(psmrl) if key is None else self._raw.click(psmrl, key)  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f'click 操作失败: {e}')
            return 0

    def double_click(
        self,
        psmrl: Optional[Union[Pattern, str, pathlib.Path, Region, Location]] = None,
        key: Optional[int] = None,
    ) -> int:
        """
        双击区域内找到的目标对象。

        Args:
            psmrl: 目标点的图片路径、Pattern 对象、Region 对象或 Location 对象。
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
        psmrl: Optional[Union[Pattern, str, pathlib.Path, Region, Location]] = None,
        key: Optional[int] = None,
    ) -> int:
        """
        右键点击区域内找到的目标图像。

        Args:
            psmrl: 目标点的图片路径、Pattern 对象、Region 对象或 Location 对象。
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
        psmrl: Optional[Union[Pattern, str, pathlib.Path, Region, Location]] = None,
    ) -> int:
        """
        将鼠标悬停在区域内找到的目标上。

        Args:
            psmrl: 目标点的图片路径、Pattern 对象、Region 对象或 Location 对象。
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
        drag_from: Union[Pattern, str, pathlib.Path, Region, Location],
        drop_dest: Union[Pattern, str, pathlib.Path, Region, Location],
    ) -> int:
        """
        在区域内执行拖放操作，将对象从源位置拖动到目标位置。

        Args:
            drag_from: 拖动源 - 图片路径、Pattern 对象、Region 对象或 Location 对象。
            drop_to: 放置目标 - 图片路径、Pattern 对象、Region 对象或 Location 对象。

        Returns:
            操作成功返回 1，失败返回 0。
        """
        drag_from = self._handle_psmrl(drag_from)  # type: ignore
        drop_dest = self._handle_psmrl(drop_dest)  # type: ignore
        if not drag_from or not drop_dest:
            raise ValueError('"drag_from" and "drop_dest" cannot be none.')

        return self._raw.dragDrop(drag_from, drop_dest)  # type: ignore

    def mouse_down(self, button: int | None = None) -> int:
        """
        按下鼠标按钮。

        Args:
            button: 按钮常量 Btn.LEFT、Btn.MIDDLE 或 Btn.RIGHT。

        Returns:
            若操作成功则返回数字 1，否则返回 0。
        """
        try:
            result = self._raw.mouseDown(button) if button else self._raw.mouseDown()  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f'mouse_down 操作失败: {e}')
            return 0

    def mouse_up(self, button: int | None = None) -> int:
        """
        释放鼠标按钮。

        Args:
            button: 按钮常量 Btn.LEFT、Btn.MIDDLE 或 Btn.RIGHT。

        Returns:
            若操作成功则返回数字 1，否则返回 0。
        """
        try:
            result = self._raw.mouseUp(button) if button else self._raw.mouseUp()  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f'mouse_up 操作失败: {e}')
            return 0

    def mouse_move(
        self,
        psmrl_or_xoff: Optional[Union[Pattern, str, Region, Location, int]],
        yoff: Optional[int] = None,
    ) -> int:
        """
        移动鼠标到目标位置。

        当参数 psmrl_or_xoff 和 yoff 都是数字时，则将鼠标移动到起始点相对偏移psmrl_or_xoff, yoff的位置
        （<0 向左/上，>0 向右/下）。

        Args:
            psmrl_or_xoff: 目标点的图片路径、Pattern 对象、Region 对象、Location 对象，
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
        psmrl: Optional[Union[Pattern, str, Region, Location]] = None,
        direction: int | None = None,
        steps: int = 3,
    ) -> int:
        """
        将鼠标指针移动到 PSRML 指示的位置，并按指定方向转动鼠标滚轮指定步数。

        Args:
            psmrl: 目标点图片路径、Pattern 对象、Region 对象或 Location 对象。
                如果为 None，则在区域中心执行滚轮操作。
            direction: 滚轮方向的按钮常量 Button.WHEEL_DOWN 或 Button.WHEEL_UP。
            steps: 滚动步数。

        Returns:
            操作成功返回 1，失败返回 0。
        """
        if direction is None:
            direction = Btn.WHEEL_DOWN
        try:
            if psmrl is None:
                # 在区域中心执行滚轮操作
                result = self._raw.wheel(direction, steps)  # type: ignore
            else:
                psmrl = self._handle_psmrl(psmrl)  # type: ignore
                result = self._raw.wheel(psmrl, direction, steps)  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f'wheel 操作失败: {e}')
            return 0

    # ==================== 键盘操作方法 ====================

    def type(
        self,
        text: str,
        psmrl: Optional[Union[Pattern, str, Region, Location]] = None,
    ) -> int:
        """
        在区域内输入文本。

        Args:
            text: 文本内容。
            psmrl: 目标点的图片路径、Pattern 对象、Region 对象或 Location 对象。
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
        psmrl: Optional[Union[Pattern, str, Region, Location]] = None,
    ) -> int:
        """
        在区域内粘贴文本（使用系统剪贴板）。

        Args:
            text: 文本内容。
            psmrl: 目标点的图片路径、Pattern 对象、Region 对象或 Location 对象。
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
                keys = get_cli().list2java_array(keys)  # type: ignore
            result = self._raw.keyDown(keys)  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f'key_down 操作失败: {e}')
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
                keys = get_cli().list2java_array(keys)  # type: ignore
            result = self._raw.keyUp(keys)  # type: ignore
            return int(result) if result is not None else 0
        except Exception as e:
            logger.error(f'key_up 操作失败: {e}')
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

    def move_to(self, x_or_location: Union[Location, int], y: Optional[int] = None) -> Region:
        """
        将区域移动到指定位置，将修改 x 与 y 值。

        Args:
            location: Location 对象将成为新的左上角

        Returns:
            当前 Region 对象（支持链式调用）
        """
        if isinstance(x_or_location, int) and isinstance(y, int):
            x_or_location = Location(x_or_location, y)
        self._raw.moveTo(x_or_location._raw)  # type: ignore
        return self

    def set_roi(self, x: int, y: int, w: int, h: int) -> Region:
        """
        将搜索范围限定在更小区域以加速处理（兴趣区域）。

        Args:
            x: ROI 左上角 X 坐标
            y: ROI 左上角 Y 坐标
            w: ROI 宽度
            h: ROI 高度

        Returns:
            当前 Region 对象（支持链式调用）
        """
        self._raw.setROI(x, y, w, h)  # type: ignore
        return self

    def set_rect(self, x: int, y: int, w: int, h: int) -> Region:
        """
        将改变区域的位置或大小（移动或缩放）。

        Args:
            x: 新的 X 坐标
            y: 新的 Y 坐标
            w: 新的宽度
            h: 新的高度

        Returns:
            当前 Region 对象（支持链式调用）
        """
        self._raw.setRect(x, y, w, h)  # type: ignore
        return self

    # 区域内查找与等待视觉事件
    def find(self, target: Union[str, pathlib.Path, Pattern]) -> Optional[Match]:
        """
        在区域内查找目标图像。

        Args:
            target: 图像路径或 Pattern 对象

        Returns:
            找到的第一个匹配结果，未找到返回 None
        """
        if isinstance(target, str):
            target = pathlib.Path(target)
        if isinstance(target, pathlib.Path):
            target = str(target.absolute())
        if isinstance(target, Pattern):
            target = target._raw  # type: ignore

        try:
            result = self._raw.find(target)  # type: ignore
        except Py4JJavaError:
            return None
        return Match(result)  # type: ignore

    def find_all(self, target: Union[str, pathlib.Path, Pattern]) -> list[Match]:
        """
        在区域内查找所有匹配目标图像的位置。

        Args:
            target: 图像路径或 Pattern 对象

        Returns:
            所有匹配结果的列表
        """
        if isinstance(target, str):
            target = pathlib.Path(target)
        if isinstance(target, pathlib.Path):
            target = str(target.absolute())
        if isinstance(target, Pattern):
            target = target._raw  # type: ignore
        results = self._raw.findAll(target)  # type: ignore
        matches = []

        while results.hasNext():  # type: ignore
            matches.append(Match(results.next()))  # type: ignore
        return matches

    def find_multi_color(
        self,
        color_str: str,
        similarity: float = 0.7,
    ) -> Match | None:
        from py_sikulix.extend import CrossPlatformFinder

        finder = CrossPlatformFinder()
        ret = finder.find_multi_color(color_str, similarity, (self.x, self.y, self.w, self.h))
        if not ret:
            return None
        return Match(get_cli().Match(Region(ret[0][0], ret[0][1], ret[0][2], ret[0][3])._raw, ret[1]))  # type: ignore

    def wait(self, target: Union[str, pathlib.Path, Pattern], timeout: float = 30) -> Optional[Match]:
        """
        等待目标图像出现在区域内。

        Args:
            target: 要等待的图像路径或 Pattern 对象
            timeout: 最大等待时间（秒）

        Returns:
            找到的匹配结果，超时未找到返回 None
        """
        if isinstance(target, str):
            target = pathlib.Path(target)
        if isinstance(target, pathlib.Path):
            target = str(target.absolute())
        if isinstance(target, Pattern):
            target = target._raw  # type: ignore
        current_time = time.time()
        while True:
            result = None
            with contextlib.suppress(Py4JJavaError):
                result = self._raw.find(target)  # type: ignore
            if result:
                return Match(result)
            if current_time + timeout < time.time():
                break
            time.sleep(0.2)
        return None

    def wait_vanish(self, target: Union[str, pathlib.Path, Pattern], timeout: float = 30.0) -> bool:
        """
        等待目标图像从区域内消失。

        Args:
            target: 要等待消失的图像路径或 Pattern 对象
            timeout: 最大等待时间（秒）

        Returns:
            目标消失返回 True，其他情况返回 False
        """
        if isinstance(target, str):
            target = pathlib.Path(target)
        if isinstance(target, pathlib.Path):
            target = str(target.absolute())
        if isinstance(target, Pattern):
            target = target._raw  # type: ignore

        current_time = time.time()
        while True:
            result = None
            with contextlib.suppress(Py4JJavaError):  # 不存在图片会直接抛出异常
                result = self._raw.find(target)  # type: ignore
            if not result:
                return True
            if current_time + timeout < time.time():
                break
            time.sleep(0.2)
        return False

    def exists(self, target: Union[str, pathlib.Path, Pattern]) -> Optional[Match]:
        """
        等待目标图像出现在区域内，但在 FindFailed 时不会抛出异常。

        Args:
            target: 要检查的图像路径或 Pattern 对象
            timeout: 超时时间（秒）

        Returns:
            找到的匹配结果，超时未找到返回 None
        """
        if isinstance(target, str):
            target = pathlib.Path(target)
        if isinstance(target, pathlib.Path):
            target = str(target.absolute())
        if isinstance(target, Pattern):
            target = target._raw  # type: ignore

        result = self._raw.exists(target)  # type: ignore
        return Match(result) if result else None

    def get_last_match(self) -> Optional[Match]:
        """
        获取最后一次成功查找的匹配结果。

        获取该区域最后一次 find()、wait() 或 exists() 操作成功找到的匹配对象。
        如果没有成功的查找操作或查找失败，则返回 None。

        Returns:
            最后一次匹配结果，无匹配返回 None
        """
        result = self._raw.getLastMatch()  # type: ignore
        return Match(result) if result else None

    def get_last_matches(self) -> list[Match]:
        """
        获取最后一次 find_all 操作的所有匹配结果。

        获取该区域最后一次 find_all() 操作找到的所有匹配对象列表。
        如果没有执行过 find_all 操作，则返回空列表。

        Returns:
            所有匹配结果的列表
        """
        results = self._raw.getLastMatches()  # type: ignore
        matches = []
        for r in results:  # type: ignore
            matches.append(Match(r))
        return matches

    # 区域内动作操作

    def above(self, height: Optional[int] = None) -> Region:
        """
        创建当前区域上方的新区域。

        Args:
            height: 新区域的高度，默认为当前区域高度

        Returns:
            当前区域上方的新区域对象
        """
        if height is None:
            return Region(self._raw.above())  # type: ignore
        return Region(self._raw.above(height))  # type: ignore

    def below(self, height: Optional[int] = None) -> Region:
        """
        创建当前区域下方的新区域。

        Args:
            height: 新区域的高度，默认为当前区域高度

        Returns:
            当前区域下方的新区域对象
        """
        if height is None:
            return Region(self._raw.below())  # type: ignore
        return Region(self._raw.below(height))  # type: ignore

    def left(self, width: Optional[int] = None) -> Region:
        """
        创建当前区域左侧的新区域。

        Args:
            width: 新区域的宽度，默认为当前区域宽度

        Returns:
            当前区域左侧的新区域对象
        """
        if width is None:
            return Region(self._raw.left())  # type: ignore
        return Region(self._raw.left(width))  # type: ignore

    def right(self, width: Optional[int] = None) -> Region:
        """
        创建当前区域右侧的新区域。

        Args:
            width: 新区域的宽度，默认为当前区域宽度

        Returns:
            当前区域右侧的新区域对象
        """
        if width is None:
            return Region(self._raw.right())  # type: ignore
        return Region(self._raw.right(width))  # type: ignore

    def nearby(self, range: int = 50) -> Region:
        """
        创建当前区域周围扩展的新区域。

        Args:
            range: 向四周扩展的像素数，默认为 50

        Returns:
            扩展后的新区域对象
        """
        return Region(self._raw.nearby(range))  # type: ignore

    def grow(self, range: int = 50) -> Region:
        """
        扩展当前区域（向四周扩展指定像素）。

        Args:
            range: 向四周扩展的像素数，默认为 50

        Returns:
            扩展后的新区域对象
        """
        return Region(self._raw.grow(range))  # type: ignore

    def __repr__(self) -> str:
        """
        返回对象的字符串表示。

        Returns:
            对象的字符串表示
        """
        return f'<class {self.__class__.__name__} at {hex(id(self))}, [{self.x},{self.y} {self.w}x{self.h}]>'


class Match(Region):
    """
    Match 类表示图像匹配成功后返回的结果，包含匹配区域的位置和置信度信息。
    """

    @classmethod
    def new_by_score(cls, x: int, y: int, w: int, h: int, score: float):
        return cls(get_cli().Match(get_cli().Region(x, y, w, h), score))  # type: ignore

    def get_target(self) -> Location:
        """
        获取将用作点击点的 Location 对象。

        Returns:
            匹配目标的位置对象
        """
        return self._raw.getTarget()  # type: ignore

    def get_score(self) -> float:
        """
        获取匹配的相似度评分。

        Returns:
            匹配分数，范围 0.0-1.0
        """
        return self._raw.getScore()  # type: ignore

    def __lt__(self, other: Match) -> bool:
        """
        比较两个 Match 对象的分数（小于）。

        Args:
            other: 另一个 Match 对象

        Returns:
            当前分数是否小于另一个
        """
        return self.get_score() < other.get_score()

    def __le__(self, other: Match) -> bool:
        """
        比较两个 Match 对象的分数（小于等于）。

        Args:
            other: 另一个 Match 对象

        Returns:
            当前分数是否小于等于另一个
        """
        return self.get_score() <= other.get_score()

    def __gt__(self, other: Match) -> bool:
        """
        比较两个 Match 对象的分数（大于）。

        Args:
            other: 另一个 Match 对象

        Returns:
            当前分数是否大于另一个
        """
        return self.get_score() > other.get_score()

    def __ge__(self, other: Match) -> bool:
        """
        比较两个 Match 对象的分数（大于等于）。

        Args:
            other: 另一个 Match 对象

        Returns:
            当前分数是否大于等于另一个
        """
        return self.get_score() >= other.get_score()

    def __eq__(self, other: object) -> bool:
        """
        比较两个 Match 对象的分数（等于）。

        Args:
            other: 另一个 Match 对象

        Returns:
            当前分数是否等于另一个
        """
        if not isinstance(other, Match):
            raise ValueError("the 'Match' class cannot be compared with other classes.")
        return self.get_score() == other.get_score()

    def __repr__(self) -> str:
        """
        返回对象的字符串表示。

        Returns:
            对象的字符串表示
        """
        return f'<class {self.__class__.__name__} at {hex(id(self))}, [{self.x},{self.y} {self.w}x{self.h}] S:{self.get_score():.4f}>'


class ObserveEvent:
    """
    当区域内的观测事件发生时，若注册的 Region.onAppear() 、 Region.onVanish() 或 Region.onChange() 事件之一被触发，系统将调用对应的处理函数
    """

    def __init__(self, java_instance):
        raise NotImplementedError()


if __name__ == '__main__':
    # 示例代码 - Region 类测试示例

    import pathlib
    import time

    from py_sikulix.keys import Btn, Key

    # ============================================
    # 第一部分: Region 基础操作示例
    print('=' * 60)
    print('第一部分: Region 基础操作示例')
    print('=' * 60)

    # 示例1: 创建 Region 对象
    region = Region(100, 100, 300, 200)
    print(f'创建区域: 位置({region.x}, {region.y}), 大小({region.w}x{region.h})')
    # # 示例2: 获取和设置 Region 属性
    # bounds = region.get_bounds()
    # print(f'区域边界: x={bounds[0]}, y={bounds[1]}, w={bounds[2]}, h={bounds[3]}')
    # center = region.get_center()
    # print(f'区域中心: ({center.x}, {center.y})')
    # # 示例3: 修改 Region 属性（链式调用）
    # region.set_x(200).set_y(150).set_w(400).set_h(300)
    # print(f'改后区域: 位置({region.x}, {region.y}), 大小({region.w}x{region.h})')
    # region.set_rect(50, 50, 500, 400)
    # print(f'set_rect后: 位置({region.x}, {region.y}), 大小({region.w}x{region.h})')
    # print(
    #     f'左上角位置点：{region.get_top_left()}，左下角位置点：{region.get_bottom_left()}，右上角位置点：{region.get_top_right()}，右上角位置点：{region.get_bottom_right()}，'
    # )
    # region.set_roi(10, 10, 200, 100)
    # print('设置ROI区域')
    # # 示例4: Region 创建方法（above, below, left, right, nearby, grow）
    # new_region = Region(0, 0, 300, 300)
    # print(f'基础区域: ({new_region.x}, {new_region.y}), {new_region.w}x{new_region.h}')
    # above_region = new_region.above(50)
    # print(f'上方区域: ({above_region.x}, {above_region.y}), {above_region.w}x{above_region.h}')
    # below_region = new_region.below(50)
    # print(f'下方区域: ({below_region.x}, {below_region.y}), {below_region.w}x{below_region.h}')
    # left_region = new_region.left(50)
    # print(f'左侧区域: ({left_region.x}, {left_region.y}), {left_region.w}x{left_region.h}')
    # right_region = new_region.right(50)
    # print(f'右侧区域: ({right_region.x}, {right_region.y}), {right_region.w}x{right_region.h}')
    # grown_region = new_region.grow(25)
    # print(f'扩展区域: ({grown_region.x}, {grown_region.y}), {grown_region.w}x{grown_region.h}')
    # new_region.highlight()
    # print(f'高亮当前区域: {new_region}')

    # # 第二部分: Region 交互操作示例
    # print('=' * 60)
    # print('第二部分: Region 鼠标操作示例')
    # print('=' * 60)
    # # 示例1: 点击类操作
    # print(f'点击区域中心：{region.click()}')
    # time.sleep(1)
    # print(f'左键点击区域图像：{region.click(Pattern("examples/RecycleBin.png"))}')
    # time.sleep(1)
    print(f'右键点击区域中心（无效）：{region.click(key=Btn.RIGHT)}')
    # time.sleep(1)
    # print(f'双击区域图像：{region.double_click()}')
    # time.sleep(1)
    # print(f'右键点击区域图像：{region.right_click(Pattern("examples/RecycleBin.png"))}')
    # time.sleep(1)
    # print('点击100,100位置：region.click(Location(100, 100))')
    # time.sleep(1)
    # match = region.find_multi_color(
    #     'f9fafb|030303,-9|10|7885e2|030303,-3|25|5e41c9|030303,-4|11|5950d9|030303,-1|10|5750d9|030303,-11|31|e4ddf6|030303,9|14|38cfdb|030303'
    # )
    # if match:
    #     print(f'找到匹配项：{match}')
    # else:
    #     print('未找到匹配项')

    # # 示例2: 移动类操作
    # print(f'移动鼠标到目标图像：{region.hover(Pattern("examples/RecycleBin.png"))}')
    # time.sleep(1)
    # print(f'拖动到目标位置：{region.drag_drop(Pattern("examples/RecycleBin.png"), Location(200, 200))}')
    # time.sleep(1)
    # print(f'左键按下（不松开）：{region.mouse_down()}')
    # time.sleep(1)
    # print(f'鼠标移动相对当前点30,30位置：{region.mouse_move(30, 30)}')
    # time.sleep(1)
    # print(f'左键松开：{region.mouse_up()}')
    # time.sleep(1)
    # print(f'鼠标移动指定100,100位置：{region.mouse_move(Location(100, 100))}')
    # time.sleep(1)
    # print(f'右键按下（不松开）：{region.mouse_down(Btn.RIGHT)}')
    # time.sleep(1)
    # print(f'右键松开：{region.mouse_up(Btn.RIGHT)}')
    # time.sleep(1)
    # print(f'鼠标滚动：{region.wheel(Location(600, 600))}')
    # time.sleep(1)

    # # # 示例3: 键盘类操作
    print(f'按键按下（无效）：{region.key_down(Key.WIN)}')
    print(f'组合按键：{region.type("r")}')
    print(f'按键松开（无效）：{region.key_up(Key.WIN)}')
    # time.sleep(1)
    # print(f'输入文本：{region.type("notepad")}')
    # print(f'输入文本（无效）：{region.type(Key.ENTER)}')
    # time.sleep(1)
    # print(f'粘贴文本：{region.paste("你好中国，See u")}')
    # time.sleep(1)
    # print(f'文本提取（效果差）：{region.text()}')
    # time.sleep(1)

    # new_region.highlight_all_off()

    # 示例代码 - Match 类测试示例
    # from py_sikulix.screen import Screen

    # # 创建屏幕实例
    # screen = Screen()

    # # ============================================
    # # 示例1: 查找图像并获取 Match 对象
    # print('=' * 50)
    # print('示例1: 查找图像并获取 Match 对象')
    # print('=' * 50)

    # # 查找图像（需要先准备好测试图像）
    # image_path = pathlib.Path('examples/RecycleBin.png')
    # print('图像状态：', image_path.exists(), image_path.absolute())
    # match = screen.find(image_path)

    # if match:
    #     print(f'找到匹配！左上角坐标: ({match.x}, {match.y}), 大小: {match.w}x{match.h}')
    # else:
    #     print('未找到匹配')

    # # ============================================
    # # 示例2: 获取匹配分数 (get_score)
    # print('\n' + '=' * 50)
    # print('示例2: 获取匹配分数')
    # print('=' * 50)

    # if match:
    #     score = match.get_score()
    #     print(f'匹配分数: {score:.4f} (范围 0.0-1.0)')

    #     if score > 0.9:
    #         print('高置信度匹配！')
    #     elif score > 0.7:
    #         print('中等置信度匹配')
    #     else:
    #         print('低置信度匹配')

    # # ============================================
    # # 示例3: 获取点击目标位置 (get_target)
    # print('\n' + '=' * 50)
    # print('示例3: 获取点击目标位置')
    # print('=' * 50)

    # if match:
    #     target = match.get_target()
    #     print(f'点击目标位置: ({target.x}, {target.y})')

    # # ============================================
    # # 示例4: Match 继承自 Region 的属性和方法
    # print('\n' + '=' * 50)
    # print('示例4: Match 继承自 Region 的属性')
    # print('=' * 50)

    # if match:
    #     print(f'区域左上角: ({match.x}, {match.y})')
    #     print(f'区域大小: {match.w} x {match.h}')

    #     center = match.get_center()
    #     print(f'区域中心: ({center.x}, {center.y})')

    # # ============================================
    # # 示例5: 比较运算符 - 比较两个 Match 的分数
    # print('\n' + '=' * 50)
    # print('示例5: 比较运算符')
    # print('=' * 50)

    # match_raw = screen.find('examples/RecycleBin.png')
    # match_trn = screen.find('examples/RecycleBin_Transparent.png')
    # print(match_raw, match_trn)

    # if match_raw and match_trn:
    #     score1 = match_raw.get_score()
    #     score2 = match_trn.get_score()

    #     print(f'MatchRaw 分数: {score1:.4f}')
    #     print(f'MatchRrn 分数: {score2:.4f}')

    #     if match_raw > match_trn:
    #         print('MatchRaw 的分数更高 (MatchRaw > MatchRrn)')
    #     elif match_raw < match_trn:
    #         print('MatchRrn 的分数更高 (MatchRaw < MatchRrn)')
    #     else:
    #         print('两个匹配分数相同 (MatchRaw == MatchRrn)')

    #     print(f'MatchRaw >= MatchRrn: {match_raw >= match_trn}')
    #     print(f'MatchRaw <= MatchRrn: {match_raw <= match_trn}')

    # # ============================================
    # # 示例6: 使用 find_all 获取多个 Match 并排序
    # print('\n' + '=' * 50)
    # print('示例6: 获取多个匹配并按分数排序')
    # print('=' * 50)

    # matches = screen.find_all('examples/RecycleBin_Transparent.png')
    # if matches:
    #     print(f'找到 {len(matches)} 个匹配')

    #     sorted_matches = sorted(matches, key=lambda m: m.get_score(), reverse=True)

    #     for i, m in enumerate(sorted_matches):
    #         print(f'匹配 {i + 1}: 分数={m.get_score():.4f}, 位置=({m.x}, {m.y})')

    #     best_match = sorted_matches[0]
    #     print(f'\n最佳匹配: 分数={best_match.get_score():.4f}')

    # # ============================================
    # # 示例7: Match 与 Pattern 配合使用
    # print('\n' + '=' * 50)
    # print('示例7: Match 与 Pattern 配合使用')
    # print('=' * 50)

    # pattern = Pattern('examples/RecycleBin_Transparent.png').set_similar(0.9)

    # match = screen.find(pattern)
    # if match:
    #     print(f'使用 Pattern 找到匹配，分数: {match.get_score():.4f}，位置: ({match.x}, {match.y})')
    #     match.click()
    # print('\n所有示例完成！')

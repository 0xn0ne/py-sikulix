from __future__ import annotations

import contextlib
import logging
import pathlib
import time
from typing import Optional, Union

from py4j.java_gateway import JavaObject
from py4j.protocol import Py4JJavaError

from py_sikulix.base_region import BaseRegion
from py_sikulix.client import CLIENT
from py_sikulix.location import Location
from py_sikulix.match import Match
from py_sikulix.pattern import Pattern

logger = logging.getLogger(__name__)


class Region(BaseRegion):
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
            x_or_java_obj = CLIENT.Region(x_or_java_obj, y, w, h)  # type: ignore
        if not isinstance(x_or_java_obj, JavaObject):
            raise ValueError(
                'please pass in the correct types of x, y, w, h parameters. do not directly pass in JavaObject to create the Class.'
            )
        super().__init__(x_or_java_obj)

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
            目标消失返回 True，超时返回 False
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
            if not result:
                return True
            if current_time + timeout < time.time():
                break
            time.sleep(0.2)
        return False

    def exists(self, target: Union[str, pathlib.Path, Pattern], timeout: float = 30.0) -> Optional[Match]:
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

        result = self._raw.exists(target, timeout)  # type: ignore
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
    # 示例2: 获取和设置 Region 属性
    bounds = region.get_bounds()
    print(f'区域边界: x={bounds[0]}, y={bounds[1]}, w={bounds[2]}, h={bounds[3]}')
    center = region.get_center()
    print(f'区域中心: ({center.x}, {center.y})')
    # 示例3: 修改 Region 属性（链式调用）
    region.set_x(200).set_y(150).set_w(400).set_h(300)
    print(f'改后区域: 位置({region.x}, {region.y}), 大小({region.w}x{region.h})')
    region.set_rect(50, 50, 500, 400)
    print(f'set_rect后: 位置({region.x}, {region.y}), 大小({region.w}x{region.h})')
    print(
        f'左上角位置点：{region.get_top_left()}，左下角位置点：{region.get_bottom_left()}，右上角位置点：{region.get_top_right()}，右上角位置点：{region.get_bottom_right()}，'
    )
    region.set_roi(10, 10, 200, 100)
    print('设置ROI区域')
    # 示例4: Region 创建方法（above, below, left, right, nearby, grow）
    new_region = Region(0, 0, 300, 300)
    print(f'基础区域: ({new_region.x}, {new_region.y}), {new_region.w}x{new_region.h}')
    above_region = new_region.above(50)
    print(f'上方区域: ({above_region.x}, {above_region.y}), {above_region.w}x{above_region.h}')
    below_region = new_region.below(50)
    print(f'下方区域: ({below_region.x}, {below_region.y}), {below_region.w}x{below_region.h}')
    left_region = new_region.left(50)
    print(f'左侧区域: ({left_region.x}, {left_region.y}), {left_region.w}x{left_region.h}')
    right_region = new_region.right(50)
    print(f'右侧区域: ({right_region.x}, {right_region.y}), {right_region.w}x{right_region.h}')
    grown_region = new_region.grow(25)
    print(f'扩展区域: ({grown_region.x}, {grown_region.y}), {grown_region.w}x{grown_region.h}')
    new_region.highlight()
    print(f'高亮当前区域: {new_region}')

    # 第二部分: Region 交互操作示例
    print('=' * 60)
    print('第二部分: Region 鼠标操作示例')
    print('=' * 60)
    # 示例1: 点击类操作
    print(f'点击区域中心：{new_region.click()}')
    time.sleep(1)
    print(f'左键点击区域图像：{new_region.click(Pattern("examples/RecycleBin.png"))}')
    time.sleep(1)
    print(f'右键点击区域中心（无效）：{new_region.click(key=Btn.RIGHT)}')
    time.sleep(1)
    print(f'双击区域图像：{new_region.double_click()}')
    time.sleep(1)
    print(f'右键点击区域图像：{new_region.right_click(Pattern("examples/RecycleBin.png"))}')
    time.sleep(1)
    print('点击100,100位置：new_region.click(Location(100, 100))')
    time.sleep(1)

    # 示例2: 移动类操作
    print(f'移动鼠标到目标图像：{new_region.hover(Pattern("examples/RecycleBin.png"))}')
    time.sleep(1)
    print(f'拖动到目标位置：{new_region.drag_drop(Pattern("examples/RecycleBin.png"), Location(200, 200))}')
    time.sleep(1)
    print(f'左键按下（不松开）：{new_region.mouse_down()}')
    time.sleep(1)
    print(f'鼠标移动相对当前点30,30位置：{new_region.mouse_move(30, 30)}')
    time.sleep(1)
    print(f'左键松开：{new_region.mouse_up()}')
    time.sleep(1)
    print(f'鼠标移动指定100,100位置：{new_region.mouse_move(Location(100, 100))}')
    time.sleep(1)
    print(f'右键按下（不松开）：{new_region.mouse_down(Btn.RIGHT)}')
    time.sleep(1)
    print(f'右键松开：{new_region.mouse_up(Btn.RIGHT)}')
    time.sleep(1)
    print(f'鼠标滚动：{new_region.wheel(Location(600, 600))}')
    time.sleep(1)

    # # 示例3: 键盘类操作
    print(f'按键按下（无效）：{new_region.key_down(Key.WIN)}')
    print(f'组合按键：{new_region.type("r")}')
    print(f'按键松开（无效）：{new_region.key_up(Key.WIN)}')
    time.sleep(1)
    print(f'输入文本：{new_region.type("notepad")}')
    print(f'输入文本（无效）：{new_region.type(Key.ENTER)}')
    time.sleep(1)
    print(f'粘贴文本：{new_region.paste("你好中国，See u")}')
    time.sleep(1)
    print(f'文本提取（效果差）：{new_region.text()}')
    time.sleep(1)

    new_region.highlight_all_off()

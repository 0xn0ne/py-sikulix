#!/usr/bin/env python3

#
"""Location 类 - 屏幕坐标点。"""

from typing import Optional, Union

from py4j.java_gateway import JavaObject

from py_sikulix.client import CLIENT


class Location:
    """Location 类表示屏幕上的一个点坐标 (x, y)。"""

    def __init__(self, x_or_java_obj: Union[JavaObject, int], y: Optional[int] = None):
        """
        创建一个 Location 对象。

        Args:
            x_or_java_obj: X 轴坐标或Java 对象，用于创建 Location 对象。
            y: Y 轴坐标
        """
        if isinstance(x_or_java_obj, int) and isinstance(y, int):
            x_or_java_obj = CLIENT.Location(x_or_java_obj, y)  # type: ignore
        if not isinstance(x_or_java_obj, JavaObject):
            raise ValueError(
                'please pass in the correct types of x, y parameters. do not directly pass in JavaObject to create the Class.'
            )
        self._raw: JavaObject = x_or_java_obj  # type: ignore

    @property
    def x(self) -> int:
        """
        获取 X 坐标。

        Returns:
            X 坐标值
        """
        return self._raw.getX()  # type: ignore

    @property
    def y(self) -> int:
        """
        获取 Y 坐标。

        Returns:
            Y 坐标值
        """
        return self._raw.getY()  # type: ignore

    def get_x(self) -> int:
        """
        获取 X 坐标。

        Returns:
            X 坐标值
        """
        return self._raw.getX()  # type: ignore

    def get_y(self) -> int:
        """
        获取 Y 坐标。

        Returns:
            Y 坐标值
        """
        return self._raw.getY()  # type: ignore

    def offset(self, dx: int, dy: int) -> 'Location':
        """
        获取偏移后的新位置。

        Args:
            dx: X 轴偏移量
            dy: Y 轴偏移量

        Returns:
            新的 Location 对象
        """
        return Location(self._raw.offset(dx, dy))  # type: ignore

    def above(self, d: int) -> 'Location':
        """
        获取上方指定距离的位置。

        Args:
            d: 距离

        Returns:
            上方的新位置
        """
        return Location(self._raw.above(d))  # type: ignore

    def below(self, d: int) -> 'Location':
        """
        获取下方指定距离的位置。

        Args:
            d: 距离

        Returns:
            下方的新位置
        """
        return Location(self._raw.below(d))  # type: ignore

    def left(self, d: int) -> 'Location':
        """
        获取左侧指定距离的位置。

        Args:
            d: 距离

        Returns:
            左侧的新位置
        """
        return Location(self._raw.left(d))  # type: ignore

    def right(self, d: int) -> 'Location':
        """
        获取右侧指定距离的位置。

        Args:
            d: 距离

        Returns:
            右侧的新位置
        """
        return Location(self._raw.right(d))  # type: ignore

    def __repr__(self) -> str:
        """
        返回对象的字符串表示。

        Returns:
            对象的字符串表示
        """
        return f'<class {self.__class__.__name__} at {hex(id(self))}, [{self.x},{self.y}]>'


if __name__ == '__main__':
    loc = Location(100, 200)
    print(f'初始位置: ({loc.x}, {loc.y})')

    offset_loc = loc.offset(50, 30)
    print(f'右偏50，下偏30后位置: ({offset_loc.x}, {offset_loc.y})')

    above_loc = loc.above(50)
    print(f'上方50像素位置: ({above_loc.x}, {above_loc.y})')

    below_loc = loc.below(50)
    print(f'下方50像素位置: ({below_loc.x}, {below_loc.y})')

    left_loc = loc.left(50)
    print(f'左侧50像素位置: ({left_loc.x}, {left_loc.y})')

    right_loc = loc.right(50)
    print(f'右侧50像素位置: ({right_loc.x}, {right_loc.y})')

    print(f'打印对象：{loc}')

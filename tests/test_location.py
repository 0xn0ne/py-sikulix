#!/usr/bin/env python3
"""
Location 类集成测试

这些测试需要 SikuliX 网关运行。
测试会自动启动网关（如未运行），测试完成后自动停止。
"""

import pytest

from py_sikulix import Location


class TestLocationCreation:
    """Location 创建测试"""

    def test_create_location(self):
        """测试创建 Location"""
        loc = Location(100, 200)

        assert isinstance(loc, Location)
        assert loc.x == 100
        assert loc.y == 200

    def test_location_properties(self, location):
        """测试 Location 属性"""
        assert hasattr(location, "x")
        assert hasattr(location, "y")

    def test_get_x(self, location):
        """测试获取 X 坐标"""
        assert location.get_x() == location.x

    def test_get_y(self, location):
        """测试获取 Y 坐标"""
        assert location.get_y() == location.y


class TestLocationOffset:
    """Location 偏移测试"""

    def test_offset_positive(self, location):
        """测试正向偏移"""
        new_loc = location.offset(50, 30)

        assert isinstance(new_loc, Location)
        assert new_loc.x == location.x + 50
        assert new_loc.y == location.y + 30

    def test_offset_negative(self, location):
        """测试负向偏移"""
        new_loc = location.offset(-20, -10)

        assert isinstance(new_loc, Location)
        assert new_loc.x == location.x - 20
        assert new_loc.y == location.y - 10

    def test_offset_zero(self, location):
        """测试零偏移"""
        new_loc = location.offset(0, 0)

        assert isinstance(new_loc, Location)
        assert new_loc.x == location.x
        assert new_loc.y == location.y


class TestLocationDirection:
    """Location 方向测试"""

    def test_above(self, location):
        """测试上方位置"""
        above = location.above(50)

        assert isinstance(above, Location)
        # 上方的 y 应该小于原位置
        assert above.y < location.y

    def test_below(self, location):
        """测试下方位置"""
        below = location.below(50)

        assert isinstance(below, Location)
        # 下方的 y 应该大于原位置
        assert below.y > location.y

    def test_left(self, location):
        """测试左侧位置"""
        left = location.left(50)

        assert isinstance(left, Location)
        # 左侧的 x 应该小于原位置
        assert left.x < location.x

    def test_right(self, location):
        """测试右侧位置"""
        right = location.right(50)

        assert isinstance(right, Location)
        # 右侧的 x 应该大于原位置
        assert right.x > location.x


class TestLocationChain:
    """Location 链式调用测试"""

    def test_chain_operations(self, location):
        """测试链式操作"""
        result = location.offset(10, 20).right(30).below(40)

        assert isinstance(result, Location)
        assert result.x == location.x + 10 + 30
        assert result.y == location.y + 20 + 40


class TestLocationRepr:
    """Location 字符串表示测试"""

    def test_repr(self, location):
        """测试 repr"""
        repr_str = repr(location)

        assert "Location" in repr_str
        assert str(location.x) in repr_str
        assert str(location.y) in repr_str

    def test_str(self, location):
        """测试 str"""
        str_val = str(location)

        assert str(location.x) in str_val
        assert str(location.y) in str_val

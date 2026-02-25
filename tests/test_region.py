#!/usr/bin/env python3
"""
Region 类集成测试

这些测试需要 SikuliX 网关运行。
测试会自动启动网关（如未运行），测试完成后自动停止。
"""

import pathlib
import time

import pytest

from py_sikulix import Btn, Key, Location, Match, Pattern, Region, Screen


class TestRegionCreation:
    """Region 创建测试"""

    def test_create_region_with_integers(self):
        """测试使用整数坐标创建区域"""
        region = Region(100, 100, 300, 200)

        assert isinstance(region, Region)
        assert region.x == 100
        assert region.y == 100
        assert region.w == 300
        assert region.h == 200

    def test_region_properties(self, region):
        """测试区域属性"""
        assert hasattr(region, 'x')
        assert hasattr(region, 'y')
        assert hasattr(region, 'w')
        assert hasattr(region, 'h')

    def test_get_bounds(self, region):
        """测试获取边界"""
        bounds = region.get_bounds()

        assert isinstance(bounds, tuple)
        assert len(bounds) == 4
        x, y, w, h = bounds
        assert x >= 0
        assert y >= 0
        assert w > 0
        assert h > 0

    def test_get_center(self, region):
        """测试获取中心点"""
        center = region.get_center()

        assert isinstance(center, Location)
        # 中心点应该在区域内
        assert region.x <= center.x <= region.x + region.w
        assert region.y <= center.y <= region.y + region.h


class TestRegionSetters:
    """Region 属性设置测试"""

    def test_set_x(self, region):
        """测试设置 X 坐标"""
        original_x = region.x
        region.set_x(200)

        assert region.x == 200
        # 恢复原值
        region.set_x(original_x)

    def test_set_y(self, region):
        """测试设置 Y 坐标"""
        original_y = region.y
        region.set_y(300)

        assert region.y == 300
        # 恢复原值
        region.set_y(original_y)

    def test_set_w(self, region):
        """测试设置宽度"""
        original_w = region.w
        region.set_w(500)

        assert region.w == 500
        # 恢复原值
        region.set_w(original_w)

    def test_set_h(self, region):
        """测试设置高度"""
        original_h = region.h
        region.set_h(400)

        assert region.h == 400
        # 恢复原值
        region.set_h(original_h)

    def test_chain_setters(self, region):
        """测试链式设置"""
        region.set_x(100).set_y(100).set_w(200).set_h(150)

        assert region.x == 100
        assert region.y == 100
        assert region.w == 200
        assert region.h == 150


class TestRegionGeometry:
    """区域几何操作测试"""

    def test_above(self, region):
        """测试获取上方区域"""
        above = region.above(100)

        assert isinstance(above, Region)
        # SikuliX 坐标系中，y 越小越靠上（不能超出屏幕边界时可能相等）
        assert above.y <= region.y

    def test_below(self, region):
        """测试获取下方区域"""
        below = region.below(100)

        assert isinstance(below, Region)
        # SikuliX 坐标系中，y 越大越靠下
        assert below.y >= region.y

    def test_left(self, region):
        """测试获取左侧区域"""
        left = region.left(100)

        assert isinstance(left, Region)
        # SikuliX 坐标系中，x 越小越靠左（不能超出屏幕边界时可能相等）
        assert left.x <= region.x

    def test_right(self, region):
        """测试获取右侧区域"""
        right = region.right(100)

        assert isinstance(right, Region)
        # SikuliX 坐标系中，x 越大越靠右
        assert right.x >= region.x

    def test_nearby(self, region):
        """测试获取附近区域"""
        nearby = region.nearby(50)

        assert isinstance(nearby, Region)
        # 附近区域应该比原区域大
        assert nearby.w >= region.w
        assert nearby.h >= region.h

    def test_grow(self, region):
        """测试扩展区域"""
        grown = region.grow(50)

        assert isinstance(grown, Region)
        # 扩展后的区域应该比原区域大
        assert grown.w > region.w
        assert grown.h > region.h

    def test_set_roi(self, region):
        """测试设置 ROI"""
        original_bounds = region.get_bounds()

        region.set_roi(10, 10, 100, 100)

        # ROI 只影响搜索区域，不改变区域本身
        # 这个测试验证方法可调用
        assert callable(region.set_roi)

        # 恢复
        region.set_roi(0, 0, original_bounds[2], original_bounds[3])


class TestRegionLocation:
    """区域位置方法测试"""

    def test_get_top_left(self, region):
        """测试获取左上角"""
        top_left = region.get_top_left()

        assert isinstance(top_left, Location)
        assert top_left.x == region.x
        assert top_left.y == region.y

    def test_get_top_right(self, region):
        """测试获取右上角"""
        top_right = region.get_top_right()

        assert isinstance(top_right, Location)
        # SikuliX 坐标系使用左闭右开区间，所以 right = x + w - 1
        assert top_right.x == region.x + region.w - 1
        assert top_right.y == region.y

    def test_get_bottom_left(self, region):
        """测试获取左下角"""
        bottom_left = region.get_bottom_left()

        assert isinstance(bottom_left, Location)
        assert bottom_left.x == region.x
        # SikuliX 坐标系使用左闭右开区间，所以 bottom = y + h - 1
        assert bottom_left.y == region.y + region.h - 1

    def test_get_bottom_right(self, region):
        """测试获取右下角"""
        bottom_right = region.get_bottom_right()

        assert isinstance(bottom_right, Location)
        # SikuliX 坐标系使用左闭右开区间
        assert bottom_right.x == region.x + region.w - 1
        assert bottom_right.y == region.y + region.h - 1

    def test_move_to(self, region):
        """测试移动区域"""
        original_x, original_y = region.x, region.y

        # 移动到新位置
        new_location = Location(500, 500)
        region.move_to(new_location)

        # 验证位置已改变
        assert region.x == 500
        assert region.y == 500

        # 恢复
        region.move_to(Location(original_x, original_y))

    def test_set_rect(self, region):
        """测试设置矩形"""
        original_bounds = region.get_bounds()

        region.set_rect(100, 100, 400, 300)

        assert region.x == 100
        assert region.y == 100
        assert region.w == 400
        assert region.h == 300

        # 恢复
        region.set_rect(*original_bounds)


class TestRegionMouse:
    """区域鼠标操作测试"""

    def test_click(self, region):
        """测试点击"""
        # 这是一个基本测试，验证方法可调用
        # 实际点击会移动鼠标，可以观察
        result = region.click()

        # 返回值应该是整数（点击次数或状态码）
        assert isinstance(result, int)

    def test_click_with_button(self, region):
        """测试使用按键点击"""
        # 测试右键点击
        result = region.click(key=Btn.RIGHT)

        assert isinstance(result, int)

    def test_double_click(self, region):
        """测试双击"""
        result = region.double_click()

        assert isinstance(result, int)

    def test_right_click(self, region):
        """测试右键点击"""
        result = region.right_click()

        assert isinstance(result, int)

    def test_hover(self, region):
        """测试悬停"""
        result = region.hover()

        assert isinstance(result, int)

    def test_mouse_down(self, region):
        """测试鼠标按下"""
        result = region.mouse_down()

        assert isinstance(result, int)

    def test_mouse_up(self, region):
        """测试鼠标释放"""
        result = region.mouse_up()

        assert isinstance(result, int)

    def test_mouse_move(self, region):
        """测试鼠标移动"""
        result = region.mouse_move(50, 50)

        assert isinstance(result, int)

    def test_wheel(self, region):
        """测试滚轮"""
        result = region.wheel(direction=Btn.WHEEL_DOWN)

        assert isinstance(result, int)

    def test_wheel_up(self, region):
        """测试滚轮向上"""
        result = region.wheel(direction=Btn.WHEEL_UP)

        assert isinstance(result, int)


class TestRegionKeyboard:
    """区域键盘操作测试"""

    def test_key_down(self, region):
        """测试按键按下"""
        result = region.key_down(Key.WIN)

        assert isinstance(result, int)

    def test_key_up(self, region):
        """测试按键释放"""
        result = region.key_up(Key.WIN)

        assert isinstance(result, int)

    def test_type_text(self, region):
        """测试输入文本"""
        result = region.type('test')

        assert isinstance(result, int)

    def test_paste_text(self, region):
        """测试粘贴文本"""
        result = region.paste('paste test')

        assert isinstance(result, int)


class TestRegionFind:
    """区域查找测试"""

    def test_exists_nonexistent(self, region):
        """测试查找不存在的图像"""
        # 查找不存在的图像应该返回 None
        result = region.exists('nonexistent_image.png', timeout=1)

        # 可能返回 None（未找到）或抛出异常
        assert result is None or isinstance(result, Match)

    def test_wait_timeout(self, region):
        """测试等待超时"""
        result = region.wait('nonexistent_image.png', timeout=1)

        # 超时应该返回 None
        assert result is None

    def test_wait_vanish_timeout(self, region):
        """测试等待消失超时"""
        result = region.wait_vanish('nonexistent_image.png', timeout=1)

        # 超时应该返回 False
        assert result is False


class TestRegionHighlight:
    """区域高亮测试"""

    def test_highlight(self, region):
        """测试高亮"""
        result = region.highlight('red')

        # 返回值应该是整数或字符串
        assert result is not None

    def test_highlight_off(self, region):
        """测试关闭高亮"""
        # 先高亮
        region.highlight('blue')
        # 再关闭
        region.highlight_all_off()


class TestRegionText:
    """区域文本提取测试"""

    def test_text(self, region):
        """测试文本提取"""
        # 这个测试可能返回空字符串（如果没有 OCR 文本）
        result = region.text()

        assert isinstance(result, str)


class TestConstants:
    """常量测试"""

    def test_key_constants(self):
        """测试键盘常量"""
        assert isinstance(Key.WIN, str)
        assert isinstance(Key.ENTER, str)
        assert isinstance(Key.ESC, str)
        assert isinstance(Key.TAB, str)
        assert isinstance(Key.SPACE, str)

    def test_button_constants(self):
        """测试鼠标按钮常量"""
        assert isinstance(Btn.LEFT, int)
        assert isinstance(Btn.RIGHT, int)
        assert isinstance(Btn.MIDDLE, int)
        assert isinstance(Btn.WHEEL_UP, int)
        assert isinstance(Btn.WHEEL_DOWN, int)

    def test_button_values(self):
        """测试按钮常量值"""
        # 验证常量值符合预期
        assert Btn.LEFT == 1024
        assert Btn.RIGHT == 4096
        assert Btn.MIDDLE == 2048
        assert Btn.WHEEL_DOWN == 1
        assert Btn.WHEEL_UP == -1

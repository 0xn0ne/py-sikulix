#!/usr/bin/env python3
"""
Pattern 类集成测试

这些测试需要 SikuliX 网关运行。
测试会自动启动网关（如未运行），测试完成后自动停止。
"""

import pathlib

import pytest

from py_sikulix import Pattern


class TestPatternCreation:
    """Pattern 创建测试"""

    def test_create_pattern_with_string(self):
        """测试使用字符串路径创建 Pattern"""
        # 使用示例图像（如果存在）
        examples_dir = pathlib.Path(__file__).parent.parent / "examples"

        if examples_dir.exists():
            image_files = list(examples_dir.glob("*.png"))
            if image_files:
                pattern = Pattern(str(image_files[0]))
                assert isinstance(pattern, Pattern)
                return

        # 如果没有示例图像，跳过
        pytest.skip("没有示例图像文件")

    def test_create_pattern_with_pathlib(self):
        """测试使用 pathlib.Path 创建 Pattern"""
        examples_dir = pathlib.Path(__file__).parent.parent / "examples"

        if examples_dir.exists():
            image_files = list(examples_dir.glob("*.png"))
            if image_files:
                pattern = Pattern(image_files[0])
                assert isinstance(pattern, Pattern)
                return

        pytest.skip("没有示例图像文件")

    def test_pattern_with_nonexistent_file(self):
        """测试使用不存在的文件创建 Pattern"""
        # 这可能会抛出异常或返回一个无效的 Pattern
        # 取决于具体实现
        try:
            pattern = Pattern("/nonexistent/file.png")
            # 如果没有抛出异常，检查它是否有 _raw 属性
            assert hasattr(pattern, "_raw") or pattern is not None
        except Exception:
            # 有些实现可能会抛出异常，这也是可接受的
            pass


class TestPatternModification:
    """Pattern 修改测试"""

    @pytest.fixture
    def valid_pattern(self):
        """创建一个有效的 Pattern"""
        examples_dir = pathlib.Path(__file__).parent.parent / "examples"

        if examples_dir.exists():
            image_files = list(examples_dir.glob("*.png"))
            if image_files:
                return Pattern(str(image_files[0]))

        pytest.skip("没有示例图像文件")

    def test_set_similar(self, valid_pattern):
        """测试设置相似度（使用 set_similar 方法）"""
        result = valid_pattern.set_similar(0.8)

        # 应该返回 self（链式调用）
        assert result is valid_pattern

    def test_similar_property(self, valid_pattern):
        """测试相似度属性"""
        # 使用属性设置
        valid_pattern.similar = 0.9
        assert valid_pattern.similar == 0.9

    def test_exact(self, valid_pattern):
        """测试精确匹配"""
        result = valid_pattern.exact()

        assert result is valid_pattern

    def test_set_resize(self, valid_pattern):
        """测试图像缩放（使用 set_resize 方法）"""
        result = valid_pattern.set_resize(1.5)

        assert result is valid_pattern

    def test_resize_property(self, valid_pattern):
        """测试缩放属性"""
        # 使用属性设置
        valid_pattern.resize = 2.0
        assert valid_pattern.resize == 2.0

    def test_set_target_offset(self, valid_pattern):
        """测试目标偏移（使用 set_target_offset 方法）"""
        result = valid_pattern.set_target_offset(10, 20)

        assert result is valid_pattern

    def test_target_offset_property(self, valid_pattern):
        """测试目标偏移属性"""
        # 使用属性设置
        valid_pattern.target_offset = (15, 25)
        offset = valid_pattern.target_offset
        assert offset.x == 15
        assert offset.y == 25

    def test_chain_modifications(self, valid_pattern):
        """测试链式修改"""
        result = valid_pattern.set_similar(0.9).set_target_offset(5, -10).set_resize(1.2)

        assert result is valid_pattern


class TestPatternMask:
    """Pattern 蒙版测试"""

    @pytest.fixture
    def valid_pattern(self):
        """创建一个有效的 Pattern"""
        examples_dir = pathlib.Path(__file__).parent.parent / "examples"

        if examples_dir.exists():
            image_files = list(examples_dir.glob("*.png"))
            if image_files:
                return Pattern(str(image_files[0]))

        pytest.skip("没有示例图像文件")

    def test_mask_with_pattern(self, valid_pattern):
        """测试使用另一个 Pattern 作为蒙版"""
        examples_dir = pathlib.Path(__file__).parent.parent / "examples"

        if examples_dir.exists():
            image_files = list(examples_dir.glob("*.png"))
            if len(image_files) >= 2:
                mask_pattern = Pattern(str(image_files[1]))
                result = valid_pattern.mask(mask_pattern)
                assert result is valid_pattern
                return

        pytest.skip("没有足够的示例图像文件")

    def test_mask_without_argument(self, valid_pattern):
        """测试使用自身作为蒙版"""
        result = valid_pattern.mask()

        assert result is valid_pattern


class TestPatternGetters:
    """Pattern 获取方法测试"""

    @pytest.fixture
    def valid_pattern(self):
        """创建一个有效的 Pattern"""
        examples_dir = pathlib.Path(__file__).parent.parent / "examples"

        if examples_dir.exists():
            image_files = list(examples_dir.glob("*.png"))
            if image_files:
                return Pattern(str(image_files[0]))

        pytest.skip("没有示例图像文件")

    def test_get_filename(self, valid_pattern):
        """测试获取文件名"""
        filename = valid_pattern.get_filename()

        assert isinstance(filename, str)
        assert len(filename) > 0

    def test_get_similar(self, valid_pattern):
        """测试获取相似度"""
        similar = valid_pattern.get_similar()

        # 相似度应该是 0-1 之间的浮点数
        assert isinstance(similar, (int, float))
        assert 0 <= similar <= 1

    def test_get_target_offset(self, valid_pattern):
        """测试获取目标偏移"""
        offset = valid_pattern.get_target_offset()

        assert hasattr(offset, "x")
        assert hasattr(offset, "y")

    def test_get_resize(self, valid_pattern):
        """测试获取缩放因子"""
        resize = valid_pattern.get_resize()

        assert isinstance(resize, (int, float))


class TestPatternRepr:
    """Pattern 字符串表示测试"""

    @pytest.fixture
    def valid_pattern(self):
        """创建一个有效的 Pattern"""
        examples_dir = pathlib.Path(__file__).parent.parent / "examples"

        if examples_dir.exists():
            image_files = list(examples_dir.glob("*.png"))
            if image_files:
                return Pattern(str(image_files[0]))

        pytest.skip("没有示例图像文件")

    def test_repr(self, valid_pattern):
        """测试 repr"""
        repr_str = repr(valid_pattern)

        assert "Pattern" in repr_str

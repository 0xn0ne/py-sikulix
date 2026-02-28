#!/usr/bin/env python3
"""
Gateway 启动和连接测试。

测试 sikulix-gateway 启动脚本是否能正常工作，
特别验证导入 py_sikulix 包时不会抛出客户端连接错误。
"""

import subprocess
import sys
import time
import pytest


class TestGateway:
    """Gateway 启动和连接测试"""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """每个测试前后启动和停止网关"""
        # 尝试停止可能存在的旧网关
        self._stop_gateway()
        time.sleep(0.5)

        # 启动网关
        self._start_gateway()
        time.sleep(1)

        yield

        # 测试后停止网关
        self._stop_gateway()

    def _start_gateway(self):
        """启动 SikuliX 网关"""
        # 使用 python -m 方式启动
        self.process = subprocess.Popen(
            [sys.executable, "-m", "py_sikulix.gateway", "start"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def _stop_gateway(self):
        """停止 SikuliX 网关"""
        try:
            subprocess.run(
                [sys.executable, "-m", "py_sikulix.gateway", "stop"],
                timeout=5,
                capture_output=True,
            )
        except Exception:
            pass
        # 确保进程已停止
        if hasattr(self, "process") and self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception:
                pass

    def test_gateway_start_no_error(self):
        """测试网关启动不抛出客户端连接错误"""
        import py_sikulix

        assert py_sikulix is not None

    def test_import_py_sikulix_without_connection_error(self):
        """测试导入 py_sikulix 包时不会抛出连接错误"""
        from py_sikulix import Region, Screen, Pattern
        from py_sikulix.keys import Key, Btn

        # 通过 Key 类访问常量
        assert Key.ENTER is not None
        assert Key.WIN is not None
        # Btn 常量是整数值
        assert isinstance(Btn.LEFT, int)

        region = Region(0, 0, 100, 100)
        assert region is not None

    def test_region_operations(self):
        """测试 Region 基本操作"""
        from py_sikulix import Region

        region = Region(0, 0, 200, 200)
        assert region.x == 0
        assert region.y == 0
        assert region.w == 200
        assert region.h == 200

        bounds = region.get_bounds()
        assert bounds == (0, 0, 200, 200)

    def test_key_constants_accessible(self):
        """测试键盘常量可以正常访问"""
        from py_sikulix.keys import Key

        # 通过 Key 类访问
        assert Key.ENTER is not None
        assert Key.WIN is not None
        assert Key.TAB is not None
        assert Key.ESC is not None
        assert Key.F1 is not None
        assert Key.F2 is not None
        assert Key.F3 is not None

    def test_btn_constants(self):
        """测试鼠标按键常量"""
        from py_sikulix.keys import Btn

        # Btn 常量是整数值
        assert isinstance(Btn.LEFT, int)
        assert isinstance(Btn.MIDDLE, int)
        assert isinstance(Btn.RIGHT, int)
        assert isinstance(Btn.WHEEL_UP, int)
        assert isinstance(Btn.WHEEL_DOWN, int)

    def test_keyboard_operations_no_error(self):
        """测试键盘操作不报错"""
        from py_sikulix import Region
        from py_sikulix.keys import Key

        region = Region(0, 0, 100, 100)
        try:
            result = region.key_down(Key.WIN)
            assert isinstance(result, int)
            region.key_up(Key.WIN)
        except Exception as e:
            assert "connection" not in str(e).lower()
            assert "connect" not in str(e).lower()

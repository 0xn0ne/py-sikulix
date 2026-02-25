#!/usr/bin/env python3
"""
Pytest 配置文件

测试时会自动检测网关是否运行，如未运行则自动启动，测试完成后自动停止。
"""

import logging
import pathlib
import sys
import time

import pytest

# 添加 src 目录到 Python 路径
src_dir = pathlib.Path(__file__).parent.parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GatewayManager:
    """网关管理器 - 自动启动和停止网关"""

    _instance = None
    _gateway_launcher = None
    _owns_gateway = False  # 标记是否由测试启动的网关

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.port = 25333

    def is_gateway_running(self) -> bool:
        """检测网关是否正在运行"""
        from py4j.java_gateway import GatewayParameters, JavaGateway
        from py4j.protocol import Py4JNetworkError

        try:
            gateway = JavaGateway(gateway_parameters=GatewayParameters(port=self.port, auto_field=True))
            # 尝试调用一个简单的方法来验证连接
            screen = gateway.jvm.org.sikuli.script.Screen()  # type: ignore
            _ = screen.getNumberScreens()  # type: ignore
            gateway.close()
            return True
        except Py4JNetworkError:
            return False
        except Exception:
            return False

    def ensure_gateway(self) -> bool:
        """确保网关运行，如未运行则启动"""
        if self.is_gateway_running():
            logger.info('网关已在运行')
            self._owns_gateway = False
            return True

        logger.info('网关未运行，尝试启动...')
        try:
            from py_sikulix.gateway import SikuliXGateway

            self._gateway_launcher = SikuliXGateway(port=self.port)

            # 尝试查找 JAR 文件
            sikulix_jar = self._gateway_launcher.find_sikulix_jar()
            if not sikulix_jar:
                logger.error('未找到 SikuliX JAR 文件，请确保 sikulixide-2.0.5.2103.jar 在项目根目录')
                return False

            self._gateway_launcher.sikulix_path = sikulix_jar

            # 启动网关
            if not self._gateway_launcher.start():
                logger.error('网关启动失败')
                return False

            # 等待网关就绪
            for _ in range(10):
                time.sleep(0.5)
                if self.is_gateway_running():
                    logger.info('网关启动成功并已就绪')
                    self._owns_gateway = True
                    return True

            logger.error('网关启动后无法连接')
            return False

        except Exception as e:
            logger.error(f'启动网关时出错: {e}')
            return False

    def stop_gateway(self):
        """停止由测试启动的网关"""
        if self._owns_gateway and self._gateway_launcher:
            logger.info('停止测试启动的网关')
            self._gateway_launcher.stop()
            self._owns_gateway = False


# 创建全局网关管理器实例
gateway_manager = GatewayManager()


@pytest.fixture(scope='session', autouse=True)
def ensure_sikulix_gateway():
    """
    Session 级别的 fixture，确保测试开始时网关可用，测试结束后清理

    使用方式：
    - 如果网关已在运行，直接使用，不停止
    - 如果网关未运行，启动网关，测试结束后停止
    """
    logger.info('=' * 50)
    logger.info('准备测试环境...')

    # 确保网关运行
    if not gateway_manager.ensure_gateway():
        pytest.skip('无法启动 SikuliX 网关，跳过测试')

    logger.info('测试环境准备完成，开始测试')
    logger.info('=' * 50)

    # 运行所有测试
    yield

    # 测试完成后清理
    logger.info('=' * 50)
    logger.info('测试完成，清理环境...')
    gateway_manager.stop_gateway()
    logger.info('清理完成')
    logger.info('=' * 50)


@pytest.fixture
def screen():
    """创建 Screen 实例"""
    from py_sikulix import Screen

    return Screen()


@pytest.fixture
def region():
    """创建 Region 实例"""
    from py_sikulix import Region

    return Region(0, 0, 1920, 1080)


@pytest.fixture
def location():
    """创建 Location 实例"""
    from py_sikulix import Location

    return Location(100, 200)


@pytest.fixture
def pattern():
    """创建 Pattern 实例（使用示例图像）"""
    import pathlib

    from py_sikulix import Pattern

    # 尝试使用 examples 目录下的图像
    examples_dir = pathlib.Path(__file__).parent.parent / 'examples'
    if examples_dir.exists():
        image_files = list(examples_dir.glob('*.png'))
        if image_files:
            return Pattern(str(image_files[0]))

    # 如果没有示例图像，创建一个无效的 Pattern（用于测试错误处理）
    return Pattern('/nonexistent/pattern.png')

#!/usr/bin/env python3
"""
SikuliX 网关启动脚本

专门用于启动 SikuliX 的 py4j 网关服务。
需提前准备好 sikulixide.jar（必须是 IDE 版本，API 版本无法调用）。

下载地址：
- SikuliX: https://raiman.github.io/SikuliX1/downloads.html
- py4j（无需下载，已包含在 SikuliX 中）: https://repo1.maven.org/maven2/net/sf/py4j/py4j/

依赖安装：pip install py4j
环境变量：设置 JAVA_HOME 指向 JDK 安装目录
"""

import logging
import os
import pathlib
import re
import subprocess
import sys
import time
from typing import Optional, Union

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def find_jar(filename: str) -> Optional[pathlib.Path]:
    """
    查找指定名称的 JAR 文件。

    Args:
        filename: JAR 文件名关键词

    Returns:
        找到的 JAR 文件路径，未找到返回 None
    """
    jar_env = os.getenv('SIKULIX_JAR') or os.getenv('SIKULIX')
    if jar_env:
        jar_path = pathlib.Path(jar_env)
        if jar_path.exists():
            return jar_path

    possible_dirs = [
        '.',
        os.path.expanduser('.'),
        '/Applications/',
        '/usr/local/',
    ]

    for directory in possible_dirs:
        p_dir = pathlib.Path(directory)
        if not p_dir.exists():
            continue
        for path in p_dir.glob('**/*.jar'):
            if re.search(filename, str(path)):
                return path

    return None


class SikuliXGateway:
    """SikuliX 网关启动器。"""

    def __init__(self, port: int = 25333, sikulix_path: Optional[Union[str, pathlib.Path]] = None):
        self.port = port
        self.gateway_process = None
        self.sikulix_path = sikulix_path

    def find_sikulix_jar(self) -> Optional[pathlib.Path]:
        """查找 SikuliX JAR 文件。"""
        path = find_jar('sikulix')
        if path:
            logger.info(f'找到 SikuliX JAR: {path.absolute()}')
            return path

        logger.error('未找到 SikuliX JAR 文件')
        return None

    def test_connection(self) -> bool:
        """测试网关连接。"""
        from py4j.java_gateway import GatewayParameters, JavaGateway
        from py4j.protocol import Py4JNetworkError

        try:
            logger.info('测试网关连接...')

            gateway = JavaGateway(gateway_parameters=GatewayParameters(port=self.port))
            screen = gateway.jvm.org.sikuli.script.Screen()  # type: ignore
            logger.info(f'屏幕数量：{screen.getNumberScreens()}，屏幕尺寸：{screen.getBounds()}')  # type: ignore

            logger.info('网关连接测试成功')
            gateway.close()
            return True

        except Py4JNetworkError:
            logger.error('无法连接到网关')
        except Exception as e:
            logger.error(f'连接测试失败: {e}')
        return False

    def start(self) -> bool:
        """启动 SikuliX 网关。"""
        logger.info('=== 启动 SikuliX 网关 ===')

        if not self.sikulix_path:
            self.sikulix_path = self.find_sikulix_jar()
            if not self.sikulix_path:
                logger.error('未找到 SikuliX JAR 文件')
                return False

        self.gateway_process = subprocess.Popen(
            ['java', '-cp', str(self.sikulix_path), 'py4j.GatewayServer', str(self.port)],
            stdout=subprocess.DEVNULL,  # 防止没有处理stdout、stderr导致的缓冲区满进程挂起的情况
            stderr=subprocess.DEVNULL,
            text=True,
        )

        time.sleep(1)

        if self.gateway_process.poll() is None:
            logger.info(f'网关启动成功，运行端口：{self.port}')
        else:
            _, stderr = self.gateway_process.communicate()
            logger.warning(f'网关启动失败: {stderr}')
            return False

        return self.test_connection()

    def stop(self, timeout: float = 8):
        """停止网关"""
        if not self.gateway_process:
            return
        self.gateway_process.terminate()  # type: ignore
        try:
            self.gateway_process.wait(timeout=timeout)  # type: ignore
            logger.info('已停止 SikuliX 网关')
        except subprocess.TimeoutExpired:
            self.gateway_process.kill()  # type: ignore
            logger.info('已停止 SikuliX 网关')

    def test_status(self, is_output: bool = True) -> bool:
        """显示网关状态。"""
        if self.gateway_process and self.gateway_process.poll() is None:
            if is_output:
                logger.info('网关正在运行...')
            return True
        if is_output:
            logger.info('网关未运行')
        return False


def main():
    """运行主函数。"""
    launcher = SikuliXGateway()
    try:
        if len(sys.argv) > 1:
            command = sys.argv[1]
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 25333

            launcher = SikuliXGateway(port)

            if command == 'start':
                launcher.start()
            elif command == 'stop':
                launcher.stop()
            elif command == 'status':
                launcher.test_status()
            elif command == 'test':
                launcher.test_connection()
            else:
                print('用法: python -m py_sikulix.gateway [start|stop|status|test] [port]')
            while launcher.test_status(False):
                time.sleep(1)
        else:
            print('#===== SikuliX 网关 =====#')
            while True:
                choice = input(
                    '\n1 - 启动网关  2 - 停止网关\n3 - 查看状态  4 - 测试连接\n0 - 退出\n请选择操作 (0-4): '
                ).strip()

                if choice == '0':
                    break
                elif choice == '1':
                    launcher.start()
                elif choice == '2':
                    launcher.stop()
                elif choice == '3':
                    launcher.test_status()
                elif choice == '4':
                    launcher.test_connection()
                else:
                    print('无效选择')
                time.sleep(1)
    except KeyboardInterrupt:
        logger.warning('用户手动中断')
    finally:
        launcher.stop()


if __name__ == '__main__':
    main()

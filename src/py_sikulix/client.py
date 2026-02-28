#!/usr/bin/env python3

import logging
import os
import threading
from typing import Any

from py4j.java_gateway import GatewayParameters, JavaClass, JavaGateway, JavaObject, JavaPackage
from py4j.protocol import Py4JNetworkError
from pynput import keyboard

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SikuliXClient:
    """SikuliX Python 客户端主类，提供对 SikuliX 核心功能的 Python 封装。"""

    def __init__(self, port: int = 25333):
        """
        初始化 SikuliX 客户端。

        Args:
            port: Py4J 网关端口
        """
        self.port = port
        self.listener: keyboard.GlobalHotKeys | None = None
        try:
            # 尝试连接
            self.gateway = JavaGateway(gateway_parameters=GatewayParameters(port=self.port, auto_field=True))
            self.jvm = self.gateway.jvm  # type: ignore

            # 初始化核心 SikuliX 类
            self._init_classes()
        except Py4JNetworkError as e:
            # 原报错很长，这里截断重新抛出
            raise Py4JNetworkError(f'无法连接到 SikuliX 网关，请检查网关是否正常启动：{e}')

    def _init_classes(self):
        """初始化 SikuliX 核心 Java 类引用。"""
        self.Sikuli: JavaPackage = self.jvm.org.sikuli  # type: ignore
        self.Screen: JavaClass = self.Sikuli.script.Screen  # type: ignore
        self.Region: JavaClass = self.Sikuli.script.Region  # type: ignore
        self.App: JavaClass = self.Sikuli.script.App  # type: ignore
        self.Pattern: JavaClass = self.Sikuli.script.Pattern  # type: ignore
        self.Match: JavaClass = self.Sikuli.script.Match  # type: ignore
        self.Location: JavaClass = self.Sikuli.script.Location  # type: ignore
        self.Key: JavaClass = self.Sikuli.script.Key  # type: ignore
        self.Button: JavaClass = self.Sikuli.script.Button  # type: ignore
        self.Options: JavaClass = self.Sikuli.script.Options  # type: ignore
        self.Settings: JavaClass = self.Sikuli.basics.Settings  # type: ignore

    def list2java_array(self, args: list[Any]) -> JavaObject:
        java_args: JavaObject = _G_SKL_CLI.jvm.java.util.ArrayList()  # type: ignore
        for arg in args:
            # try:
            java_args.append(arg)  # type: ignore
            # except Exception:
            #     java_args.append(arg._raw)  # type: ignore
        return java_args


# 全局单例客户端，需要延迟启动否则 gateway 引入时会直接启动Client连接网关报错
_G_SKL_CLI: SikuliXClient | None = None


def get_cli() -> SikuliXClient:
    """获取全局单例 SikuliX 客户端。"""
    global _G_SKL_CLI
    if _G_SKL_CLI is None:
        _G_SKL_CLI = SikuliXClient()
    return _G_SKL_CLI


def reg_exit_listener(hotkey: str = '<shift>+<alt>+c'):
    """注册按键退出监听器。

    Args:
        hotkey: 要监听的退出程序快捷键
    """

    def on_activate():
        logger.info(f'按下 {hotkey} 退出按键，正在强制退出...')
        os._exit(0)

    def run_listener():
        with keyboard.GlobalHotKeys({hotkey: on_activate}) as listener:
            listener.join()

    threading.Thread(target=run_listener, daemon=True).start()

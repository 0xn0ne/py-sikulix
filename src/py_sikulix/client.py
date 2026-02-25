#!/usr/bin/env python3

import logging
from typing import Any

from py4j.java_gateway import GatewayParameters, JavaClass, JavaGateway, JavaObject, JavaPackage
from py4j.protocol import Py4JNetworkError

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
        java_args: JavaObject = CLIENT.jvm.java.util.ArrayList()  # type: ignore
        for arg in args:
            # try:
            java_args.append(arg)  # type: ignore
            # except Exception:
            #     java_args.append(arg._raw)  # type: ignore
        return java_args


# 全局单例客户端（延迟初始化）
CLIENT: SikuliXClient = SikuliXClient()

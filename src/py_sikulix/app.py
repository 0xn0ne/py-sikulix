#!/usr/bin/env python3

#

import pathlib
from typing import Optional, Union

from py4j.java_gateway import JavaObject

from py_sikulix.client import CLIENT
from py_sikulix.region import Region


class App:
    """App 类用于控制应用程序的启动、关闭和焦点管理。"""

    def __init__(self, name_or_java_obj: Union[str, pathlib.Path, JavaObject]):
        """
        初始化 App 对象，和 sikuli 的 open 方法存在区别，必须传入参数。

        Args:
            name: 应用程序名称（不区分大小写）或可执行文件的路径
        """
        if isinstance(name_or_java_obj, (str, pathlib.Path)):
            name_or_java_obj = CLIENT.App(str(pathlib.Path(name_or_java_obj).absolute()))  # type: ignore
        if not isinstance(name_or_java_obj, JavaObject):
            raise ValueError(
                'please pass in the correct types of name parameter. do not directly pass in JavaObject to create the Class.'
            )
        self._raw = name_or_java_obj  # type: ignore

    @property
    def name(self) -> str:
        return self._raw.getName()  # type: ignore

    def open(self, name: Optional[str] = None) -> 'App':
        """
        打开指定名称的应用程序，如果不提供名称则打开 new() 方法中设置的应用程序。

        Args:
            name: 应用程序名称（不区分大小写）或可执行文件的路径

        Returns:
            包装后的 App 对象
        """
        if name is None:
            self._raw.open()  # type: ignore
        else:
            self._raw = self._raw.open(name)  # type: ignore
        return self

    def close(self, name: Optional[str] = None) -> bool:
        """
        关闭指定名称的应用程序。

        Args:
            name: 应用程序名称

        Returns:
            关闭成功返回 True，否则返回 False
        """
        if name is None:
            return self._raw.close()  # type: ignore
        return self._raw.close(name)  # type: ignore

    def focus(self, title: Optional[str] = None, index: Optional[int] = 0) -> 'App':
        """
        将焦点切换到具有匹配标题的窗口的应用程序。

        Args:
            title: 应用程序名称（不区分大小写）或窗口标题（区分大小写）
            index: 可选，匹配到多个应用时，选择应用编号（从 0 开始计数）

        Returns:
            当前 App 对象
        """
        if title is None:
            self._raw.focus()  # type: ignore
        else:
            self._raw = self._raw.focus(title, index)  # type: ignore
        return self

    def set_using(self, param_text: Union[str, list[str]]):
        """
        在使用 open() 函数启动应用程序时传递给应用程序，就像从命令行启动应用程序一样。

        Args:
            param_text: 参数字符串或参数列表

        Returns:
            当前 App 对象
        """
        if isinstance(param_text, list):
            param_text = ' '.join(param_text)
        self._raw.setUsing(param_text)  # type: ignore

    def set_work_dir(self, work_dir: Union[str, pathlib.Path]):
        """
        设置应用程序工作目录。

        Args:
            work_dir: 工作路径

        Returns:
            当前 App 对象
        """
        if isinstance(work_dir, pathlib.Path):
            work_dir = str(work_dir)
        self._raw.setWorkDir(work_dir)  # type: ignore
        return self

    def is_valid(self) -> bool:
        """
        检查应用程序对象是否具有有效的进程 ID。

        Returns:
            如果有进程 ID 则为 True，否则为 False
        """
        return self._raw.isValid()  # type: ignore

    def is_running(self, wait_time: Optional[int] = 1) -> bool:
        """
        检查应用程序是否正在运行，在 wait_time 内每秒检查一次应用程序的状态。

        Args:
            wait_time: 等待时间（秒）

        Returns:
            正在运行返回 True，否则返回 False
        """
        return self._raw.isRunning(wait_time)  # type: ignore

    def has_window(self) -> bool:
        """
        检查应用程序是否有窗口。

        Returns:
            如果应用程序正在运行并且已存在主窗口，则为 True，否则为 False
        """
        return self._raw.hasWindow()  # type: ignore

    def focused_window(self) -> Region:
        """
        获取当前焦点窗口的 Region 对象。

        Returns:
            焦点窗口区域
        """
        java_region = self._raw.focusedWindow()  # type: ignore
        return Region(java_region)  # type: ignore

    # 信息获取方法
    def get_title(self) -> str:
        """
        该应用程序最前窗口的标题，可能是一个空字符串。

        Returns:
            应用程序窗口标题
        """
        return self._raw.getTitle()  # type: ignore

    def get_pid(self) -> int:
        """
        获取应用程序的进程ID。

        Returns:
            进程ID，如果无法获取则返回 -1
        """
        return self._raw.getPID()  # type: ignore

    def get_name(self) -> str:
        """
        获取应用程序的名称。

        Returns:
            应用程序名称
        """
        return self.name  # type: ignore


if __name__ == '__main__':
    # 示例代码
    import time

    app = App('Google Chrome')
    app.open()
    new_app = app.open('微信')
    print(f'程序名称：{app.name}')
    print(f'程序进程：{app.get_pid()}')
    print(f'程序标题：{app.get_title()}')
    print(f'新开程序名称：{new_app.get_name()}')
    print(f'新开程序进程：{new_app.get_pid()}')
    print(f'新开程序标题：{new_app.get_title()}')
    print('切换Google Chrome', app.focus('Google Chrome'))
    print('请手动切换到其他程序，5s后切回Google Chrome')
    time.sleep(5)
    print('切换回Google Chrome', app.focus())
    region = app.focused_window()
    print(
        f'程序区域：{region._raw.getX()},{region._raw.getY()},{region._raw.getW()},{region._raw.getH()}'  # type: ignore
    )
    print(app.close('微信'))
    print(app.close())

"""
SikuliX Setting 类封装
提供了对 SikuliX 全局设置的访问和控制
接口参考：https://javadoc.io/static/com.sikulix/sikulixapi/2.0.5/org/sikuli/basics/Setting.html
"""

import logging

from py_sikulix.client import CLIENT

logger = logging.getLogger(__name__)


class Setting:
    """
    Setting 类封装了 SikuliX 中的全局设置选项，允许配置各种行为参数，
    如最小相似度、图像缩放、等待时间等。这些设置会影响整个应用程序的行为。
    """

    def __init__(self):
        """
        初始化 Setting 对象。
        """
        self._raw = CLIENT.Setting  # type: ignore
        self._throw_exception = False

    @property
    def action_logs(self) -> bool:
        """
        获取动作日志记录状态。

        Returns:
            bool: True表示启用动作日志，False表示禁用
        """
        return self._raw.ActionLogs  # type: ignore

    @action_logs.setter
    def action_logs(self, value: bool):
        """
        启用或禁用动作日志记录。

        Args:
            value (bool): True启用日志，False禁用日志
        """
        self._raw.ActionLogs = value  # type: ignore

    @property
    def info_logs(self) -> bool:
        """
        获取信息日志记录状态。

        Returns:
            bool: True表示启用信息日志，False表示禁用
        """
        return self._raw.InfoLogs  # type: ignore

    @info_logs.setter
    def info_logs(self, value: bool):
        """
        启用或禁用信息日志记录。

        Args:
            value (bool): True启用信息日志，False禁用
        """
        self._raw.InfoLogs = value  # type: ignore

    @property
    def debug_logs(self) -> bool:
        """
        获取调试日志记录状态。

        Returns:
            bool: True表示启用调试日志，False表示禁用
        """
        return self._raw.DebugLogs  # type: ignore

    @debug_logs.setter
    def debug_logs(self, value: bool):
        """
        启用或禁用调试日志记录。

        Args:
            value (bool): True启用调试日志，False禁用
        """
        self._raw.DebugLogs = value  # type: ignore

    @property
    def min_similarity(self) -> float:
        """
        获取当前的最小相似度阈值。

        Returns:
            float: 当前最小相似度值（0.0-1.0之间）
        """
        return self._raw.MinSimilarity  # type: ignore

    @min_similarity.setter
    def min_similarity(self, value: float):
        """
        设置最小相似度阈值。

        Args:
            value (float): 最小相似度值，范围应该在0.0-1.0之间
        """
        self._raw.MinSimilarity = value  # type: ignore

    @property
    def throw_exception(self) -> bool:
        """
        获取是否在查找失败时抛出异常。

        如果为 False（默认），查找失败时返回 None；
        如果为 True，查找失败时抛出 FindFailed 异常。

        Returns:
            bool: True 表示抛出异常，False 表示返回 None
        """
        return self._throw_exception

    @throw_exception.setter
    def throw_exception(self, value: bool):
        """
        设置是否在查找失败时抛出异常。

        Args:
            value (bool): True 启用异常抛出，False 禁用（返回 None）
        """
        self._throw_exception = value

    @property
    def move_mouse_delay(self) -> float:
        """
        获取鼠标移动到目标位置所需的时间（秒）。

        Returns:
            float: 鼠标移动所需时间（秒）
        """
        return self._raw.MoveMouseDelay  # type: ignore

    @move_mouse_delay.setter
    def move_mouse_delay(self, value: float):
        """
        设置鼠标移动到目标位置所需的时间（秒）。将其设置为 0 将关闭滑动（鼠标将"跳"到目标位置）。

        Args:
            value (float): 鼠标移动所需时间（秒），值应该 >= 0
        """
        self._raw.MoveMouseDelay = value  # type: ignore

    @property
    def delay_before_mouse_down(self) -> float:
        """
        获取拖动源始位置鼠标按下前的延迟时间。

        鼠标从源位置移动到目标位置所花费的时间由 Setting.MoveMouseDelay 控制。

        Returns:
            float: 延迟时间（秒）
        """
        return self._raw.DelayBeforeMouseDown  # type: ignore

    @delay_before_mouse_down.setter
    def delay_before_mouse_down(self, value: float = 0.3):
        """
        设置拖动源始位置鼠标按下前的延迟时间。

        鼠标从源位置移动到目标位置所花费的时间由 Setting.MoveMouseDelay 控制，
        这仅适用于下一次拖动操作。

        Args:
            value (float): 延迟时间（秒），默认0.3秒
        """
        self._raw.DelayBeforeMouseDown = value  # type: ignore

    @property
    def delay_before_drag(self) -> float:
        """
        获取在拖动源始位置鼠标按下后延迟时间。

        鼠标从源位置移动到目标位置所花费的时间由 Setting.MoveMouseDelay 控制，
        这仅适用于下一次拖动操作。

        Returns:
            float: 延迟时间（秒）
        """
        return self._raw.DelayBeforeDrag  # type: ignore

    @delay_before_drag.setter
    def delay_before_drag(self, value: float = 0.3):
        """
        设置在拖动源始位置鼠标按下后延迟时间。

        鼠标从源位置移动到目标位置所花费的时间由 Setting.MoveMouseDelay 控制。

        Args:
            value (float): 延迟时间（秒）
        """
        self._raw.DelayBeforeDrag = value  # type: ignore

    @property
    def delay_before_drop(self) -> float:
        """
        获取拖动目标位置鼠标抬起前延迟时间。

        鼠标从源位置移动到目标位置所花费的时间由 Setting.MoveMouseDelay 控制。

        Returns:
            float: 延迟时间（秒）
        """
        return self._raw.DelayBeforeDrop  # type: ignore

    @delay_before_drop.setter
    def delay_before_drop(self, value: float = 0.3):
        """
        设置拖动目标位置鼠标抬起前延迟时间。

        鼠标从源位置移动到目标位置所花费的时间由 Setting.MoveMouseDelay 控制。

        Args:
            value (float): 延迟时间（秒）
        """
        self._raw.DelayBeforeDrop = value  # type: ignore

    @property
    def click_delay(self) -> float:
        """
        鼠标点击按下和抬起之间的延迟。这仅适用于下一次点击操作。

        Returns:
            float: 延迟时间（秒）
        """
        return self._raw.ClickDelay  # type: ignore

    @click_delay.setter
    def click_delay(self, value: float = 0):
        """
        鼠标点击按下和抬起之间的延迟。这仅适用于下一次点击操作。

        Args:
            value (float): 延迟时间（秒），应该 >= 0，大于 1 的值会被强制重置为 1
        """
        self._raw.ClickDelay = value  # type: ignore

    @property
    def type_delay(self) -> float:
        """
        键盘按键按下和抬起之间的延迟。这仅适用于下一次按键操作。

        Returns:
            float: 延迟时间（秒）
        """
        return self._raw.TypeDelay  # type: ignore

    @type_delay.setter
    def type_delay(self, value: float = 0):
        """
        键盘按键按下和抬起之间的延迟。这仅适用于下一次按键操作。

        Args:
            value (float): 延迟时间（秒），应该 >= 0，大于 1 的值会被强制重置为 1
        """
        self._raw.TypeDelay = value  # type: ignore

    @property
    def slow_motion_delay(self) -> float:
        """
        获取慢动作延迟时间（当前不支持）。

        Returns:
            float: 延迟时间（秒）
        """
        logger.warning('slow_motion_delay property is not fully supported')
        return self._raw.SlowMotionDelay  # type: ignore

    @slow_motion_delay.setter
    def slow_motion_delay(self, value: float = 0):
        """
        设置慢动作延迟时间（当前不支持）。

        Args:
            value (float): 延迟时间（秒）
        """
        logger.warning('slow_motion_delay property is not fully supported')
        self._raw.SlowMotionDelay = value  # type: ignore

    @property
    def wait_scan_rate(self) -> float:
        """
        获取等待出现扫描速率。

        Returns:
            float: 图像搜索时的扫描速率（每秒扫描次数）
        """
        return self._raw.WaitScanRate  # type: ignore

    @wait_scan_rate.setter
    def wait_scan_rate(self, value: float):
        """
        设置等待出现扫描速率。

        Args:
            value (float): 图像搜索时的扫描速率（每秒扫描次数）
        """
        self._raw.WaitScanRate = value  # type: ignore

    @property
    def observe_scan_rate(self) -> float:
        """
        获取等待消失扫描速率。

        Returns:
            float: 观察模式下的扫描速率（每秒扫描次数）
        """
        return self._raw.ObserveScanRate  # type: ignore

    @observe_scan_rate.setter
    def observe_scan_rate(self, value: float):
        """
        设置等待消失的扫描速率。

        Args:
            value (float): 观察模式下的扫描速率（每秒扫描次数）
        """
        self._raw.ObserveScanRate = value  # type: ignore

    @property
    def always_resize(self) -> bool:
        """
        获取是否总是调整图像大小的状态。

        Returns:
            float: 图像缩放值
        """
        return self._raw.AlwaysResize  # type: ignore

    @always_resize.setter
    def always_resize(self, value: float):
        """
        设置是否总是调整图像大小。

        Args:
            value (float): 图像缩放值，值 >= 0，当值 = 0 或值 = 1 时，将关闭缩放使用原始大小
        """
        self._raw.AlwaysResize = value  # type: ignore

    @property
    def image_callback(self) -> float:
        """
        获取图像回调设置（当前不支持）。

        Returns:
            float: 回调设置值
        """
        logger.warning('image_callback property is not fully supported')
        return 0.0

    @image_callback.setter
    def image_callback(self, value: float = 0):
        """
        设置图像回调（当前不支持）。

        Args:
            value (float): 回调设置值
        """
        logger.warning('image_callback property is not fully supported')

    def get_data_path(self) -> str:
        """
        获取 SikuliX 数据目录的路径。

        Returns:
            str: SikuliX 数据目录的路径
        """
        return self._raw.getDataPath()  # type: ignore

    def get_file_path_seperator(self) -> str:
        """
        获取文件路径分隔符。

        Returns:
            str: 文件路径分隔符（例如 "/" 或 "\\"）
        """
        return self._raw.getFilePathSeperator()  # type: ignore

    def get_image_cache(self) -> int:
        """
        获取当前图像缓存的最大数量。

        Returns:
            int: 当前图像缓存的最大数量
        """
        return self._raw.getImageCache()  # type: ignore

    def get_os(self) -> str:
        """
        获取操作系统名称。

        Returns:
            str: 操作系统名称（例如 "Windows", "Mac OS X", "Linux"）
        """
        return self._raw.getOS()  # type: ignore

    def get_os_version(self) -> str:
        """
        获取操作系统版本。

        Returns:
            str: 操作系统版本字符串
        """
        return self._raw.getOSVersion()  # type: ignore

    def get_path_separator(self) -> str:
        """
        获取路径分隔符。

        Returns:
            str: 路径分隔符（例如 ":" 或 ";"）
        """
        return self._raw.getPathSeparator()  # type: ignore

    def get_timestamp(self) -> str:
        """
        获取当前时间戳。

        Returns:
            str: 当前时间戳字符串
        """
        return self._raw.getTimestamp()  # type: ignore

    def get_version(self) -> str:
        """
        获取 SikuliX 版本号。

        Returns:
            str: SikuliX 版本号字符串
        """
        return self._raw.getVersion()  # type: ignore

    def get_version_build(self) -> str:
        """
        获取 SikuliX 构建版本。

        Returns:
            str: SikuliX 构建版本字符串
        """
        return self._raw.getVersionBuild()  # type: ignore

    def is_linux(self) -> bool:
        """
        检查当前操作系统是否为 Linux。

        Returns:
            bool: 如果是 Linux 系统返回 True，否则返回 False
        """
        return self._raw.isLinux()  # type: ignore

    def is_mac(self) -> bool:
        """
        检查当前操作系统是否为 Mac。

        Returns:
            bool: 如果是 Mac 系统返回 True，否则返回 False
        """
        return self._raw.isMac()  # type: ignore

    def is_windows(self) -> bool:
        """
        检查当前操作系统是否为 Windows。

        Returns:
            bool: 如果是 Windows 系统返回 True，否则返回 False
        """
        return self._raw.isWindows()  # type: ignore

    def is_show_actions(self) -> bool:
        """
        检查是否启用了动作显示。

        Returns:
            bool: 如果启用了动作显示返回 True，否则返回 False
        """
        return self._raw.isShowActions()  # type: ignore


if __name__ == '__main__':
    setting = Setting()
    print(f'当前最小相似度: {setting.min_similarity}')

    # 修改一些设置
    setting.min_similarity = 0.8
    setting.action_logs = True
    setting.debug_logs = True

    print(f'修改后的最小相似度: {setting.min_similarity}')
    print(f'动作日志状态: {setting.action_logs}')
    print(f'调试日志状态: {setting.debug_logs}')

    # 测试新增的方法
    print(f'数据路径: {setting.get_data_path()}')
    print(f'文件路径分隔符: {setting.get_file_path_seperator()}')
    print(f'图像缓存大小: {setting.get_image_cache()}')
    print(f'操作系统: {setting.get_os()}')
    print(f'操作系统版本: {setting.get_os_version()}')
    print(f'路径分隔符: {setting.get_path_separator()}')
    print(f'当前时间戳: {setting.get_timestamp()}')
    print(f'SikuliX版本: {setting.get_version()}')
    print(f'构建版本: {setting.get_version_build()}')
    print(f'是否为Linux系统: {setting.is_linux()}')
    print(f'是否为Mac系统: {setting.is_mac()}')
    print(f'是否为Windows系统: {setting.is_windows()}')
    print(f'是否显示动作: {setting.is_show_actions()}')
    print(f'鼠标移动速度: {setting.move_mouse_delay}')

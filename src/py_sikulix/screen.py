import logging
import pathlib
from typing import Optional, Union

from py4j.java_gateway import JavaObject

from py_sikulix.client import get_cli
from py_sikulix.region import Region

logger = logging.getLogger(__name__)


class Screen(Region):
    """
    Screen 类表示整个屏幕，继承自 Region 类。
    文档地址：https://sikulix-2014.readthedocs.io/en/latest/screen.html
    """

    def __init__(self, screenid_or_java_obj: Union[JavaObject, int] = 0):
        """
        初始化 Screen 对象。多显示器环境中可选择显示器编号进行监控。

        Args:
            screenid_or_java_obj: 屏幕编号或Java对象实例
        """
        if isinstance(screenid_or_java_obj, int):
            screenid_or_java_obj = get_cli().Screen(screenid_or_java_obj)  # type: ignore

        if not isinstance(screenid_or_java_obj, JavaObject):
            raise ValueError(
                'please pass in the correct types of screenid parameters. do not directly pass in JavaObject to create the Class.'
            )
        super().__init__(screenid_or_java_obj)

    # 设置、获取属性与信息
    def get_number_screens(self) -> int:
        """
        获取多显示器环境下的屏幕数量。

        Returns:
            屏幕数量
        """
        return self._raw.getNumberScreens()  # type: ignore

    def show_monitors(self):
        """
        打印当前显示器配置信息。
        """
        logger.info('show_monitors: 显示器配置信息功能暂不可用')

    def capture(
        self,
        x_or_region: Optional[Union[int, Region]] = None,
        y: Optional[int] = None,
        w: Optional[int] = None,
        h: Optional[int] = None,
        path: Union[str, pathlib.Path] = '.',
    ) -> pathlib.Path:
        """
        捕获屏幕截图。

        Args:
            x_or_region: 截图区域左上角 X 坐标
            y: 截图区域左上角 Y 坐标
            w: 截图区域宽度
            h: 截图区域高度
            path: 截图保存路径

        Returns:
            截图文件保存路径目录（原函数返回 org.sikuli.script.Image 类）
        """
        screen_x, screen_y, screen_w, screen_h = self.get_bounds()
        if isinstance(x_or_region, Region):
            return self._raw.capture(x_or_region._raw).getFile()  # type: ignore
        if x_or_region is None:
            x_or_region = screen_x
        if y is None:
            y = screen_y
        if w is None:
            w = screen_w
        if h is None:
            h = screen_h
        jva_image = self._raw.capture(x_or_region, y, w, h)  # type: ignore
        if isinstance(path, str):
            path = pathlib.Path(path)
        if path.is_dir():
            return pathlib.Path(jva_image.save(str(path.absolute())))  # type: ignore
        elif path.parent.is_dir():
            return pathlib.Path(jva_image.save(str(path.parent.absolute()), path.name))  # type: ignore
        raise ValueError(f'path "{path}" is not a file or directory')


if __name__ == '__main__':
    # 创建屏幕实例用于查找操作
    screen = Screen()

    # 示例5: find() - 查找单个图像
    print('\n--- 示例5: find() - 查找单个图像 ---')

    image_path = 'examples/RecycleBin.png'
    match = screen.find(image_path)

    if match:
        print(f'找到图像! 位置: ({match.x}, {match.y}), 大小: {match.w}x{match.h}')
        print(f'匹配分数: {match.get_score():.4f}')
    else:
        print(f'未找到图像: {image_path}')

    # 示例6: find_all() - 查找所有匹配
    print('\n--- 示例6: find_all() - 查找所有匹配 ---')

    matches = screen.find_all(image_path)
    if matches:
        print(f'找到 {len(matches)} 个匹配')
        for i, m in enumerate(matches):
            print(f'  匹配 {i + 1}: ({m.x}, {m.y}), 分数={m.get_score():.4f}')
    else:
        print('未找到任何匹配')

    # 示例7: wait() - 等待图像出现
    print('\n--- 示例7: wait() - 等待图像出现 ---')

    match = screen.wait(image_path, 5)
    if match:
        print(f'图像在等待时间内出现! 位置: ({match.x}, {match.y})')
    else:
        print('等待超时，图像未出现')

    # 示例8: wait_vanish() - 等待图像消失
    print('\n--- 示例8: wait_vanish() - 等待图像消失 ---')

    vanished = screen.wait_vanish(image_path, 5)
    if vanished:
        print('图像已消失')
    else:
        print('等待超时，图像仍然存在')

    # 示例9: exists() - 检查图像是否存在
    print('\n--- 示例9: exists() - 检查图像是否存在 ---')

    match = screen.exists(image_path)
    if match:
        print(f'图像存在! 位置: ({match.x}, {match.y})')
    else:
        print('图像不存在')

    # 示例18: 获取屏幕信息
    print('\n--- 示例18: 获取屏幕信息 ---')

    num_screens = screen.get_number_screens()
    print(f'显示器数量: {num_screens}')

    screen_bounds = screen.get_bounds()
    print(f'屏幕边界: x={screen_bounds[0]}, y={screen_bounds[1]}, w={screen_bounds[2]}, h={screen_bounds[3]}')

    # 示例19: 屏幕截图
    print('\n--- 示例19: 屏幕截图 ---')

    print('截取整个屏幕')
    print('截取指定区域 (100, 100, 300, 200)')

    # 示例20: highlight() - 高亮显示区域
    print('\n--- 示例20: highlight() - 高亮显示区域 ---')
    print('高亮显示区域2秒')

    # 示例21: get_last_match() - 获取最后一次匹配
    print('\n--- 示例21: get_last_match() - 获取最后一次匹配 ---')

    last_match = screen.get_last_match()
    if last_match:
        print(f'最后一次匹配: ({last_match.x}, {last_match.y})')
    else:
        print('没有最后一次匹配记录')

    print('\n' + '=' * 60)
    print('所有示例完成！')
    print('=' * 60)

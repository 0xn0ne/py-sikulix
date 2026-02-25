import pathlib
from typing import Optional, Union

from py4j.java_gateway import JavaObject

from py_sikulix.client import CLIENT
from py_sikulix.location import Location


class Pattern:
    """
    Pattern 类用于定义要搜索的图像模式，包括图像路径、相似度阈值等属性。
    """

    def __init__(self, path_or_java_obj: Union[str, pathlib.Path, JavaObject]):
        """
        初始化 Pattern 对象。

        Args:
            java_instance: SikuliX 中的 Pattern Java 对象
        """
        if isinstance(path_or_java_obj, (str, pathlib.Path)):
            path_or_java_obj = pathlib.Path(path_or_java_obj)
            if not path_or_java_obj.exists():
                raise FileNotFoundError(f'file {path_or_java_obj} does not exist')
        path_or_java_obj = CLIENT.Pattern(str(path_or_java_obj.absolute()))  # type: ignore
        if not isinstance(path_or_java_obj, JavaObject):
            raise ValueError(
                'please pass in the correct types of path parameter. do not directly pass in JavaObject to create the Class.'
            )
        self._raw = path_or_java_obj

    @property
    def filename(self) -> pathlib.Path:
        return pathlib.Path(self._raw.getFilename())  # type: ignore

    @filename.setter
    def filename(self, value: Union[str, pathlib.Path]):
        if isinstance(value, str):
            value = pathlib.Path(value)
        self._raw.setFilename(str(value.absolute()))  # type: ignore

    @property
    def resize(self) -> float:
        return self._raw.getResize()  # type: ignore

    @resize.setter
    def resize(self, value: float):
        self._raw.resize(value)  # type: ignore

    @property
    def similar(self) -> float:
        return self._raw.getSimilar()  # type: ignore

    @similar.setter
    def similar(self, value: float):
        self._raw.similar(value)  # type: ignore

    @property
    def target_offset(self) -> Location:
        return Location(self._raw.getTargetOffset())  # type: ignore

    @target_offset.setter
    def target_offset(self, value: Union[tuple[int, int], Location]):
        if isinstance(value, Location):
            self._raw.targetOffset(value)  # type: ignore
        else:
            self._raw.targetOffset(value[0], value[1])  # type: ignore

    def set_similar(self, sim: float = 0.7):
        """
        设置匹配最低相似度阈值。

        Args:
            similarity: 相似度阈值，范围 0.0-1.0，值越大匹配要求越精确，
                默认最小相似度 0.7，可在 Settings.MinSimilarity 中更改

        Returns:
            当前 Pattern 对象，支持链式调用
        """
        self._raw.similar(sim)  # type: ignore
        return self

    def exact(self):
        """
        将最低相似度设置为 0.99，相当于需要完全匹配。

        Returns:
            当前 Pattern 对象，支持链式调用
        """
        self._raw.exact()  # type: ignore
        return self

    def set_resize(self, factor: float = 1):
        """
        在搜索操作之前调整图像大小（因子同时应用于宽度和高度）。
        使用 Java-AWT-BufferedImage 标准调整大小行为。

        Args:
            factor: 缩放因子，值应大于0但不等于1，设置为0或1关闭

        Returns:
            当前 Pattern 对象，支持链式调用
        """
        self._raw.resize(factor)  # type: ignore
        return self

    def set_target_offset(self, dx: int, dy: int):
        """
        设置目标偏移量，点击时相对于匹配中心的偏移位置。

        Args:
            dx: X 轴偏移量
            dy: Y 轴偏移量

        Returns:
            当前 Pattern 对象，支持链式调用
        """
        self._raw.targetOffset(dx, dy)  # type: ignore
        return self

    def mask(self, image_or_pattern: Optional[Union[str, pathlib.Path, 'Pattern']] = None):
        """
        设置蒙版。若设置参数，该图片将作为当前图片的蒙版，黑色（RGB为000000）部分不匹配。若无参数，将图片的alpha通道为100%的透明部分视为蒙版。基础图像和蒙版图像必须具有相同像素尺寸。
        注意：Sikulix在透明蒙版处理上结果很差，如测试的垃圾桶图片能匹配出几十个结果出来，而且相似度都很高。需要测试的可以使用ide工具实时查看匹配结果。

        Args:
            image_or_pattern: 蒙版图片路径或 Pattern 对象

        Returns:
            当前 Pattern 对象，支持链式调用
        """
        if image_or_pattern:
            if not isinstance(image_or_pattern, Pattern):
                image_or_pattern = Pattern(image_or_pattern)
            self._raw.mask(image_or_pattern._raw)  # type: ignore
        else:
            self._raw.mask()  # type: ignore
        return self

    def get_filename(self) -> str:
        """
        获取 Pattern 的图像文件路径。

        Returns:
            图像文件的绝对路径字符串
        """
        return self._raw.getFilename()  # type: ignore

    def get_similar(self) -> float:
        """
        获取当前设置的相似度阈值。

        Returns:
            相似度阈值，范围 0.0-1.0
        """
        return self._raw.getSimilar()  # type: ignore

    def get_target_offset(self) -> Location:
        """
        获取目标偏移量。

        Returns:
            Location对象，表示相对于匹配中心的偏移点位
        """
        return Location(self._raw.getTargetOffset())  # type: ignore

    def get_resize(self):
        """
        获取缩放因子

        Returns:
            缩放比例
        """
        return self._raw.getResize()  # type: ignore

    def __repr__(self) -> str:
        """
        返回对象的字符串表示。

        Returns:
            对象的字符串表示
        """
        return f'<class {self.__class__.__name__} at {hex(id(self))}, S:{self.similar} O:{self.target_offset.x},{self.target_offset.y} R:{self.resize} F:{self.filename}>'


if __name__ == '__main__':
    import pathlib

    print('=' * 50)
    print('示例1: 创建 Pattern 对象')
    print('=' * 50)

    image_path = 'examples/RecycleBin.png'
    try:
        pattern1 = Pattern(image_path)
        print(f'成功创建 Pattern: {image_path}')
    except FileNotFoundError as e:
        print(f'文件不存在: {e}')

    path_obj = pathlib.Path('examples/RecycleBin_Transparent.png')
    try:
        pattern2 = Pattern(path_obj)
        print(f'使用 pathlib.Path 创建 Pattern: {path_obj}')
    except FileNotFoundError as e:
        print(f'文件不存在: {e}')

    print('\n' + '=' * 50)
    print('示例2: 设置相似度阈值')
    print('=' * 50)

    try:
        pattern = Pattern('examples/RecycleBin_Transparent.png')
        pattern.similar = 0.8
        print(f'设置相似度: {pattern.similar}')
    except FileNotFoundError:
        print('跳过示例2: 测试图像不存在')

    print('\n' + '=' * 50)
    print('示例3: 精确匹配')
    print('=' * 50)

    try:
        pattern = Pattern('examples/RecycleBin_Transparent.png')
        pattern.exact()
        print(f'精确匹配模式，相似度: {pattern.similar}')
    except FileNotFoundError:
        print('跳过示例3: 测试图像不存在')

    print('\n' + '=' * 50)
    print('示例4: 图像缩放')
    print('=' * 50)

    try:
        pattern = Pattern('examples/RecycleBin_Transparent.png')
        pattern.resize = 1.5
        print('图像放大 1.5 倍')
        pattern.set_resize(0.5)
        print('图像缩小到 0.5 倍')
    except FileNotFoundError:
        print('跳过示例4: 测试图像不存在')

    print('\n' + '=' * 50)
    print('示例5: 目标偏移量')
    print('=' * 50)

    try:
        pattern = Pattern('examples/RecycleBin_Transparent.png')
        pattern.target_offset = 10, 20
        location = pattern.target_offset
        print(f'目标偏移量: x={location.x}, y={location.y}')
    except FileNotFoundError:
        print('跳过示例5: 测试图像不存在')

    print('\n' + '=' * 50)
    print('示例6: 蒙版功能')
    print('=' * 50)

    try:
        pattern_black = Pattern('examples/RecycleBin_Black.png').mask()
        print('方式1: 使用图像黑色部分作为蒙版')
        pattern_trans = Pattern('examples/RecycleBin_Transparent.png').mask()
        print('方式2: 使用透明部分作为蒙版')
        pattern_mask = Pattern('examples/RecycleBin.png').mask('examples/RecycleBin_Black.png')
        print('方式3: 使用另一个图像作为蒙版')
    except FileNotFoundError:
        print('跳过示例6: 测试图像不存在')

    print('\n' + '=' * 50)
    print('示例7: Getter 方法 - 获取 Pattern 属性')
    print('=' * 50)

    try:
        pattern = Pattern('examples/RecycleBin.png').set_similar(0.85).set_target_offset(5, -10)
        filename = pattern.get_filename()
        print(f'图像路径: {filename}')
        similarity = pattern.get_similar()
        print(f'相似度: {similarity}')
        offset = pattern.get_target_offset()
        print(f'目标偏移: dx={offset.x}, dy={offset.y}')
    except FileNotFoundError:
        print('跳过示例7: 测试图像不存在')

    print('\n' + '=' * 50)
    print('示例8: 流式 API - 方法链式调用')
    print('=' * 50)

    try:
        pattern = Pattern('examples/RecycleBin.png').set_similar(0.9).set_target_offset(0, 5).set_resize(1.2)
        print('链式调用创建 Pattern 成功！')
        print(f'  相似度: {pattern.get_similar()}')
        print(f'  偏移量: {pattern.get_target_offset()}')
        print(f'  缩放比: {pattern.get_resize()}')
    except FileNotFoundError:
        print('跳过示例8: 测试图像不存在')

    print('\n' + '=' * 50)
    print('示例9: 实际使用场景')
    print('=' * 50)

    try:
        exact_pattern = Pattern('examples/RecycleBin.png').exact()
        print('场景2: 精确匹配按钮')
        offset_pattern = Pattern('examples/RecycleBin.png').set_target_offset(50, 0)
        print('场景3: 点击图标右侧 50 像素处')
        scaled_pattern = Pattern('examples/RecycleBin.png').set_resize(1.5)
        print('场景4: 高 DPI 屏幕缩放匹配')
        masked_pattern = Pattern('examples/RecycleBin.png').mask('examples/RecycleBin.png')
        print('场景5: 使用蒙版忽略背景')
    except FileNotFoundError:
        print('跳过示例9: 测试图像不存在')

    print(f'打印对象：{pattern}')  # type: ignore

    print('\n所有示例完成！')

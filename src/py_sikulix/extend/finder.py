import time
from collections.abc import Sequence

try:
    import cv2
    import mss
    import numpy as np
    from numba import njit
except ImportError:
    raise ImportError(
        'please install dependencies using the commands "pip install opencv-python mss numpy numba" before loading this script.'
    )


# =============================================================
# 多点找色核心算法：跨平台机器码加速
# =============================================================
@njit(fastmath=True, nogil=True)
def _numba_kernel(
    y_cands: np.ndarray,
    x_cands: np.ndarray,
    image: np.ndarray,
    sub_colors: np.ndarray,
    similarity_threshold: float,
) -> tuple[int, int, int, int, float, int, int, int] | None:
    """
    Numba优化的核心匹配算法（基于匹配比例），首次加载大约需要1s随后即可正常加速搜索

    Args:
        y_cands: 候选点y坐标数组
        x_cands: 候选点x坐标数组
        image: 原始图像 (H, W, 4) BGRA格式
        sub_colors: (N, 8) int32 数组，包含偏移和颜色信息 [偏移X, 偏移Y, 目标B, 目标G, 目标R, 偏离B, 偏离G, 偏离R]
        similarity_threshold: 相似度阈值 (0.0-1.0)

    Returns:
        匹配结果数组 [x, y, similarity, r, g, b] 或 None
        x, y: 匹配点的坐标 (相对于区域左上角)
        similarity: 匹配比例 (0.0-1.0)
        r, g, b: 匹配点的RGB颜色值 (BGR格式)
    """
    h, w = image.shape[:2]
    num_cands = len(y_cands)

    len_sub_colors = len(sub_colors)
    total_points = len_sub_colors + 1
    min_similarity_score = total_points * similarity_threshold
    max_offset_x = 0
    min_offset_x = 0
    max_offset_y = 0
    min_offset_y = 0
    for main_i in range(num_cands):
        main_y, main_x = y_cands[main_i], x_cands[main_i]
        match_score_sum = 1.0  # 主点总是记为100%匹配（通过初筛），缺点是主点不会考虑色彩偏离
        for sub_i in range(len_sub_colors):
            offset_x, offset_y = sub_colors[sub_i, 0], sub_colors[sub_i, 1]
            sub_x, sub_y = main_x + offset_x, main_y + offset_y
            # 更新坐标边界值
            max_offset_x = max(max_offset_x, offset_x)
            min_offset_x = min(min_offset_x, offset_x)
            max_offset_y = max(max_offset_y, offset_y)
            min_offset_y = min(min_offset_y, offset_y)

            # 边界检查，像素点超出边界直接放弃匹配
            if 0 <= sub_x < w and 0 <= sub_y < h:
                scol_b, scol_g, scol_r = sub_colors[sub_i, 2], sub_colors[sub_i, 3], sub_colors[sub_i, 4]
                bias_b, bias_g, bias_r = sub_colors[sub_i, 5], sub_colors[sub_i, 6], sub_colors[sub_i, 7]
                image_b = image[sub_y, sub_x, 0]  # B
                image_g = image[sub_y, sub_x, 1]  # G
                image_r = image[sub_y, sub_x, 2]  # R

                # 检查是否匹配
                abs_b = abs(image_b - scol_b)
                abs_g = abs(image_g - scol_g)
                abs_r = abs(image_r - scol_r)
                if abs_b <= bias_b and abs_g <= bias_g and abs_r <= bias_r:
                    match_score_sum += 1.0 - (abs_b + abs_g + abs_r) / 765  # 765 = FF * 3
            # 匹配值不达标的情况提前退出内层循环，相似度要求越低匹配循环次数越多
            if match_score_sum + (len_sub_colors - sub_i - 1) < min_similarity_score:
                break
        similarity = match_score_sum / total_points
        if similarity < similarity_threshold:
            continue
        # 基于匹配比例计算相似度
        # 返回主点x, 主点y, 匹配目标宽度, 匹配目标高度, 相似度, RGB颜色10进制值(BGR转RGB)
        return (
            main_x + min_offset_x,  # 主点x
            main_y + min_offset_y,  # 主点y
            max_offset_x - min_offset_x,  # 匹配目标宽度
            max_offset_y - min_offset_y,  # 匹配目标高度
            similarity,  # 相似度
            image[main_y, main_x, 2],  # 十进制R
            image[main_y, main_x, 1],  # 十进制G
            image[main_y, main_x, 0],  # 十进制B
        )

    return None


class CrossPlatformFinder:
    def __init__(self, screen_id: int = 0):
        """
        初始化跨平台找色器，2560*1440分辨率下单次400个点约100ms

        Args:
            screen_id: 显示器编号，0为使用默认显示器，1为使用第1个显示器，2为使用第2个显示器，以此类推
        """
        self.screen = mss.mss()
        self.width = self.screen.monitors[screen_id]['width']
        self.height = self.screen.monitors[screen_id]['height']

    def _rgb_to_bgr(self, hex_str: str) -> list[int]:
        """
        将十六进制RGB颜色转换为BGR顺序 (MSS默认格式)

        Args:
            hex_str: 六位十六进制颜色值 (如 "FF00AA")

        Returns:
            BGR颜色值 [B, G, R]
        """
        return [int(hex_str[4:6], 16), int(hex_str[2:4], 16), int(hex_str[0:2], 16)]

    def _parse_config(self, color_str: str) -> tuple[np.ndarray, np.ndarray, np.ndarray] | None:
        """
        解析颜色字符串，生成匹配配置

        Args:
            color_str: 颜色字符串格式，偏色范围为可选值
            "主色|偏色范围,偏移X|偏移Y|次色|偏色范围,..."
            例如: "fafbfb|080808,-3|21|f9fafa|080808,-3|21|f9fafa, ..."

        Returns:
            (主色BGR, 主色偏色BGR, 偏移点配置数组)
        """
        colors_list = color_str.split(',')
        if not colors_list:
            return None

        # 解析首点 (主点)
        main_part = colors_list[0].split('|')
        main_bgr = self._rgb_to_bgr(main_part[0])
        main_bias = self._rgb_to_bgr(main_part[1]) if len(main_part) > 1 else [0, 0, 0]

        # 解析偏移点
        sub_colors = []
        for sub_color_str in colors_list[1:]:
            sub_color_parts = sub_color_str.split('|')
            if len(sub_color_parts) < 2:
                continue

            try:
                offset_x, offset_y = int(sub_color_parts[0]), int(sub_color_parts[1])
            except ValueError:
                continue

            # 处理颜色值
            if len(sub_color_parts) < 3:
                continue
            color_val = sub_color_parts[2]
            if len(color_val) != 6:
                continue
            sub_bgr = self._rgb_to_bgr(color_val)

            # 处理偏色范围
            sub_bias = [0, 0, 0]
            if len(sub_color_parts) >= 4:
                bias_val = sub_color_parts[3]
                if len(bias_val) == 6:
                    sub_bias = self._rgb_to_bgr(bias_val)

            sub_colors.append([offset_x, offset_y, *sub_bgr, *sub_bias])

        return np.array(main_bgr), np.array(main_bias), np.array(sub_colors, dtype=np.int32)

    def find_multi_color(
        self,
        color_str: str,
        similarity: float = 0.7,
        region: Sequence[int] | None = None,
    ) -> tuple[tuple[int, int, int, int], float] | None:
        """
        在指定区域执行多点找色（匹配比例计算）

        Args:
            color_str: 颜色字符串格式，偏色范围为可选值
                "主色|偏色范围,偏移X|偏移Y|次色|偏色范围,..."
                例如: "fafbfb|080808,-3|21|f9fafa|080808,-3|21|f9fafa, ..."
            similarity: 相似度阈值 (0.0-1.0), 默认0.9
            region: 搜索区域，格式为(左上角横坐标, 左上角纵坐标, 找色区域宽度, 找色区域高度)

        Returns:
            匹配结果 (最左上角x, 最左上角y, 相似度值) 或 None
        """
        # 1. 解析配置
        colors = self._parse_config(color_str)
        if not colors or len(colors[2]) == 0:
            raise ValueError(
                f'invalid color string or fewer than 2 colors. current color string: {color_str if len(color_str) < 30 else color_str[:30] + "..."}'
            )
        main_bgr, main_bias, sub_colors = colors
        if not region:
            left, top, width, height = (0, 0, self.width, self.height)
        elif len(region) >= 4:
            left, top, width, height = region[:4]
        elif len(region) >= 2:
            left, top = region[:2]
            width = self.width - left
            height = self.height - top
        else:
            raise ValueError(f'invalid region, must contain more than two values. current region: {region}')

        # 2. 跨平台截图
        scr_img = self.screen.grab({'left': left, 'top': top, 'width': width, 'height': height})
        frame = np.array(scr_img)  # 形状 (H, W, 4), 顺序 BGRA

        # 关键优化：使用OpenCV的inRange替代NumPy向量化操作
        lower = np.clip(main_bgr - main_bias, 0, 255).astype(np.uint8)
        upper = np.clip(main_bgr + main_bias, 0, 255).astype(np.uint8)
        mask = cv2.inRange(frame[:, :, :3], lower, upper)
        mask = mask > 0  # 转换为布尔数组
        y_cands, x_cands = np.where(mask)

        if len(y_cands) == 0:
            return None

        # 4. Numba核心匹配
        ret = _numba_kernel(y_cands, x_cands, frame, sub_colors, similarity)
        if not ret:
            return None
        return (ret[0] + left, ret[1] + top, ret[2], ret[3]), ret[4]


# =============================================================
# 测试运行 (以 PowerToys 界面为例)
# =============================================================
if __name__ == '__main__':
    finder = CrossPlatformFinder()

    # 样例：寻找 PowerToys 主页的蓝色颜色选取器等
    test_config = [
        'fafbfb|030303,3|10|f8f9fb|030303,-11|12|6fb2db|030303,-10|8|fafbfb|030303,-4|15|b4cce0|030303,-1|1|f3f8fa|030303',
        'f9fafb|030303,-9|10|7885e2|030303,-3|25|5e41c9|030303,-4|11|5950d9|030303,-1|10|5750d9|030303,-11|31|e4ddf6|030303,9|14|38cfdb|030303',
    ]

    print('跨平台找色引擎已启动 (mss + numba + OpenCV) - 修正版')
    print('相似度计算: 基于匹配比例 (与原始方法一致)')
    import random

    # 预热编译
    finder.find_multi_color(test_config[0], 0.7)

    times = []
    for _ in range(50):
        t_index = random.randint(0, len(test_config) - 1)
        start_t = time.time()
        result = finder.find_multi_color(test_config[t_index], 0.7)
        end_t = time.time()

        if result:
            print(
                f'找到第{t_index}个目标！坐标:{result[0][0]},{result[0][1]} 宽度:{result[0][2]} 高度:{result[0][3]} 相似度:{result[1]:.2f} 耗时:{(end_t - start_t) * 1000:.2f}ms'
            )
        else:
            print(f'未找到，耗时:{(end_t - start_t) * 1000:.2f}ms')
        times.append((end_t - start_t) * 1000)

    print(f'平均耗时: {sum(times) / len(times):.2f}ms')

#!/usr/bin/env python3

#

from __future__ import annotations

from py_sikulix.base_region import BaseRegion
from py_sikulix.location import Location


class Match(BaseRegion):
    """
    Match 类表示图像匹配成功后返回的结果，包含匹配区域的位置和置信度信息。
    """

    def get_target(self) -> Location:
        """
        获取将用作点击点的 Location 对象。

        Returns:
            匹配目标的位置对象
        """
        return self._raw.getTarget()  # type: ignore

    def get_score(self) -> float:
        """
        获取匹配的相似度评分。

        Returns:
            匹配分数，范围 0.0-1.0
        """
        return self._raw.getScore()  # type: ignore

    def __lt__(self, other: Match) -> bool:
        """
        比较两个 Match 对象的分数（小于）。

        Args:
            other: 另一个 Match 对象

        Returns:
            当前分数是否小于另一个
        """
        return self.get_score() < other.get_score()

    def __le__(self, other: Match) -> bool:
        """
        比较两个 Match 对象的分数（小于等于）。

        Args:
            other: 另一个 Match 对象

        Returns:
            当前分数是否小于等于另一个
        """
        return self.get_score() <= other.get_score()

    def __gt__(self, other: Match) -> bool:
        """
        比较两个 Match 对象的分数（大于）。

        Args:
            other: 另一个 Match 对象

        Returns:
            当前分数是否大于另一个
        """
        return self.get_score() > other.get_score()

    def __ge__(self, other: Match) -> bool:
        """
        比较两个 Match 对象的分数（大于等于）。

        Args:
            other: 另一个 Match 对象

        Returns:
            当前分数是否大于等于另一个
        """
        return self.get_score() >= other.get_score()

    def __eq__(self, other: object) -> bool:
        """
        比较两个 Match 对象的分数（等于）。

        Args:
            other: 另一个 Match 对象

        Returns:
            当前分数是否等于另一个
        """
        if not isinstance(other, Match):
            raise ValueError("the 'Match' class cannot be compared with other classes.")
        return self.get_score() == other.get_score()

    def __repr__(self) -> str:
        """
        返回对象的字符串表示。

        Returns:
            对象的字符串表示
        """
        return f'<class {self.__class__.__name__} at {hex(id(self))}, [{self.x},{self.y} {self.w}x{self.h}] S:{self.get_score():.4f}>'


if __name__ == '__main__':
    # 示例代码 - Match 类测试示例

    import pathlib

    from py_sikulix.pattern import Pattern
    from py_sikulix.screen import Screen

    # 创建屏幕实例
    screen = Screen()

    # ============================================
    # 示例1: 查找图像并获取 Match 对象
    print('=' * 50)
    print('示例1: 查找图像并获取 Match 对象')
    print('=' * 50)

    # 查找图像（需要先准备好测试图像）
    image_path = pathlib.Path('examples/RecycleBin.png')
    print('图像状态：', image_path.exists(), image_path.absolute())
    match = screen.find(image_path)

    if match:
        print(f'找到匹配！左上角坐标: ({match.x}, {match.y}), 大小: {match.w}x{match.h}')
    else:
        print('未找到匹配')

    # ============================================
    # 示例2: 获取匹配分数 (get_score)
    print('\n' + '=' * 50)
    print('示例2: 获取匹配分数')
    print('=' * 50)

    if match:
        score = match.get_score()
        print(f'匹配分数: {score:.4f} (范围 0.0-1.0)')

        if score > 0.9:
            print('高置信度匹配！')
        elif score > 0.7:
            print('中等置信度匹配')
        else:
            print('低置信度匹配')

    # ============================================
    # 示例3: 获取点击目标位置 (get_target)
    print('\n' + '=' * 50)
    print('示例3: 获取点击目标位置')
    print('=' * 50)

    if match:
        target = match.get_target()
        print(f'点击目标位置: ({target.x}, {target.y})')

    # ============================================
    # 示例4: Match 继承自 Region 的属性和方法
    print('\n' + '=' * 50)
    print('示例4: Match 继承自 Region 的属性')
    print('=' * 50)

    if match:
        print(f'区域左上角: ({match.x}, {match.y})')
        print(f'区域大小: {match.w} x {match.h}')

        center = match.get_center()
        print(f'区域中心: ({center.x}, {center.y})')

    # ============================================
    # 示例5: 比较运算符 - 比较两个 Match 的分数
    print('\n' + '=' * 50)
    print('示例5: 比较运算符')
    print('=' * 50)

    match_raw = screen.find('examples/RecycleBin.png')
    match_trn = screen.find('examples/RecycleBin_Transparent.png')
    print(match_raw, match_trn)

    if match_raw and match_trn:
        score1 = match_raw.get_score()
        score2 = match_trn.get_score()

        print(f'MatchRaw 分数: {score1:.4f}')
        print(f'MatchRrn 分数: {score2:.4f}')

        if match_raw > match_trn:
            print('MatchRaw 的分数更高 (MatchRaw > MatchRrn)')
        elif match_raw < match_trn:
            print('MatchRrn 的分数更高 (MatchRaw < MatchRrn)')
        else:
            print('两个匹配分数相同 (MatchRaw == MatchRrn)')

        print(f'MatchRaw >= MatchRrn: {match_raw >= match_trn}')
        print(f'MatchRaw <= MatchRrn: {match_raw <= match_trn}')

    # ============================================
    # 示例6: 使用 find_all 获取多个 Match 并排序
    print('\n' + '=' * 50)
    print('示例6: 获取多个匹配并按分数排序')
    print('=' * 50)

    matches = screen.find_all('examples/RecycleBin_Transparent.png')
    if matches:
        print(f'找到 {len(matches)} 个匹配')

        sorted_matches = sorted(matches, key=lambda m: m.get_score(), reverse=True)

        for i, m in enumerate(sorted_matches):
            print(f'匹配 {i + 1}: 分数={m.get_score():.4f}, 位置=({m.x}, {m.y})')

        best_match = sorted_matches[0]
        print(f'\n最佳匹配: 分数={best_match.get_score():.4f}')

    # ============================================
    # 示例7: Match 与 Pattern 配合使用
    print('\n' + '=' * 50)
    print('示例7: Match 与 Pattern 配合使用')
    print('=' * 50)

    pattern = Pattern('examples/RecycleBin_Transparent.png').set_similar(0.9)

    match = screen.find(pattern)
    if match:
        print(f'使用 Pattern 找到匹配，分数: {match.get_score():.4f}，位置: ({match.x}, {match.y})')

        match.click()

    print('\n所有示例完成！')

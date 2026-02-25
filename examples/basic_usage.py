#!/usr/bin/env python3

"""
Py-SikuliX 基础使用示例

这个示例展示了如何使用 Py-SikuliX 库进行基本的 GUI 自动化操作，
包括：
- 启动和连接 Java 网关
- 屏幕操作
- 图像识别
- 鼠标操作
- 键盘操作
- 应用程序控制
"""

import pathlib
import time

from py_sikulix import App, Key, Location, Pattern, Region, Screen, Setting


def print_section(title):
    """打印章节标题"""
    print('\n' + '=' * 60, title, '=' * 60)


def test_screen_operations(screen: Screen):
    """测试屏幕操作"""
    print_section('屏幕操作')

    try:
        # 获取主屏幕
        print(f'屏幕数量: {screen.get_number_screens()}')

        # 获取屏幕尺寸
        bounds = screen.get_bounds()
        print(f'屏幕尺寸: {bounds[2]}x{bounds[3]}，起始坐标：({bounds[0]},{bounds[1]})')

        # 获取中心点
        center = screen.get_center()
        print(f'屏幕中心: ({center.x}, {center.y})')

        # 屏幕截图
        savepath = screen.capture()
        print(f'截图保存: {savepath}')

    except Exception as e:
        print(f'错误: {e}')


def test_region_operations():
    """测试区域操作"""
    print_section('区域操作')

    try:
        # 创建区域
        region = Region(100, 100, 300, 200)
        print(f'创建区域: ({region.x}, {region.y})，宽长: {region.w}x{region.h}')
        region.highlight()
        time.sleep(0.5)
        region.x = 200
        region.y = 200
        region.w = 210
        region.h = 150
        print(f'修改区域: ({region.x}, {region.y})，宽长: {region.w}x{region.h}')
        region.highlight()
        region.highlight()

        # 获取区域边界
        bounds = region.get_bounds()
        print(f'区域边界: {bounds}')

        # 获取中心位置
        center = region.get_center()
        print(f'区域中心: ({center.x}, {center.y})')

        # 创建上方区域
        above_region = region.above(50)
        print(f'上方区域: ({above_region.x}, {above_region.y}) - {above_region.w}x{above_region.h}')
        above_region.highlight()
        time.sleep(0.5)
        region.move_to(Location(300, 300))
        region.highlight()
        region.highlight()
        time.sleep(0.5)

        region.highlight_all_off()

    except Exception as e:
        print(f'错误: {e}')


def test_location_operations():
    """测试位置操作"""
    print_section('位置操作')

    try:
        # 创建位置
        loc = Location(200, 300)
        print(f'初始位置: ({loc.get_x()}, {loc.get_y()})')

        # 偏移操作
        offset_loc = loc.offset(50, 50)
        print(f'偏移后: ({offset_loc.get_x()}, {offset_loc.get_y()})')

        # 方向操作
        above = loc.above(100)
        below = loc.below(100)
        left = loc.left(100)
        right = loc.right(100)

        print(f'上方 100px: ({above.get_x()}, {above.get_y()})')
        print(f'下方 100px: ({below.get_x()}, {below.get_y()})')
        print(f'左侧 100px: ({left.get_x()}, {left.get_y()})')
        print(f'右侧 100px: ({right.get_x()}, {right.get_y()})')

    except Exception as e:
        print(f'错误: {e}')


def test_pattern_operations():
    """测试模式操作"""
    print_section('模式操作')

    try:
        # 使用项目根目录的示例图像
        test_image = pathlib.Path(__file__).parent / 'examples/RecycleBin_Raw.png'

        if test_image.exists():
            pattern = Pattern(test_image)

            print(f'图像路径: {pattern.get_filename()}')

            # 设置相似度
            pattern.similar = 0.85
            print(f'相似度: {pattern.get_similar():.2f}')

            # 设置目标偏移
            pattern.target_offset = 10, 5
            location = pattern.get_target_offset()
            print(f'目标偏移: ({location.x}, {location.y})')

        else:
            print(f'测试图像不存在: {test_image}')

    except Exception as e:
        print(f'错误: {e}')


def test_mouse_operations(screen: Screen):
    """测试鼠标操作"""
    print_section('鼠标操作')

    try:
        # 获取中心位置
        center = screen.get_center()
        print(f'中心点: ({center.get_x()}, {center.get_y()})')

        # 点击
        print('点击中心位置...')
        screen.click()

        # 右键点击
        print('右键点击中心位置...')
        screen.right_click()

        # 双击
        print('双击中心位置...')
        screen.double_click()

        time.sleep(1)

    except Exception as e:
        print(f'错误: {e}')


def test_keyboard_operations(screen: Screen):
    """测试键盘操作"""
    print_section('键盘操作')

    try:
        # 输入文本
        print("输入文本 'Hello, World!'")
        screen.type('Hello, World!')
        time.sleep(0.5)

        # 按回车
        print('按回车键')
        screen.type(Key.ENTER)
        time.sleep(0.5)

        # 按 Ctrl+C
        print('按 Ctrl+C')
        screen.key_down(Key.CTRL)
        screen.key_down('c')
        screen.key_up('c')
        screen.key_up(Key.CTRL)

    except Exception as e:
        print(f'错误: {e}')


def test_app_operations():
    """测试应用程序操作"""
    print_section('应用程序操作')

    try:
        # 打开计算器（Windows）或计算器应用（其他系统）
        app = App('calc')

        print('尝试打开计算器...')
        app.open()
        time.sleep(2)

        if app.is_running():
            print(f'应用正在运行: {app.get_name()}')
            print(f'PID: {app.get_pid()}')
            print(f'标题: {app.get_title()}')

            # 获取焦点
            app.focus()
            print('应用获得焦点')

            # 获取聚焦窗口区域
            window = app.focused_window()
            bounds = window.get_bounds()
            print(f'窗口区域: {bounds}')

            time.sleep(3)
            print('关闭应用...')
            app.close()

        else:
            print('应用未成功打开')

    except Exception as e:
        print(f'错误: {e}')


def test_image_find(screen: Screen):
    """测试图像查找"""
    print_section('图像识别')

    try:
        test_image = pathlib.Path(__file__).parent / 'examples/RecycleBin_Raw.png'

        if test_image.exists():
            print('尝试查找回收站图标...')

            match = screen.find(test_image)
            if match:
                print(f'找到匹配: ({match.x}, {match.y}) - {match.w}x{match.h}')
                print(f'相似度: {match.get_score():.4f}')

                # 高亮匹配区域
                print('高亮匹配区域...')
                match.highlight('red')
                time.sleep(1)

            else:
                print('未找到匹配')

        else:
            print(f'测试图像不存在: {test_image}')

    except Exception as e:
        print(f'错误: {e}')


def main():
    """主函数"""
    print_section('Py-SikuliX 基础使用示例')

    try:
        # 配置设置
        Setting.min_similarity = 0.8

        # 获取屏幕实例
        screen = Screen()

        # 执行各项测试
        test_screen_operations(screen)
        test_region_operations()
        test_location_operations()
        test_pattern_operations()
        test_image_find(screen)
        test_mouse_operations(screen)
        test_keyboard_operations(screen)
        test_app_operations()

        print('\n' + '=' * 60)
        print('所有测试完成！')
        print('=' * 60)

    except ConnectionError as e:
        print(f'连接错误: {e}')
        print('\n请确保已启动 Java 网关:')
        print('  1. 运行命令: sikulix-gateway start')
        print('  2. 或使用命令: java -jar sikulixide.jar -r gateway')
    except Exception as e:
        print(f'意外错误: {e}')


if __name__ == '__main__':
    main()

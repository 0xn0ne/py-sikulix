# py-sikulix

[![PyPI](https://img.shields.io/pypi/v/py-sikulix.svg)](https://pypi.org/project/py-sikulix/)
[![Python](https://img.shields.io/pypi/pyversions/py-sikulix.svg)](https://pypi.org/project/py-sikulix/)
[![License](https://img.shields.io/pypi/l/py-sikulix.svg)](https://github.com/0xn0ne/py-sikulix/blob/main/LICENSE)

Py-SikuliX 是一个 Python 客户端库，通过 Py4J 与 SikuliX Java 后端交互，提供强大的 GUI 自动化和图像识别功能。

## 功能特性

- **屏幕操作**：获取屏幕信息、截图、屏幕区域管理
- **图像识别**：基于图像匹配的 GUI 元素定位
- **鼠标操作**：点击、右键、双击、拖拽等
- **键盘操作**：文本输入、快捷键、组合键
- **应用控制**：启动、关闭、焦点管理
- **区域操作**：区域定位、扩展、几何计算
- **配置管理**：可配置的相似度阈值、延迟等参数

## 环境要求

- **Python**: 3.10+
- **Java**: JDK 8+ (需设置 JAVA_HOME 环境变量)
- **SikuliX**: 测试环境使用 sikulixide-2.0.5 版本（项目根目录需放置 sikulixide-2.0.5.jar，或手动设置ide路径）

> **注意**: 必须是 sikulixide 版本，API 版本无法调用完整功能。

## 安装

### 使用 pip 安装

```bash
pip install py-sikulix
```

### 从源代码安装

```bash
git clone https://github.com/0xn0ne/py-sikulix.git
cd py-sikulix
pip install .
```

### 开发模式安装

```bash
pip install -e ".[dev]"
```

## 快速开始

### 1. 准备 SikuliX IDE JAR 文件

下载 [sikulixide-2.0.5.jar](https://raiman.github.io/SikuliX1/downloads.html) 并放置到项目根目录。

### 2. 启动 Java 网关

> ⚠️ **重要**: 在使用任何 py-sikulix 功能之前，必须先启动 Java 网关

**方式一：使用命令行工具**

```bash
# 启动网关（默认端口 25333）
python -m py_sikulix.gateway start

# 测试连接
python -m py_sikulix.gateway test

# 查看网关状态
python -m py_sikulix.gateway status

# 停止网关
python -m py_sikulix.gateway stop

# 或者使用编译好的
sikulix-gateway stop
```

**方式二：使用 Python 脚本**

```python
from py_sikulix.gateway import SikuliXGateway

launcher = SikuliXGateway(port=25333)
launcher.start()
```

### 3. 基本使用示例

```python
from py_sikulix import Screen, Pattern, Key, reg_exit_listener
import time

def main():
    # 获取主屏幕
    screen = Screen()

    # 查找图像
    try:
        # 查找图像并点击
        if match := screen.find("button.png"):
            match.click()

        # 输入文本
        screen.type("Hello, World!")
        screen.type(Key.ENTER)
        
        # 使用组合键
        screen.key_down(Key.WIN)
        screen.type("r")    # 注意这里必须使用小写字母才能触发组合键
        screen.key_up(Key.WIN)

    except Exception as e:
        print(f"错误: {e}")

    reg_exit_listener() # 如果程序需要长期运行，请务注册全局退出监听快捷键
    while True:
        # do something
        print('正在运行...')
        time.sleep(3)

if __name__ == "__main__":
    main()
```

## 核心类

### 屏幕和区域

- `Screen`：表示整个屏幕
- `Region`：表示屏幕的矩形区域
- `Location`：表示屏幕上的坐标点

### 图像识别

- `Pattern`：定义图像搜索模式（相似度、偏移、缩放）
- `Match`：表示图像匹配结果（位置、尺寸、相似度）

### 应用程序控制

- `App`：应用程序管理（启动、关闭、焦点）

### 输入设备

- `Key`：键盘按键常量
- `Btn`：鼠标按键常量

### 配置

- `Settings`：全局配置管理

## 使用示例

### 图像识别

```python
from py_sikulix import Screen, Pattern

screen = Screen()

# 查找图像
match = screen.find("image.png")
if match:
    print(f"找到图像: ({match.x}, {match.y})")
    print(f"相似度: {match.get_score():.2f}")

# 使用模式查找
pattern = Pattern("image.png").similar(0.8)
match = screen.find(pattern)
```

### 区域操作

```python
from py_sikulix import Region

# 创建区域
region = Region(100, 100, 300, 200)

# 获取区域属性
print(f"位置: ({region.x}, {region.y})")
print(f"尺寸: {region.w}x{region.h}")

# 获取中心位置
center = region.get_center()
print(f"中心: ({center.x}, {center.y})")

# 创建扩展区域
nearby = region.nearby(50)
```

### 应用程序控制

```python
from py_sikulix import App

app = App("Notepad")
app.open()

if app.is_running():
    print(f"PID: {app.get_pid()}")
    app.focus()
    
    # 获取窗口区域
    window = app.focused_window()
    print(f"窗口尺寸: {window.w}x{window.h}")

app.close()
```

### 鼠标和键盘操作

```python
from py_sikulix import Region, Key, Btn

region = Region(100, 100, 300, 200)

# 鼠标操作
region.click()                    # 左键点击
region.click(key=Btn.RIGHT)       # 右键点击
region.double_click()             # 双击
region.mouse_down()               # 鼠标按下
region.mouse_move(50, 50)          # 鼠标移动
region.mouse_up()                 # 鼠标释放
region.wheel(direction=Btn.WHEEL_DOWN)  # 滚轮向下

# 键盘操作
region.key_down(Key.WIN)          # 按下 Win 键
region.type("r")                  # 输入字符
region.key_up(Key.WIN)            # 释放 Win 键
```

## 高级用法

### 配置参数

```python
from py_sikulix import Settings

# 设置相似度阈值
Settings.min_similarity = 0.8

# 设置鼠标移动延迟
Settings.move_mouse_delay = 0.5

# 设置查找超时
Settings.wait_scan_rate = 2  # 每秒扫描次数
```

## 开发

### 运行测试

```bash
# 运行单元测试
pytest tests/test_location.py -v

# 运行所有测试
pytest -v

# 运行集成测试（需要真实 Java 网关）
pytest --run-integration tests/
```

### 代码检查

```bash
# 运行 ruff linter
ruff check src/

# 运行 mypy 类型检查
mypy src/

# 格式化代码
ruff format src/
```

## 项目结构

```
py-sikulix/
├── src/py_sikulix/
│   ├── __init__.py         # 包导出
│   ├── client.py           # 客户端管理，SikuliXClient 类
│   ├── region.py           # Region、Screen、Match 类
│   ├── screen.py           # 屏幕类
│   ├── pattern.py          # Pattern 类
│   ├── app.py              # App 类
│   ├── location.py         # Location 类
│   ├── settings.py         # Settings 配置类
│   ├── keys.py             # Key、Btn 常量
│   ├── gateway.py          # Java 网关启动器
│   └── extend/             # 扩展功能
│       └── finder.py       # 图像查找扩展
├── tests/
│   ├── conftest.py         # Pytest fixtures
│   ├── test_region.py
│   ├── test_pattern.py
│   └── test_location.py
├── examples/               # 示例图像
├── sikulixide-2.0.5.jar  # SikuliX IDE (需自行下载)
├── pyproject.toml          # 项目配置
└── README.md
```

## 依赖

- **Py4J**：Java 进程通信
- **Java 8+**：SikuliX 所需的 Java 运行时

## 版本历史

### v0.1.0 (2024-02-24)

- 初始版本
- 基本的屏幕操作和图像识别
- 鼠标、键盘、应用程序控制
- 区域管理和配置系统

### v0.1.1 (2026-02-28)

- 初始版本
- 基本的屏幕操作和图像识别
- 鼠标、键盘、应用程序控制
- 区域管理和配置系统

## 许可证

Apache 2.0

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- 报告问题：[Issues](https://github.com/0xn0ne/py-sikulix/issues)
- 功能请求：[Discussions](https://github.com/0xn0ne/py-sikulix/discussions)

## 致谢

基于 SikuliX 项目的工作：<https://sikulix-2014.readthedocs.io/>

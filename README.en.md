# py-sikulix

[![PyPI](https://img.shields.io/pypi/v/py-sikulix.svg)](https://pypi.org/project/py-sikulix/)
[![Python](https://img.shields.io/pypi/pyversions/py-sikulix.svg)](https://pypi.org/project/py-sikulix/)
[![License](https://img.shields.io/pypi/l/py-sikulix.svg)](https://github.com/0xn0ne/py-sikulix/blob/main/LICENSE)

Py-SikuliX is a Python client library that interacts with the SikuliX Java backend via Py4J, providing powerful GUI automation and image recognition capabilities.

## Features

- **Screen Operations**: Capture screen information, take screenshots, manage screen regions
- **Image Recognition**: GUI element localization based on image matching
- **Mouse Actions**: Click, right-click, double-click, drag-and-drop, etc.
- **Keyboard Actions**: Text input, shortcuts, key combinations
- **Application Control**: Launch, close, focus management
- **Area Operations**: Region positioning, expansion, geometric calculations
- **Configuration Management**: Configurable similarity thresholds, delays, and other parameters

## Environment Requirements

- **Python**: 3.9+
- **Java**: JDK 8+ (Requires setting JAVA_HOME environment variable)
- **SikuliX**: Test environment uses sikulixide-2.0.5 (Place sikulixide-2.0.5.jar in project root directory or manually set IDE path)

> **Note**: Must be the sikulixide version; API versions cannot invoke full functionality.

## Installation

### Using pip

Translated with DeepL.com (free version)

```bash
pip install py-sikulix
```

### Installing from Source Code

```bash
git clone https://github.com/0xn0ne/py-sikulix.git
cd py-sikulix
pip install .
```

### Development Mode Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### 1. Prepare the SikuliX IDE JAR File

Download [sikulixide-2.0.5.jar](https://raiman.github.io/SikuliX1/downloads.html) and place it in the project root directory.

### 2. Start the Java Gateway

**Method One: Using the Command Line Tool**

```bash
python -m py_sikulix.gateway start
```

**Method 2: Using Python Script**

```python
from py_sikulix.gateway import SikuliXGateway

launcher = SikuliXGateway(port=25333)
launcher.start()
```

### 3. Basic Usage Example

python
from py_sikulix import Screen, Pattern, Key

def main():
    # Get the main screen
    screen = Screen()

    # Find the image
    try:
        # Find and click the image
        if match := screen.find(“button.png”):
            match.click()
            
        # Input text
        screen.type(“Hello, World!”)
        screen.type(Key.ENTER)
        
        # Use a key combination
        screen.key_down(Key.WIN)
        screen.type(“r”)    # Note: Must use lowercase letters to trigger key combination
        screen.key_up(Key.WIN)
        
    except Exception as e:
        print(f“Error: {e}”)

if **name** == “**main**”:
    main()

```

## Core Classes

### Screen and Regions

- `Screen`: Represents the entire screen
- `Region`: Represents a rectangular area on the screen
- `Location`: Represents a coordinate point on the screen

### Image Recognition

- `Pattern`: Defines image search parameters (similarity, offset, scaling)
- `Match`: Represents image matching results (position, size, similarity)

### Application Control

- `App`: Application management (start, close, focus)

### Input Devices

- `Key`: Keyboard key constants
- `Btn`: Mouse button constants

### Configuration

- `Settings`: Global configuration management

## Usage Examples

### Image Recognition

python
from py_sikulix import Screen, Pattern

screen = Screen()

# Find image
match = screen.find(“image.png”)
if match:
    print(f“Image found: ({match.x}, {match.y})”)
    print(f“Similarity: {match.get_score():.2f}”)

# Search using pattern
pattern = Pattern(“image.png”).similar(0.8)
match = screen.find(pattern)
```

### Region Operations

```python
from py_sikulix import Region

# Create region
region = Region(100, 100, 300, 200)

# Get region properties
print(f“Position: ({region.x}, {region.y})”)
print(f“Size: {region.w}x{region.h}”)

# Get center position
center = region.get_center()
print(f“Center: ({center.x}, {center.y})”)

# Create extended region
nearby = region.nearby(50)
```

### Application Control

```python
from py_sikulix import App

app = App(“Notepad”)
app.open()

if app.is_running():
    print(f“PID: {app.get_pid()}”)
    app.focus()
    
    # Get window region
    window = app.focused_window()
    print(f“Window size: {window.w}x{window.h}”)

app.close()
```

### Mouse and Keyboard Operations

```python
from py_sikulix import Region, Key, Btn

region = Region(100, 100, 300, 200)

# Mouse operations
region.click()                    # Left-click
region.click(key=Btn.RIGHT)          # Right-click
region.double_click()              # Double-click
region.mouse_down()                # Mouse down
region.mouse_move(50, 50)          # Mouse move
region.mouse_up()                 # Mouse release
region.wheel(direction=Btn.WHEEL_DOWN)  # Scroll wheel down

# Keyboard operations
region.key_down(Key.WIN)          # Press Win key
region.type(“r”)                  # Input character
region.key_up(Key.WIN)            # Release Win key
```

## Advanced Usage

### Configuration Parameters

```python
from py_sikulix import Settings

# Set similarity threshold
Settings.min_similarity = 0.8

# Set mouse movement delay
Settings.move_mouse_delay = 0.5

# Set scan timeout
Settings.wait_scan_rate = 2  # Scans per second
```

## Development

### Running Tests

```bash
# Run unit tests
pytest tests/test_location.py -v

# Run all tests
pytest -v

# Run integration tests (Requires real Java gateway)
pytest --run-integration tests/
```

### Code Checking

```bash
# Run ruff linter
ruff check src/

# Run mypy type checking
mypy src/

# Format code
ruff format src/
```

## Project Structure

```
py-sikulix/
├── src/py_sikulix/
│   ├── __init__.py         # Package exports
│   ├── client.py           # Client management, global CLIENT singleton
│   ├── base_region.py      # Base region class, shared by Region/Match
│   ├── region.py           # Region and Screen classes
│   ├── screen.py           # Screen class
│   ├── match.py            # Match class
│   ├── pattern.py          # Pattern class
│   ├── app.py              # App class
│   ├── location.py         # Location class
│   ├── settings.py         # Settings configuration class
│   ├── keys.py             # Key and Btn constants
│   ├── gateway.py          # Java gateway launcher
│   └── exceptions.py       # Exception classes
├── tests/
│   ├── conftest.py         # Pytest fixtures
│   ├── test_region.py
│   ├── test_pattern.py
│   └── test_location.py
├── examples/               # Sample images
├── sikulixide-2.0.5.2103.jar  # SikuliX IDE (must be downloaded separately)
├── pyproject.toml          # Project configuration
└── README.md
```

## Dependencies

- **Py4J**: Java process communication
- **Java 8+**: Java runtime required by SikuliX

## Version History

### v0.1.0 (2024-02-24)

- Initial release
- Basic screen manipulation and image recognition
- Mouse, keyboard, and application control
- Region management and configuration system

## License

Apache 2.0

## Contributing

Issues and Pull Requests are welcome!

## Contact

- Report issues: [Issues](https://github.com/0xn0ne/py-sikulix/issues)
- Feature requests: [Discussions](https://github.com/0xn0ne/py-sikulix/discussions)

## Acknowledgments

Based on work from the SikuliX project: <https://sikulix-2014.readthedocs.io/>

# AGENTS.md - SikuliX Python Client

AI coding agent guidance for this repository.

## Project Overview

Python client library for SikuliX GUI automation via Py4J. Wraps SikuliX Java classes (Screen, Region, App, Pattern, Match, Location, Key, Button, Settings) with Python-friendly interfaces and bilingual (Chinese/English) documentation.

## Build/Lint/Test Commands

### Prerequisites

```bash
# Install dependencies
pip install -e ".[dev]"

# Java Requirements: JDK with JAVA_HOME set; sikulixide.jar in project directory
```

### Testing

```bash
# Run all tests (gateway will be auto-started if not running)
pytest

# Run specific test file
pytest tests/test_region.py
pytest tests/test_pattern.py
pytest tests/test_location.py

# Run specific test class
pytest tests/test_region.py::TestRegionCreation -v

# Run with coverage
pytest --cov=src/py_sikulix --cov-report=html
```

**Note**: Tests will automatically detect if SikuliX gateway is running. If not, it will start the gateway before tests and stop it after tests complete. Gateway requires `sikulixide-2.0.5.2103.jar` in the project root directory.

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_region.py
pytest tests/test_pattern.py
pytest tests/test_location.py

# Run with coverage
pytest --cov=src/py_sikulix --cov-report=html

# Run integration tests (requires Java gateway)
pytest --run-integration tests/
```

### Linting & Type Checking

```bash
# Run ruff linter
ruff check src/

# Run ruff with auto-fix
ruff check --fix src/

# Run mypy type checker
mypy src/

# Format code
ruff format src/
```

### Gateway Commands

```bash
# Start Java gateway (REQUIRED before client operations)
python -m py_sikulix.gateway start
python -m py_sikulix.gateway start [port]    # Default port: 25333

# Test gateway connection
python -m py_sikulix.gateway test

# Stop gateway
python -m py_sikulix.gateway stop
```

### Module Self-Tests

```bash
# Each module has if __name__ == "__main__": block for quick testing
python -m py_sikulix.region
python -m py_sikulix.keys
```

## Class Hierarchy

```
BaseRegion (base_region.py)     # Shared base: position props + interaction methods
├── Region (region.py)          # Search methods: find, wait, exists + region creation
│   └── Screen (screen.py)       # Full screen + capture
└── Match (match.py)            # Match result: get_score, get_target + inherited interaction
```

**Key Design**: Region.find() returns Match; Match inherits click/hover/type from BaseRegion.

## Code Style

### File Header & Imports

```python
#!/usr/bin/env python3
#
"""Bilingual docstring (Chinese primary, English secondary)."""

# 1. Standard library
import logging
import pathlib
from typing import List, Optional, Union, Tuple, TYPE_CHECKING

# 2. Third-party (py4j)
from py4j.java_gateway import JavaObject
from py4j.protocol import Py4JJavaError

# 3. Local (relative imports from py_sikulix)
from py_sikulix.base_region import BaseRegion
from py_sikulix.client import CLIENT
from py_sikulix.location import Location

# Forward references for circular imports
if TYPE_CHECKING:
    from py_sikulix.match import Match
```

### Class Patterns

```python
# Raw instance pattern - store Java reference
def __init__(self, java_instance):
    self._raw = java_instance  # type: ignore
    self.x = java_instance.getX()

# Factory method - create from Python
@classmethod
def new(cls, x: int, y: int) -> "Location":
    return cls(CLIENT.Location(x, y))  # type: ignore

# Fluent API - return self for setters
def set_x(self, x: int) -> "Region":
    self._raw.setX(x)  # type: ignore
    return self

# Property pattern - see settings.py
@property
def min_similarity(self) -> float:
    return self._raw.MinSimilarity  # type: ignore
```

### Type Hints & Java Interop

```python
# Always use type hints
def find(self, target: Union[str, pathlib.Path, Pattern]) -> Optional[Match]:
    ...

# Always add # type: ignore for Java calls
self._raw.find(target)  # type: ignore
CLIENT.Screen()  # type: ignore
except Py4JJavaError:  # type: ignore

# Handle Union types with isinstance checks
def click(self, psmrl: Union[Pattern, str, Match, Location]) -> int:
    if isinstance(psmrl, (Pattern, Match, Location)):
        psmrl = psmrl._raw
    return self._raw.click(psmrl)  # type: ignore
```

### Docstrings (Bilingual)

```python
def find(self, target: Union[str, pathlib.Path, Pattern]) -> Optional[Match]:
    """
    在区域内查找目标图像

    Find a target image within the region.

    Args:
        target: 要查找的图像路径或 Pattern 对象
            The image path or Pattern object to find.

    Returns:
        找到的第一个匹配结果，如果未找到则返回 None
        The first match found, or None if not found.
    """
```

### Error Handling

```python
# Catch Py4JJavaError, return None/False on failure (don't raise)
try:
    result = self._raw.find(target)  # type: ignore
except Py4JJavaError:
    return None
return Match(result)

# For methods that should return int, handle errors gracefully
def key_down(self, keys: Union[str, list[str]]) -> int:
    try:
        result = self._raw.keyDown(keys)  # type: ignore
        return int(result) if result is not None else 0
    except Exception as e:
        logger.error(f"key_down 操作失败: {e}")
        return 0
```

## Naming Conventions

| Type | Convention | Examples |
|------|------------|----------|
| Classes | PascalCase | `Region`, `SikuliXClient` |
| Methods | snake_case | `find_all`, `get_bounds` |
| Constants | UPPER_SNAKE_CASE | `LEFT`, `WHEEL_DOWN` |
| Private | `_prefix` | `_init_classes` |
| Java methods | Preserve original | `getX()`, `findAll()` |

## Project Structure

```
py-sikulix/
├── src/py_sikulix/
│   ├── __init__.py         # Package exports
│   ├── client.py           # SikuliXClient, global CLIENT singleton
│   ├── base_region.py      # BaseRegion - shared Region/Match base
│   ├── region.py           # Region, Screen classes
│   ├── match.py            # Match class
│   ├── pattern.py          # Pattern class
│   ├── app.py              # App class
│   ├── location.py         # Location class
│   ├── settings.py         # Settings class (property-based)
│   ├── keys.py             # Key, Button constants
│   ├── gateway.py          # Java gateway launcher
│   └── exceptions.py       # SikuliXError, FindFailed
├── tests/
│   ├── conftest.py         # Pytest fixtures
│   ├── test_region.py
│   ├── test_pattern.py
│   └── test_location.py
├── examples/
├── pyproject.toml          # Project configuration
└── README.md
```

## Important Notes

1. **Gateway Required**: Run `python -m py_sikulix.gateway start` before any client operations
2. **Source Path**: Code is in `src/py_sikulix/` not `client/`
3. **TYPE_CHECKING**: Required for circular imports (Region ↔ Match)
4. **Path Handling**: Support both `str` and `pathlib.Path` inputs
5. **Bilingual Docs**: All docstrings include Chinese and English
6. **Return Types**: Methods should return appropriate types (int for operations, None for not found)
7. **Error Handling**: Always add try-except for Java interop calls to prevent crashes
8. **Py4J Dependency**: All Java objects accessed via Py4J need `# type: ignore` comments

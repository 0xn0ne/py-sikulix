# AGENTS.md - SikuliX Python Client

AI coding agent guidance for this repository.

## Project Overview

Python client library for SikuliX GUI automation via Py4J. Wraps SikuliX Java classes with Python-friendly interfaces and bilingual (Chinese/English) documentation.

## Build/Lint/Test Commands

### Prerequisites

```bash
pip install -e ".[dev]"  # JDK with JAVA_HOME required; sikulixide.jar in project root
```

### Testing

```bash
pytest                              # All tests (gateway auto-started)
pytest tests/test_region.py         # Single file
pytest tests/test_region.py::TestRegionCreation -v  # Single class
pytest tests/test_region.py::TestRegionCreation::test_region_creation -v  # Single test
pytest --cov=src/py_sikulix        # With coverage
pytest --run-integration tests/    # Integration tests (requires Java)
```

### Linting & Type Checking

```bash
ruff check src/          # Lint
ruff check --fix src/   # Auto-fix
ruff format src/         # Format
mypy src/                # Type check
```

### Gateway

```bash
python -m py_sikulix.gateway start     # Start (REQUIRED)
python -m py_sikulix.gateway start [port]  # Default: 25333
python -m py_sikulix.gateway test      # Test connection
python -m py_sikulix.gateway stop      # Stop
```

## Class Hierarchy

```
BaseRegion (base_region.py)     # Shared: position props + interaction
├── Region (region.py)          # find, wait, exists
│   └── Screen (screen.py)       # Full screen + capture
└── Match (match.py)            # Inherits click/hover/type
```

## Code Style

### Imports (3-section order)

```python
#!/usr/bin/env python3
"""Bilingual docstring (Chinese primary, English secondary)."""

# 1. Standard library
import logging
import pathlib
from typing import List, Optional, Union, Tuple, TYPE_CHECKING

# 2. Third-party (py4j)
from py4j.java_gateway import JavaObject
from py4j.protocol import Py4JJavaError

# 3. Local
from py_sikulix.base_region import BaseRegion
from py_sikulix.client import CLIENT

if TYPE_CHECKING:
    from py_sikulix.match import Match
```

### Class Patterns

```python
# Raw instance - store Java reference
def __init__(self, java_instance):
    self._raw = java_instance  # type: ignore
    self.x = java_instance.getX()

# Factory method
@classmethod
def new(cls, x: int, y: int) -> "Location":
    return cls(CLIENT.Location(x, y))  # type: ignore

# Fluent API - return self
def set_x(self, x: int) -> "Region":
    self._raw.setX(x)  # type: ignore
    return self

# Property
@property
def min_similarity(self) -> float:
    return self._raw.MinSimilarity  # type: ignore
```

### Type Hints & Java Interop

- Always use type hints
- Always add `# type: ignore` for Py4J calls

```python
def click(self, psmrl: Union[Pattern, str, Match, Location]) -> int:
    if isinstance(psmrl, (Pattern, Match, Location)):
        psmrl = psmrl._raw
    return self._raw.click(psmrl)  # type: ignore
```

### Docstrings (Bilingual)

```python
def find(self, target: Union[str, pathlib.Path, "Pattern"]) -> Optional["Match"]:
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
# Return None/False on failure (don't raise)
try:
    result = self._raw.find(target)  # type: ignore
except Py4JJavaError:
    return None
return Match(result)

# For int returns
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
| Java methods | Preserve | `getX()`, `findAll()` |

## Project Structure

```
src/py_sikulix/
├── __init__.py      # Package exports
├── client.py        # SikuliXClient, global CLIENT singleton
├── base_region.py   # Shared Region/Match base
├── region.py        # Region, Screen classes
├── match.py         # Match class
├── pattern.py       # Pattern class
├── app.py           # App class
├── location.py      # Location class
├── settings.py      # Settings (property-based)
├── keys.py          # Key, Button constants
├── gateway.py       # Java gateway launcher
└── exceptions.py    # SikuliXError, FindFailed
```

## Important Notes

1. **Gateway Required**: Run `python -m py_sikulix.gateway start` before client ops
2. **Source Path**: Code in `src/py_sikulix/`
3. **TYPE_CHECKING**: Required for circular imports (Region ↔ Match)
4. **Path Handling**: Support both `str` and `pathlib.Path`
5. **Bilingual Docs**: All docstrings include Chinese and English
6. **Py4J**: All Java accesses need `# type: ignore`

## Lint Config

- **ruff**: E/W/F/I/B/SIM/UP; ignores E501/B904/UP007/UP045
- **mypy**: strict mode, py4j.* ignored
- **pytest markers**: `@pytest.mark.integration`, `@pytest.mark.slow`

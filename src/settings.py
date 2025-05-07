# src/settings.py

import os
import ast
from pathlib import Path
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    # IDE увидят эти объявления, но они не будут выполняться в runtime
    SCREEN_WIDTH: int
    SCREEN_HEIGHT: int
    FPS: int
    PLAYER_WIDTH: int
    PLAYER_HEIGHT: int
    MENU_BG_IMAGE: str
    BRIEFING_BG_IMAGE: str
    PLAYER_IMAGE: str
    AK_IMAGE: str
    AK_WIDTH: int
    AK_HEIGHT: int
    DEAD_TANK_IMAGE: str
    DEAD_TANK_WIDTH: int
    DEAD_TANK_HEIGHT: int
    LEVEL_PATHS: List[str]
    TITLE: str


# Path to the settings file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'settings.txt')

def _load_constants(path):
    constants = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            name, value = map(str.strip, line.split('=', 1))
            try:
                # Safely evaluate literals: numbers, booleans, strings, tuples, lists, dicts
                constants[name] = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                # Fallback to raw string
                constants[name] = value
    return constants

# Load and inject into module globals
_constants = _load_constants(CONFIG_PATH)
for _name, _value in _constants.items():
    globals()[_name] = _value

# Clean up namespace
del _load_constants, _constants, os, ast

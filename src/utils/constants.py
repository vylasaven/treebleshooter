"""
Module: constants
Purpose: Application-wide constants and configuration values
Author: Allen (with Claude Code assistance)
Date Created: 2025-08-15
"""

# Application metadata
APP_NAME = "Treebleshooter"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Allen"

# Window settings
MAIN_WINDOW_WIDTH = 1200
MAIN_WINDOW_HEIGHT = 800
MAIN_WINDOW_MIN_WIDTH = 800
MAIN_WINDOW_MIN_HEIGHT = 600

# File settings
GUIDE_FILE_EXTENSION = ".tsg"  # Troubleshooting Guide
GUIDE_FILE_FILTER = "Troubleshooting Guides (*.tsg);;JSON Files (*.json);;All Files (*.*)"
DEFAULT_SAVE_DIRECTORY = "data"

# UI Settings
BUTTON_HEIGHT = 36
BUTTON_MIN_WIDTH = 100
ICON_SIZE = 24
PADDING_SMALL = 8
PADDING_MEDIUM = 16
PADDING_LARGE = 24

# Colors (can be overridden by themes) - Modern technological theme
COLOR_PRIMARY = "#00D4FF"       # Cyan/Electric blue
COLOR_SUCCESS = "#00FF88"       # Neon green  
COLOR_WARNING = "#FFB800"       # Amber
COLOR_ERROR = "#FF3366"         # Hot pink/red
COLOR_BACKGROUND = "#0A0E27"    # Deep dark blue
COLOR_SURFACE = "#1A1F3A"       # Dark blue-gray
COLOR_TEXT_PRIMARY = "#E8EAED"  # Light gray
COLOR_TEXT_SECONDARY = "#9AA0A6" # Medium gray

# Tree structure limits
MAX_TREE_DEPTH = 20
MAX_ANSWERS_PER_NODE = 10
MIN_ANSWERS_PER_NODE = 2

# Auto-save settings
AUTOSAVE_ENABLED = True
AUTOSAVE_INTERVAL_SECONDS = 300  # 5 minutes

# Logging settings
LOG_LEVEL = "DEBUG"
LOG_FILE = "logs/app.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
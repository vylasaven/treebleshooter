# CLAUDE.md - AI Assistant Context for Treebleshooter

## Project Overview
Treebleshooter is a PyQt5 desktop application for creating and executing branching troubleshooting guides. This project is designed for Allen, a beginner developer, so code clarity and maintainability are paramount.

## Development Philosophy
- **CLARITY OVER CLEVERNESS**: Write code that a beginner can understand
- **EXPLICIT NAMING**: Use full, descriptive names (e.g., `create_troubleshooting_node()` not `mk_node()`)
- **CONSISTENT PATTERNS**: Use the same patterns throughout the codebase
- **COMPREHENSIVE COMMENTS**: Explain WHY, not just WHAT
- **MODULAR DESIGN**: Small, single-purpose functions and classes

## Naming Conventions

### Files
- **Snake_case** for Python files: `troubleshooting_guide_creator.py`
- **Descriptive names**: `save_load_manager.py` not `io.py`

### Classes
- **PascalCase**: `TroubleshootingNode`, `GuideCreatorWizard`
- **Suffix by type**: 
  - Windows: `MainWindow`, `CreatorWindow`
  - Dialogs: `SaveDialog`, `LoadDialog`
  - Widgets: `NodeWidget`, `TreeViewWidget`
  - Managers: `DataManager`, `StyleManager`

### Functions/Methods
- **Snake_case**: `load_guide_from_file()`, `create_new_node()`
- **Verb-first**: `get_`, `set_`, `create_`, `delete_`, `update_`, `validate_`
- **Boolean returns**: `is_valid()`, `has_children()`, `can_save()`

### Variables
- **Snake_case**: `current_node`, `guide_data`, `selected_path`
- **Descriptive**: `troubleshooting_steps` not `steps`
- **Type hints always**: `node_id: str`, `children: List[TroubleshootingNode]`

## Project Structure

```
treebleshooter/
├── main.py                          # Entry point - keep minimal
├── requirements.txt                 # All dependencies
├── CLAUDE.md                       # This file - AI context
├── GETTING_STARTED.md              # User documentation
├── PROMPTS_LOG.txt                 # Development history
│
├── src/
│   ├── __init__.py
│   │
│   ├── models/                    # Data structures
│   │   ├── __init__.py
│   │   ├── troubleshooting_node.py    # Node class
│   │   ├── troubleshooting_guide.py   # Guide container
│   │   └── guide_metadata.py          # Guide info
│   │
│   ├── views/                     # UI components
│   │   ├── __init__.py
│   │   ├── main_window.py            # Primary application window
│   │   ├── guide_creator_wizard.py   # Guide creation interface
│   │   ├── guide_executor_view.py    # Guide execution interface
│   │   ├── widgets/
│   │   │   ├── node_editor_widget.py
│   │   │   ├── tree_visualizer_widget.py
│   │   │   └── help_overlay_widget.py
│   │   └── dialogs/
│   │       ├── save_dialog.py
│   │       ├── load_dialog.py
│   │       └── about_dialog.py
│   │
│   ├── controllers/               # Business logic
│   │   ├── __init__.py
│   │   ├── guide_controller.py       # Guide management
│   │   ├── navigation_controller.py  # Tree navigation
│   │   └── file_controller.py        # Save/load operations
│   │
│   └── utils/                     # Helper functions
│       ├── __init__.py
│       ├── json_handler.py          # JSON serialization
│       ├── validators.py            # Input validation
│       ├── constants.py             # App-wide constants
│       └── style_manager.py         # Theme management
│
├── data/                          # Saved guides (JSON files)
│   └── examples/                 # Example guides
│
├── resources/                     # Assets
│   ├── icons/
│   ├── images/
│   └── styles/
│       └── main_theme.qss
│
└── tests/                        # Unit tests
    ├── test_models.py
    ├── test_controllers.py
    └── test_utils.py
```

## Code Standards

### Every Python File Must Have:
```python
"""
Module: [module_name]
Purpose: [Clear description of what this module does]
Author: Allen (with Claude Code assistance)
Date Created: [date]
"""

from typing import List, Dict, Optional, Any  # Always use type hints
import logging

logger = logging.getLogger(__name__)  # Every module gets a logger
```

### Every Class Must Have:
```python
class TroubleshootingNode:
    """
    Represents a single node in a troubleshooting decision tree.
    
    Each node contains a question/statement and possible answers
    that lead to other nodes or final solutions.
    """
    
    def __init__(self, node_id: str, question: str):
        """
        Initialize a troubleshooting node.
        
        Args:
            node_id: Unique identifier for this node
            question: The question or statement displayed to user
        """
        self.node_id = node_id
        self.question = question
        self.answers: List[Answer] = []
        logger.debug(f"Created node with ID: {node_id}")
```

### Every Function Must Have:
```python
def save_guide_to_file(guide: TroubleshootingGuide, filepath: str) -> bool:
    """
    Save a troubleshooting guide to a JSON file.
    
    Args:
        guide: The guide object to save
        filepath: Full path where the file should be saved
        
    Returns:
        bool: True if save successful, False otherwise
        
    Raises:
        IOError: If file cannot be written
        ValueError: If guide data is invalid
    """
    # Implementation here
    pass
```

## Common Patterns to Use

### 1. Error Handling Pattern
```python
def safe_operation():
    try:
        # Attempt operation
        result = perform_operation()
        logger.info("Operation successful")
        return result
    except SpecificError as e:
        logger.error(f"Specific error occurred: {e}")
        # Show user-friendly message
        show_error_dialog("Something went wrong. Please try again.")
        return None
    except Exception as e:
        logger.exception("Unexpected error")
        # Log full traceback but show simple message to user
        show_error_dialog("An unexpected error occurred.")
        return None
```

### 2. Signal/Slot Pattern (PyQt5)
```python
class GuideCreatorWizard(QWidget):
    # Define signals at class level
    guide_created = pyqtSignal(TroubleshootingGuide)
    
    def __init__(self):
        super().__init__()
        # Connect signals to slots
        self.save_button.clicked.connect(self.on_save_clicked)
    
    def on_save_clicked(self):
        """Handle save button click."""
        # Naming: on_[widget]_[action]
        pass
```

### 3. Validation Pattern
```python
def validate_node_data(node_data: dict) -> tuple[bool, str]:
    """
    Validate node data before processing.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not node_data.get('question'):
        return False, "Question is required"
    
    if len(node_data.get('answers', [])) < 2:
        return False, "At least 2 answers required"
    
    return True, ""
```

## UI/UX Guidelines

### Windows and Dialogs
- Always include tooltips for buttons
- Provide keyboard shortcuts for common actions
- Show loading indicators for long operations
- Confirm destructive actions with dialogs

### Help System
- Every major screen has a "?" help button
- First-time users see an automatic tutorial overlay
- Tooltips explain every non-obvious element
- Include example guides in the data folder

### Visual Design
- Use consistent spacing (8px grid system)
- Primary action buttons are blue, destructive are red
- Dark mode and light mode support
- Icons for all major actions

## Testing Requirements

### Before Committing:
1. Run all tests: `python -m pytest tests/`
2. Check code style: `python -m black src/`
3. Type checking: `python -m mypy src/`
4. Manual testing of new features

### Test Coverage Goals:
- Models: 100% coverage
- Controllers: 80% coverage
- Utils: 100% coverage
- Views: Manual testing (UI)

## Common Tasks

### Adding a New Feature
1. Create feature branch: `git checkout -b feature/feature-name`
2. Update models if needed
3. Create/update view components
4. Add controller logic
5. Write tests
6. Update documentation
7. Test manually
8. Commit with clear message

### Debugging Tips
- Use `logger.debug()` liberally
- Check `logs/app.log` for detailed output
- Use PyQt5's built-in debugging: `export QT_DEBUG_PLUGINS=1`
- Visual debugging with `qtpy` package

## For Claude Code

When Allen asks for help:

1. **Always maintain code clarity** - He's learning, so readable > clever
2. **Add helpful comments** - Explain complex logic
3. **Use consistent patterns** - Match existing code style
4. **Suggest small steps** - Break big features into small PRs
5. **Provide examples** - Show how to use new features
6. **Update documentation** - Keep GETTING_STARTED.md current
7. **Test suggestions** - Ensure code runs before suggesting

## Important Reminders

- This is Allen's first real project - be encouraging!
- Prioritize working code over perfect code
- Make the app visually appealing to maintain motivation
- Keep the architecture simple but extensible
- Document everything as if explaining to a friend

## Future Considerations

The app should be designed to eventually support:
- Multiple guide formats (not just tree)
- AI-assisted guide creation
- Web/mobile versions
- Collaborative editing
- Analytics on guide usage
- Plugin system for extensions

Keep these in mind but don't over-engineer early!
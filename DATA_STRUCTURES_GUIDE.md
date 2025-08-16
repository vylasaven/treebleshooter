# Treebleshooter Data Structures Guide

## Complete Data Structure Map & Feature Usage

This document provides a comprehensive overview of every data structure in the Treebleshooter application, explaining what each one does and which features use them.

---

## 1. Core Data Models (`src/models/`)

### 1.1 NodeAnswer (dataclass)
**Location:** `src/models/troubleshooting_node.py`

**Structure:**
```python
@dataclass
class NodeAnswer:
    answer_text: str                    # The text displayed for this answer
    next_node_id: Optional[str] = None  # ID of the next node (None if solution)
    is_solution: bool = False            # True if this ends the troubleshooting
    solution_text: Optional[str] = None  # Final solution text if endpoint
    answer_id: str = field(default_factory=lambda: str(uuid.uuid4()))
```

**Used By:**
- **Guide Creator Wizard:** When adding possible answers to questions
- **Guide Executor View:** Displaying answer choices to users
- **Save/Load System:** Serialized as part of node data
- **Navigation Logic:** Determines path through troubleshooting tree

**Purpose:** Represents a single answer choice in a troubleshooting step, containing both the answer text and where it leads (next node or solution).

---

### 1.2 TroubleshootingNode (class)
**Location:** `src/models/troubleshooting_node.py`

**Structure:**
```python
class TroubleshootingNode:
    node_id: str                           # Unique identifier
    question: str                          # Main question/instruction
    description: Optional[str]             # Extended description
    help_text: Optional[str]               # Additional help info
    answers: List[NodeAnswer]              # Possible answers
    parent_node_id: Optional[str]          # Reference to parent node
```

**Key Methods:**
- `add_answer()` - Add a new answer option
- `remove_answer()` - Remove an answer
- `is_leaf_node()` - Check if node has no children
- `is_valid()` - Validate node structure
- `to_dict()/from_dict()` - Serialization

**Used By:**
- **Guide Creator Wizard:** Core building block for creating guides
- **Guide Executor View:** Displays current step to user
- **Tree Visualization:** (future feature) Would render these nodes
- **Path History:** Tracks navigation through nodes
- **Validation System:** Ensures guide integrity

**Purpose:** The fundamental unit of a troubleshooting guide - each node is one decision point with a question and multiple possible answers.

---

### 1.3 GuideMetadata (dataclass)
**Location:** `src/models/guide_metadata.py`

**Structure:**
```python
@dataclass
class GuideMetadata:
    title: str                                # Guide title
    description: str                           # What this guide helps troubleshoot
    author: str = "Unknown"                   # Who created this guide
    version: str = "1.0.0"                    # Version number
    created_date: datetime                     # When created
    last_modified_date: datetime               # Last modification
    tags: List[str]                          # Categories/tags
    difficulty_level: str = "Beginner"        # Beginner/Intermediate/Advanced
    estimated_time_minutes: Optional[int]     # Estimated completion time
```

**Key Methods:**
- `update_modified_date()` - Update timestamp
- `add_tag()/remove_tag()` - Manage tags
- `increment_version()` - Version management

**Used By:**
- **Guide Library Display:** Shows title, author, difficulty
- **Guide Creator Wizard:** First page collects this metadata
- **Search/Filter:** (future) Would use tags and difficulty
- **Guide Statistics:** Displays estimated time
- **Export System:** Includes metadata in exports

**Purpose:** Contains all the "about" information for a guide - who made it, when, how difficult it is, etc.

---

### 1.4 TroubleshootingGuide (class)
**Location:** `src/models/troubleshooting_guide.py`

**Structure:**
```python
class TroubleshootingGuide:
    metadata: GuideMetadata                    # Guide information
    nodes: Dict[str, TroubleshootingNode]     # All nodes (node_id -> node)
    root_node_id: Optional[str]               # Starting node ID
```

**Key Methods:**
- `add_node()/remove_node()` - Manage nodes
- `get_root_node()` - Get starting point
- `get_child_nodes()` - Get node's children
- `get_all_paths()` - Find all possible paths
- `get_statistics()` - Calculate guide stats
- `validate()` - Check guide integrity
- `_has_cycles()` - Detect circular references

**Used By:**
- **Main Application:** Primary data container for guides
- **Guide Executor:** Navigates through the guide
- **Save/Load System:** Top-level object that gets serialized
- **Guide Library:** Stores collection of guides
- **Validation System:** Ensures guide is valid before saving
- **Statistics Display:** Shows path counts, node counts

**Purpose:** The complete container for a troubleshooting guide, holding all nodes and metadata together.

---

### 1.5 ProblemCategory (dataclass)
**Location:** `src/models/product_catalog.py`

**Structure:**
```python
@dataclass
class ProblemCategory:
    category_id: str                          # Unique identifier
    category_name: str                        # Display name
    description: str                          # Category description
    icon_name: Optional[str] = None          # For future icon support
    guide_ids: List[str]                     # List of guide IDs in this category
```

**Used By:**
- **Product Selector Widget:** Shows categories for selected product
- **Guide Organization:** Groups related guides together
- **Navigation Hierarchy:** Product → Category → Guide

**Purpose:** Groups troubleshooting guides by problem type (e.g., "Toast Malfunctions", "AI Personality Issues").

---

### 1.6 Product (dataclass)
**Location:** `src/models/product_catalog.py`

**Structure:**
```python
@dataclass
class Product:
    product_id: str                           # Unique identifier
    product_name: str                         # Display name
    description: str                          # Product description
    manufacturer: str = "Generic Corp"        # Manufacturer name
    version: str = "1.0"                     # Product version
    icon_name: Optional[str] = None          # For future icon support
    problem_categories: Dict[str, ProblemCategory]  # Categories for this product
```

**Key Methods:**
- `add_category()/remove_category()` - Manage categories
- `get_all_guide_ids()` - Get all guides for product

**Used By:**
- **Product Selector Widget:** Top-level selection
- **Guide Organization:** Highest level of hierarchy
- **Catalog Management:** Product CRUD operations

**Purpose:** Represents a product that can have troubleshooting guides (e.g., "Smart Toaster 3000").

---

### 1.7 ProductCatalog (class)
**Location:** `src/models/product_catalog.py`

**Structure:**
```python
class ProductCatalog:
    products: Dict[str, Product]              # All products (product_id -> product)
    last_updated: datetime                    # Last modification time
```

**Key Methods:**
- `add_product()/remove_product()` - Manage products
- `find_guide_location()` - Find which product/category has a guide
- `get_statistics()` - Catalog statistics
- `create_default_catalog()` - Generate example data

**Used By:**
- **Main Window:** Initializes with catalog
- **Product Selector:** Displays available products
- **Save/Load System:** Persists catalog to JSON
- **Guide Management:** Organizes all guides

**Purpose:** Top-level container for all products and their associated troubleshooting guides.

---

## 2. View Components (`src/views/`)

### 2.1 MainWindow (QMainWindow)
**Location:** `src/views/main_window.py`

**Internal Data:**
```python
self.current_guide: Optional[TroubleshootingGuide]  # Currently active guide
self.guide_library: List[TroubleshootingGuide]      # All loaded guides
self.content_stack: QStackedWidget                  # Stack of different views
self.guide_list: QListWidget                        # Sidebar guide list
```

**Features Using This:**
- **Application Shell:** Contains all other views
- **Navigation:** Menu bar, toolbar, status bar
- **View Switching:** Between welcome, creator, executor
- **Guide Library Management:** List and selection

---

### 2.2 GuideCreatorWizard (QWidget)
**Location:** `src/views/guide_creator_wizard.py`

**Internal Data:**
```python
self.current_guide: Optional[TroubleshootingGuide]  # Guide being created/edited
self.current_node: Optional[TroubleshootingNode]    # Node being edited
self.stack: QStackedWidget                          # Wizard pages
# Form fields:
self.title_input: QLineEdit
self.description_input: QTextEdit
self.author_input: QLineEdit
self.difficulty_combo: QComboBox
self.time_input: QSpinBox
```

**Features Using This:**
- **Guide Creation:** Step-by-step guide building
- **Metadata Collection:** First page of wizard
- **Node Editing:** Add/edit questions and answers
- **Guide Validation:** Before saving
- **Review Page:** Summary before finishing

---

### 2.3 GuideExecutorView (QWidget)
**Location:** `src/views/guide_executor_view.py`

**Internal Data:**
```python
self.current_guide: Optional[TroubleshootingGuide]  # Guide being executed
self.current_node: Optional[TroubleshootingNode]    # Current step
self.path_history: List[str]                        # Node IDs visited
self.answer_button_group: QButtonGroup              # Radio buttons for answers
```

**Features Using This:**
- **Guide Execution:** Step through troubleshooting
- **Answer Selection:** Radio buttons for choices
- **Navigation:** Back button using path history
- **Progress Tracking:** Progress bar
- **Solution Display:** Final answer presentation

---

### 2.4 ProductSelectorWidget (QWidget)
**Location:** `src/views/product_selector_widget.py`

**Internal Data:**
```python
self.catalog: ProductCatalog                        # Product catalog
self.current_product: Optional[Product]             # Selected product
self.current_category: Optional[ProblemCategory]    # Selected category
# UI elements:
self.product_combo: QComboBox                       # Product dropdown
self.category_combo: QComboBox                      # Category dropdown
self.guides_list: QListWidget                       # Available guides
```

**Features Using This:**
- **Product Selection:** Hierarchical navigation
- **Category Filtering:** Show relevant problems
- **Guide Discovery:** List available guides
- **Statistics Display:** Product/category counts

---

## 3. Controllers (`src/controllers/`)

### 3.1 FileController (class)
**Location:** `src/controllers/file_controller.py`

**Internal Data:**
```python
self.data_dir: Path                                 # Main data directory
self.guides_dir: Path                               # User guides directory
self.examples_dir: Path                             # Example guides directory
self.catalog_file: Path                             # Product catalog location
```

**Key Methods:**
- `save_guide()/load_guide()` - Guide persistence
- `save_catalog()/load_catalog()` - Catalog persistence
- `list_guide_files()` - Find all guides
- `export_guide_to_format()` - Export to HTML/Markdown

**Features Using This:**
- **Save/Load System:** All file operations
- **Import/Export:** Different format support
- **Example Loading:** Load demo guides
- **Auto-save:** (future) Periodic saving

---

## 4. Utility Classes (`src/utils/`)

### 4.1 ExampleGuideGenerator (class)
**Location:** `src/utils/example_guides.py`

**Static Methods:**
- `create_all_guides()` - Generate all examples
- `create_[specific]_guide()` - Individual guide creators

**Features Using This:**
- **Demo Content:** Whimsical example guides
- **First-Run Experience:** Pre-populated content
- **Testing:** Sample data for development

---

### 4.2 Constants Module
**Location:** `src/utils/constants.py`

**Key Constants:**
```python
# Application
APP_NAME, APP_VERSION, APP_AUTHOR

# Window Settings
MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT

# UI Settings
BUTTON_HEIGHT, ICON_SIZE, PADDING_*

# Colors (Modern Tech Theme)
COLOR_PRIMARY = "#00D4FF"      # Cyan
COLOR_SUCCESS = "#00FF88"      # Neon green
COLOR_BACKGROUND = "#0A0E27"   # Deep blue

# Tree Structure Limits
MAX_TREE_DEPTH = 20
MAX_ANSWERS_PER_NODE = 10

# File Settings
GUIDE_FILE_EXTENSION = ".tsg"
```

**Features Using This:**
- **Theming:** All color definitions
- **Layout:** Spacing and sizing
- **Validation:** Structure limits
- **File System:** Extensions and paths

---

## 5. Data Flow Relationships

### Creating a Guide:
```
GuideCreatorWizard → GuideMetadata → TroubleshootingGuide
                  ↓
                TroubleshootingNode → NodeAnswer
                  ↓
              FileController.save_guide()
```

### Executing a Guide:
```
ProductSelectorWidget → ProductCatalog → Product → ProblemCategory
                      ↓
              Guide Selection → FileController.load_guide()
                      ↓
              GuideExecutorView → TroubleshootingGuide
                      ↓
              Navigate: current_node → NodeAnswer → next_node_id
```

### Data Persistence:
```
TroubleshootingGuide.to_dict() → JSON → .tsg file
ProductCatalog.to_dict() → JSON → product_catalog.json

Loading reverses this with from_dict() methods
```

---

## 6. Feature-to-Data Mapping

| Feature | Primary Data Structures Used |
|---------|----------------------------|
| **Guide Creation** | GuideMetadata, TroubleshootingNode, NodeAnswer |
| **Guide Execution** | TroubleshootingGuide, path_history list |
| **Product Selection** | ProductCatalog, Product, ProblemCategory |
| **Save/Load** | All models' to_dict()/from_dict() methods |
| **Guide Library** | List[TroubleshootingGuide], QListWidget items |
| **Navigation** | node_id strings, parent/child relationships |
| **Validation** | Node.is_valid(), Guide.validate(), _has_cycles() |
| **Statistics** | Guide.get_statistics(), path analysis |
| **Export** | Guide + Metadata → HTML/Markdown/JSON |
| **Search** | (Future) Would use tags, title, description |

---

## 7. Data Integrity Rules

1. **Every Guide must have:**
   - Valid metadata
   - At least one node (root)
   - No circular references
   - All referenced node_ids must exist

2. **Every Node must have:**
   - Unique node_id
   - Non-empty question
   - At least 2 answers
   - Valid answer destinations

3. **Every Answer must have:**
   - Answer text
   - Either next_node_id OR is_solution=True
   - If solution, must have solution_text

4. **Product Catalog must have:**
   - Unique product_ids
   - Unique category_ids within products
   - Valid guide_id references

---

## 8. Memory Considerations

- **Guides are loaded entirely into memory** when opened
- **Path history grows linearly** with navigation depth
- **Product catalog is singleton** - one instance for app
- **QListWidget items** store references, not copies
- **Node dictionary** provides O(1) lookup by ID

---

This document provides a complete map of how data flows through Treebleshooter. Each structure serves a specific purpose and connects to others to create the full troubleshooting experience.
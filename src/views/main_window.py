"""
Module: main_window
Purpose: Main application window for Treebleshooter
Author: Allen (with Claude Code assistance)
Date Created: 2025-08-15
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMenuBar, QMenu, QAction,
    QToolBar, QStatusBar, QMessageBox, QStackedWidget,
    QListWidget, QListWidgetItem, QSplitter, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QKeySequence, QFont
import logging
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.constants import *
from src.models import TroubleshootingGuide, GuideMetadata
from src.views.guide_creator_wizard import GuideCreatorWizard
from src.views.guide_executor_view import GuideExecutorView

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window for Treebleshooter.
    
    Provides the primary interface for:
    - Creating new troubleshooting guides
    - Loading existing guides
    - Executing/running guides
    - Managing the guide library
    """
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self.current_guide: Optional[TroubleshootingGuide] = None
        self.guide_library: list[TroubleshootingGuide] = []
        
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_status_bar()
        self.apply_styles()
        
        # Show welcome screen
        self.show_welcome_screen()
        
        # Load example guides
        self.load_example_guides()
        
        logger.info("Main window initialized")
    
    def setup_ui(self):
        """Set up the main user interface."""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.setMinimumSize(MAIN_WINDOW_MIN_WIDTH, MAIN_WINDOW_MIN_HEIGHT)
        
        # Central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for sidebar and content
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left sidebar
        self.sidebar = self.create_sidebar()
        splitter.addWidget(self.sidebar)
        
        # Right content area (stacked widget for different views)
        self.content_stack = QStackedWidget()
        splitter.addWidget(self.content_stack)
        
        # Set initial splitter sizes (20% sidebar, 80% content)
        splitter.setSizes([240, 960])
        
        # Add different views to the stack
        self.welcome_widget = self.create_welcome_widget()
        self.content_stack.addWidget(self.welcome_widget)
        
        self.creator_wizard = GuideCreatorWizard()
        self.creator_wizard.guide_created.connect(self.on_guide_created)
        self.content_stack.addWidget(self.creator_wizard)
        
        self.executor_view = GuideExecutorView()
        self.content_stack.addWidget(self.executor_view)
    
    def create_sidebar(self) -> QWidget:
        """Create the sidebar with guide library."""
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar")
        layout = QVBoxLayout(sidebar_widget)
        layout.setContentsMargins(PADDING_SMALL, PADDING_SMALL, PADDING_SMALL, PADDING_SMALL)
        
        # Title
        title_label = QLabel("Guide Library")
        title_label.setObjectName("sidebar-title")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Guide list
        self.guide_list = QListWidget()
        self.guide_list.setObjectName("guide-list")
        self.guide_list.itemDoubleClicked.connect(self.on_guide_selected)
        layout.addWidget(self.guide_list)
        
        # Sidebar buttons
        button_layout = QVBoxLayout()
        
        self.new_guide_button = QPushButton("New Guide")
        self.new_guide_button.setObjectName("primary-button")
        self.new_guide_button.clicked.connect(self.create_new_guide)
        button_layout.addWidget(self.new_guide_button)
        
        self.load_guide_button = QPushButton("Load Guide")
        self.load_guide_button.clicked.connect(self.load_guide_from_file)
        button_layout.addWidget(self.load_guide_button)
        
        self.delete_guide_button = QPushButton("Delete Selected")
        self.delete_guide_button.setObjectName("danger-button")
        self.delete_guide_button.clicked.connect(self.delete_selected_guide)
        self.delete_guide_button.setEnabled(False)
        button_layout.addWidget(self.delete_guide_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        return sidebar_widget
    
    def create_welcome_widget(self) -> QWidget:
        """Create the welcome screen widget."""
        welcome_widget = QWidget()
        welcome_widget.setObjectName("welcome-screen")
        layout = QVBoxLayout(welcome_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(PADDING_LARGE)
        
        # Welcome title
        title_label = QLabel(f"Welcome to {APP_NAME}")
        title_label.setObjectName("welcome-title")
        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Create interactive troubleshooting guides with ease")
        subtitle_label.setObjectName("welcome-subtitle")
        subtitle_font = QFont()
        subtitle_font.setPointSize(16)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # Quick action buttons
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(PADDING_MEDIUM)
        
        create_button = QPushButton("Create New Guide")
        create_button.setObjectName("hero-button")
        create_button.setMinimumSize(200, 60)
        create_button.clicked.connect(self.create_new_guide)
        button_layout.addWidget(create_button)
        
        load_button = QPushButton("Load Existing Guide")
        load_button.setObjectName("hero-button-secondary")
        load_button.setMinimumSize(200, 60)
        load_button.clicked.connect(self.load_guide_from_file)
        button_layout.addWidget(load_button)
        
        layout.addWidget(button_container)
        
        # Help text
        help_text = QLabel(
            "Tip: Use File → Help to learn how to create your first troubleshooting guide"
        )
        help_text.setObjectName("help-text")
        help_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(help_text)
        
        return welcome_widget
    
    def setup_menu_bar(self):
        """Set up the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Guide", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.create_new_guide)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open Guide", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.load_guide_from_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Guide", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_current_guide)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_guide_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        edit_guide_action = QAction("Edit Current Guide", self)
        edit_guide_action.triggered.connect(self.edit_current_guide)
        edit_menu.addAction(edit_guide_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        welcome_action = QAction("Welcome Screen", self)
        welcome_action.triggered.connect(self.show_welcome_screen)
        view_menu.addAction(welcome_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        tutorial_action = QAction("Tutorial", self)
        tutorial_action.setShortcut(QKeySequence.HelpContents)
        tutorial_action.triggered.connect(self.show_tutorial)
        help_menu.addAction(tutorial_action)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_toolbar(self):
        """Set up the application toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.addToolBar(toolbar)
        
        new_action = toolbar.addAction("New")
        new_action.triggered.connect(self.create_new_guide)
        
        open_action = toolbar.addAction("Open")
        open_action.triggered.connect(self.load_guide_from_file)
        
        save_action = toolbar.addAction("Save")
        save_action.triggered.connect(self.save_current_guide)
        
        toolbar.addSeparator()
        
        run_action = toolbar.addAction("Run Guide")
        run_action.triggered.connect(self.run_current_guide)
        
        edit_action = toolbar.addAction("Edit Guide")
        edit_action.triggered.connect(self.edit_current_guide)
    
    def setup_status_bar(self):
        """Set up the application status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def apply_styles(self):
        """Apply custom styles to the application."""
        # This will be enhanced later with the style sheet
        pass
    
    def show_welcome_screen(self):
        """Show the welcome screen."""
        self.content_stack.setCurrentWidget(self.welcome_widget)
        self.status_bar.showMessage("Welcome to Treebleshooter")
    
    def create_new_guide(self):
        """Start creating a new troubleshooting guide."""
        self.content_stack.setCurrentWidget(self.creator_wizard)
        self.creator_wizard.start_new_guide()
        self.status_bar.showMessage("Creating new guide...")
    
    def load_guide_from_file(self):
        """Load a guide from a file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Troubleshooting Guide",
            DEFAULT_SAVE_DIRECTORY,
            GUIDE_FILE_FILTER
        )
        
        if file_path:
            self.status_bar.showMessage(f"Loading guide from {file_path}")
            logger.info(f"Loading guide from {file_path}")
            
            # Import the file controller
            from src.controllers import FileController
            file_controller = FileController()
            
            # Load the guide
            guide = file_controller.load_guide(file_path)
            
            if guide:
                # Set as current guide
                self.current_guide = guide
                
                # Add to library if not already there
                if guide not in self.guide_library:
                    self.guide_library.append(guide)
                    
                    # Add to sidebar list
                    item = QListWidgetItem(guide.metadata.title)
                    self.guide_list.addItem(item)
                
                # Run the guide
                self.run_current_guide()
                
                self.status_bar.showMessage(f"Loaded: {guide.metadata.title}")
                logger.info(f"Successfully loaded guide: {guide.metadata.title}")
            else:
                QMessageBox.warning(self, "Load Failed", "Failed to load the troubleshooting guide")
                self.status_bar.showMessage("Failed to load guide")
                logger.error(f"Failed to load guide from {file_path}")
    
    def save_current_guide(self):
        """Save the current guide."""
        if self.current_guide:
            from src.controllers import FileController
            file_controller = FileController()
            
            # Save the guide
            success = file_controller.save_guide(self.current_guide)
            
            if success:
                self.status_bar.showMessage(f"Saved: {self.current_guide.metadata.title}")
                logger.info(f"Guide saved: {self.current_guide.metadata.title}")
            else:
                QMessageBox.warning(self, "Save Failed", "Failed to save the guide")
                self.status_bar.showMessage("Failed to save guide")
        else:
            QMessageBox.warning(self, "No Guide", "No guide is currently open")
    
    def save_guide_as(self):
        """Save the current guide with a new name."""
        if self.current_guide:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Troubleshooting Guide",
                DEFAULT_SAVE_DIRECTORY,
                GUIDE_FILE_FILTER
            )
            
            if file_path:
                from src.controllers import FileController
                file_controller = FileController()
                
                # Save the guide to the specified path
                success = file_controller.save_guide(self.current_guide, file_path)
                
                if success:
                    self.status_bar.showMessage(f"Saved to: {file_path}")
                    logger.info(f"Guide saved to: {file_path}")
                else:
                    QMessageBox.warning(self, "Save Failed", "Failed to save the guide")
                    self.status_bar.showMessage("Failed to save guide")
        else:
            QMessageBox.warning(self, "No Guide", "No guide is currently open")
    
    def edit_current_guide(self):
        """Edit the current guide."""
        if self.current_guide:
            self.creator_wizard.edit_existing_guide(self.current_guide)
            self.content_stack.setCurrentWidget(self.creator_wizard)
            self.status_bar.showMessage("Editing guide...")
        else:
            QMessageBox.information(self, "No Guide", "Please create or load a guide first")
    
    def run_current_guide(self):
        """Run/execute the current guide."""
        if self.current_guide:
            self.executor_view.load_guide(self.current_guide)
            self.content_stack.setCurrentWidget(self.executor_view)
            self.status_bar.showMessage("Running guide...")
        else:
            QMessageBox.information(self, "No Guide", "Please create or load a guide first")
    
    def delete_selected_guide(self):
        """Delete the selected guide from the library."""
        current_item = self.guide_list.currentItem()
        if current_item:
            reply = QMessageBox.question(
                self,
                "Delete Guide",
                f"Are you sure you want to delete '{current_item.text()}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                row = self.guide_list.row(current_item)
                self.guide_list.takeItem(row)
                # Remove from library
                if row < len(self.guide_library):
                    del self.guide_library[row]
                self.status_bar.showMessage("Guide deleted")
    
    def on_guide_selected(self, item: QListWidgetItem):
        """Handle guide selection from the library."""
        row = self.guide_list.row(item)
        if row < len(self.guide_library):
            self.current_guide = self.guide_library[row]
            self.run_current_guide()
    
    def on_guide_created(self, guide: TroubleshootingGuide):
        """Handle when a new guide is created."""
        self.current_guide = guide
        self.guide_library.append(guide)
        
        # Add to library list
        item = QListWidgetItem(guide.metadata.title)
        self.guide_list.addItem(item)
        
        self.status_bar.showMessage(f"Guide '{guide.metadata.title}' created")
        logger.info(f"New guide created: {guide.metadata.title}")
        
        # Show the executor view
        self.run_current_guide()
    
    def show_tutorial(self):
        """Show the application tutorial."""
        QMessageBox.information(
            self,
            "Tutorial",
            "Welcome to Treebleshooter!\n\n"
            "1. Click 'New Guide' to create a troubleshooting guide\n"
            "2. Add questions and answers to build your decision tree\n"
            "3. Save your guide for later use\n"
            "4. Run guides to step through troubleshooting\n\n"
            "For more help, check the GETTING_STARTED.md file!"
        )
    
    def show_about(self):
        """Show the about dialog."""
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            f"Created by {APP_AUTHOR}\n\n"
            "A visual tool for creating interactive troubleshooting guides."
        )
    
    def load_example_guides(self):
        """Load all example guides into the library."""
        try:
            from src.controllers import FileController
            file_controller = FileController()
            
            # Get all example files
            example_files = file_controller.list_example_files()
            
            for file_path in example_files:
                guide = file_controller.load_guide(str(file_path))
                if guide:
                    self.guide_library.append(guide)
                    
                    # Add to sidebar list with example indicator
                    item = QListWidgetItem(f"📘 {guide.metadata.title}")
                    self.guide_list.addItem(item)
                    
            if example_files:
                self.status_bar.showMessage(f"Loaded {len(example_files)} example guides")
                logger.info(f"Loaded {len(example_files)} example guides")
                
                # Enable the delete button since we have items
                self.delete_guide_button.setEnabled(True)
                
        except Exception as e:
            logger.error(f"Error loading example guides: {e}")
"""
Module: guide_creator_wizard
Purpose: Wizard interface for creating troubleshooting guides
Author: Allen (with Claude Code assistance)
Date Created: 2025-08-15
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QLineEdit, QComboBox,
    QListWidget, QStackedWidget, QMessageBox,
    QGroupBox, QSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import logging

from src.models import TroubleshootingGuide, TroubleshootingNode, GuideMetadata
from src.utils.constants import *

logger = logging.getLogger(__name__)


class GuideCreatorWizard(QWidget):
    """
    Wizard for creating troubleshooting guides step by step.
    
    Provides an intuitive interface for building decision trees.
    """
    
    # Signal emitted when a guide is created
    guide_created = pyqtSignal(TroubleshootingGuide)
    
    def __init__(self):
        """Initialize the guide creator wizard."""
        super().__init__()
        self.current_guide: Optional[TroubleshootingGuide] = None
        self.current_node: Optional[TroubleshootingNode] = None
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Troubleshooting Guide Creator")
        title_label.setObjectName("wizard-title")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Instruction text
        self.instruction_label = QLabel(
            "Follow these steps to create your troubleshooting guide"
        )
        self.instruction_label.setWordWrap(True)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instruction_label)
        
        # Stacked widget for wizard pages
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        # Create wizard pages
        self.create_metadata_page()
        self.create_node_editor_page()
        self.create_review_page()
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.back_button = QPushButton("← Back")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)
        nav_layout.addWidget(self.back_button)
        
        nav_layout.addStretch()
        
        self.next_button = QPushButton("Next →")
        self.next_button.setObjectName("primary-button")
        self.next_button.clicked.connect(self.go_next)
        nav_layout.addWidget(self.next_button)
        
        self.finish_button = QPushButton("Finish")
        self.finish_button.setObjectName("success-button")
        self.finish_button.clicked.connect(self.finish_guide)
        self.finish_button.setVisible(False)
        nav_layout.addWidget(self.finish_button)
        
        layout.addLayout(nav_layout)
        
    def create_metadata_page(self):
        """Create the metadata input page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Guide metadata form
        form_group = QGroupBox("Guide Information")
        form_layout = QVBoxLayout(form_group)
        
        # Title
        form_layout.addWidget(QLabel("Guide Title:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("e.g., 'Computer Won't Start Troubleshooting'")
        form_layout.addWidget(self.title_input)
        
        # Description
        form_layout.addWidget(QLabel("Description:"))
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Describe what this guide helps troubleshoot...")
        self.description_input.setMaximumHeight(80)
        form_layout.addWidget(self.description_input)
        
        # Author
        form_layout.addWidget(QLabel("Author:"))
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Your name")
        form_layout.addWidget(self.author_input)
        
        # Difficulty
        form_layout.addWidget(QLabel("Difficulty Level:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Beginner", "Intermediate", "Advanced", "Expert"])
        form_layout.addWidget(self.difficulty_combo)
        
        # Estimated time
        form_layout.addWidget(QLabel("Estimated Time (minutes):"))
        self.time_input = QSpinBox()
        self.time_input.setMinimum(1)
        self.time_input.setMaximum(999)
        self.time_input.setValue(10)
        form_layout.addWidget(self.time_input)
        
        layout.addWidget(form_group)
        layout.addStretch()
        
        self.stack.addWidget(page)
        
    def create_node_editor_page(self):
        """Create the node editing page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        layout.addWidget(QLabel("Build Your Troubleshooting Tree"))
        
        # Placeholder for node editor
        # This would be a more complex widget in the full implementation
        placeholder = QLabel("Node editor will be implemented here\n\n"
                            "This will allow:\n"
                            "• Adding questions/steps\n"
                            "• Defining possible answers\n"
                            "• Linking answers to next steps or solutions\n"
                            "• Visual tree preview")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("border: 2px dashed #ccc; padding: 40px;")
        layout.addWidget(placeholder)
        
        self.stack.addWidget(page)
        
    def create_review_page(self):
        """Create the review and finish page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        layout.addWidget(QLabel("Review Your Guide"))
        
        # Summary display
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        layout.addWidget(self.summary_text)
        
        self.stack.addWidget(page)
        
    def start_new_guide(self):
        """Start creating a new guide."""
        self.current_guide = None
        self.stack.setCurrentIndex(0)
        self.back_button.setEnabled(False)
        self.next_button.setVisible(True)
        self.finish_button.setVisible(False)
        
        # Clear form
        self.title_input.clear()
        self.description_input.clear()
        self.author_input.clear()
        self.difficulty_combo.setCurrentIndex(0)
        self.time_input.setValue(10)
        
        logger.info("Started new guide creation")
        
    def edit_existing_guide(self, guide: TroubleshootingGuide):
        """Load an existing guide for editing."""
        self.current_guide = guide
        
        # Populate metadata
        self.title_input.setText(guide.metadata.title)
        self.description_input.setPlainText(guide.metadata.description)
        self.author_input.setText(guide.metadata.author)
        
        # Set difficulty
        index = self.difficulty_combo.findText(guide.metadata.difficulty_level)
        if index >= 0:
            self.difficulty_combo.setCurrentIndex(index)
        
        if guide.metadata.estimated_time_minutes:
            self.time_input.setValue(guide.metadata.estimated_time_minutes)
        
        self.stack.setCurrentIndex(0)
        logger.info(f"Editing guide: {guide.metadata.title}")
        
    def go_back(self):
        """Go to the previous wizard page."""
        current_index = self.stack.currentIndex()
        if current_index > 0:
            self.stack.setCurrentIndex(current_index - 1)
            
        # Update button states
        self.back_button.setEnabled(self.stack.currentIndex() > 0)
        
        if self.stack.currentIndex() < self.stack.count() - 1:
            self.next_button.setVisible(True)
            self.finish_button.setVisible(False)
            
    def go_next(self):
        """Go to the next wizard page."""
        current_index = self.stack.currentIndex()
        
        # Validate current page
        if current_index == 0:
            if not self.validate_metadata():
                return
            
            # Create guide if not editing
            if not self.current_guide:
                self.create_guide_from_metadata()
        
        if current_index < self.stack.count() - 1:
            self.stack.setCurrentIndex(current_index + 1)
            
        # Update button states
        self.back_button.setEnabled(True)
        
        if self.stack.currentIndex() == self.stack.count() - 1:
            # On last page
            self.next_button.setVisible(False)
            self.finish_button.setVisible(True)
            self.update_summary()
            
    def validate_metadata(self) -> bool:
        """Validate the metadata form."""
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Missing Information", "Please enter a guide title")
            return False
            
        if not self.description_input.toPlainText().strip():
            QMessageBox.warning(self, "Missing Information", "Please enter a description")
            return False
            
        return True
        
    def create_guide_from_metadata(self):
        """Create a guide from the metadata form."""
        metadata = GuideMetadata(
            title=self.title_input.text().strip(),
            description=self.description_input.toPlainText().strip(),
            author=self.author_input.text().strip() or "Unknown",
            difficulty_level=self.difficulty_combo.currentText(),
            estimated_time_minutes=self.time_input.value()
        )
        
        self.current_guide = TroubleshootingGuide(metadata)
        
        # Create a simple example root node
        root = TroubleshootingNode(
            question="Start of troubleshooting - What's the main issue?",
            description="This is the beginning of your troubleshooting guide"
        )
        root.add_answer(
            answer_text="Example answer 1",
            is_solution=True,
            solution_text="This is where you'd add the solution"
        )
        root.add_answer(
            answer_text="Example answer 2",
            is_solution=True,
            solution_text="Another solution would go here"
        )
        
        self.current_guide.add_node(root, is_root=True)
        
        logger.info(f"Created guide: {metadata.title}")
        
    def update_summary(self):
        """Update the summary display."""
        if self.current_guide:
            stats = self.current_guide.get_statistics()
            summary = f"""
Guide Title: {self.current_guide.metadata.title}
Description: {self.current_guide.metadata.description}
Author: {self.current_guide.metadata.author}
Difficulty: {self.current_guide.metadata.difficulty_level}
Estimated Time: {self.current_guide.metadata.estimated_time_minutes} minutes

Statistics:
- Total Nodes: {stats['total_nodes']}
- Total Paths: {stats['total_paths']}
- Total Solutions: {stats['total_solutions']}

Click 'Finish' to save and use your guide!
            """
            self.summary_text.setPlainText(summary)
            
    def finish_guide(self):
        """Finish creating/editing the guide."""
        if self.current_guide:
            # Validate the guide
            is_valid, errors = self.current_guide.validate()
            
            if not is_valid:
                error_msg = "Guide validation errors:\n" + "\n".join(errors)
                QMessageBox.warning(self, "Validation Errors", error_msg)
                return
                
            # Emit the signal
            self.guide_created.emit(self.current_guide)
            logger.info(f"Guide creation completed: {self.current_guide.metadata.title}")
            
            # Reset wizard
            self.start_new_guide()
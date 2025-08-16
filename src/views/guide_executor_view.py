"""
Module: guide_executor_view
Purpose: Interface for running/executing troubleshooting guides
Author: Allen (with Claude Code assistance)
Date Created: 2025-08-15
"""

from typing import Optional, List
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QButtonGroup,
    QTextEdit, QGroupBox, QProgressBar,
    QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import logging

from src.models import TroubleshootingGuide, TroubleshootingNode, NodeAnswer
from src.utils.constants import *

logger = logging.getLogger(__name__)


class GuideExecutorView(QWidget):
    """
    View for executing/running troubleshooting guides.
    
    Presents questions and guides users through the troubleshooting process.
    """
    
    # Signal emitted when guide execution is complete
    guide_completed = pyqtSignal(str)  # Emits solution text
    
    def __init__(self):
        """Initialize the guide executor view."""
        super().__init__()
        self.current_guide: Optional[TroubleshootingGuide] = None
        self.current_node: Optional[TroubleshootingNode] = None
        self.path_history: List[str] = []  # Track the path taken
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(PADDING_MEDIUM)
        
        # Guide title and progress
        header_layout = QVBoxLayout()
        
        self.title_label = QLabel("No Guide Loaded")
        self.title_label.setObjectName("executor-title")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.title_label)
        
        self.description_label = QLabel("")
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.description_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Step %v of %m")
        header_layout.addWidget(self.progress_bar)
        
        layout.addLayout(header_layout)
        
        # Main content area (scrollable)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        
        # Question display
        self.question_group = QGroupBox("Current Step")
        self.question_group.setObjectName("question-group")
        question_layout = QVBoxLayout(self.question_group)
        
        self.question_label = QLabel("Ready to start troubleshooting")
        self.question_label.setWordWrap(True)
        self.question_label.setObjectName("question-text")
        question_font = QFont()
        question_font.setPointSize(14)
        self.question_label.setFont(question_font)
        question_layout.addWidget(self.question_label)
        
        self.help_text_label = QLabel("")
        self.help_text_label.setWordWrap(True)
        self.help_text_label.setObjectName("help-text")
        question_layout.addWidget(self.help_text_label)
        
        self.content_layout.addWidget(self.question_group)
        
        # Answer options
        self.answers_group = QGroupBox("Select Your Answer")
        self.answers_group.setObjectName("answers-group")
        self.answers_layout = QVBoxLayout(self.answers_group)
        self.answers_group.setVisible(True)  # Ensure initially visible
        
        self.answer_button_group = QButtonGroup()
        
        self.content_layout.addWidget(self.answers_group)
        
        # Solution display (initially hidden)
        self.solution_group = QGroupBox("Solution")
        self.solution_group.setObjectName("solution-group")
        solution_layout = QVBoxLayout(self.solution_group)
        
        self.solution_text = QTextEdit()
        self.solution_text.setReadOnly(True)
        self.solution_text.setObjectName("solution-text")
        solution_layout.addWidget(self.solution_text)
        
        self.solution_group.setVisible(False)
        self.content_layout.addWidget(self.solution_group)
        
        self.content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.back_button = QPushButton("← Previous Step")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)
        nav_layout.addWidget(self.back_button)
        
        nav_layout.addStretch()
        
        self.next_button = QPushButton("Next Step →")
        self.next_button.setObjectName("primary-button")
        self.next_button.clicked.connect(self.go_next)
        self.next_button.setEnabled(False)
        nav_layout.addWidget(self.next_button)
        
        self.restart_button = QPushButton("Start Over")
        self.restart_button.clicked.connect(self.restart_guide)
        self.restart_button.setVisible(False)
        nav_layout.addWidget(self.restart_button)
        
        layout.addLayout(nav_layout)
        
    def load_guide(self, guide: TroubleshootingGuide):
        """
        Load a troubleshooting guide for execution.
        
        Args:
            guide: The guide to execute
        """
        self.current_guide = guide
        self.path_history = []
        
        # Update title and description
        self.title_label.setText(guide.metadata.title)
        self.description_label.setText(guide.metadata.description)
        
        # Set up progress bar
        stats = guide.get_statistics()
        self.progress_bar.setMaximum(int(stats.get('average_path_length', 5)))
        self.progress_bar.setValue(0)
        
        # Load the root node
        root_node = guide.get_root_node()
        if root_node:
            self.display_node(root_node)
            logger.info(f"Loaded guide: {guide.metadata.title}")
        else:
            logger.error(f"Guide has no root node: {guide.metadata.title}")
            self.question_label.setText("Error: This guide has no starting point")
            
    def display_node(self, node: TroubleshootingNode):
        """
        Display a node's question and answers.
        
        Args:
            node: The node to display
        """
        self.current_node = node
        
        # Update question
        self.question_label.setText(node.question)
        
        # Update help text
        if node.help_text:
            self.help_text_label.setText(f"ℹ️ {node.help_text}")
            self.help_text_label.setVisible(True)
        else:
            self.help_text_label.setVisible(False)
        
        # Clear previous answers
        while self.answers_layout.count():
            item = self.answers_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        
        # Clear button group
        for button in self.answer_button_group.buttons():
            self.answer_button_group.removeButton(button)
        
        # Hide solution and show answers group
        self.solution_group.setVisible(False)
        self.answers_group.setVisible(True)
        
        # Add answer options
        for i, answer in enumerate(node.answers):
            radio_button = QRadioButton(answer.answer_text)
            radio_button.setObjectName(f"answer-option-{i}")
            self.answer_button_group.addButton(radio_button, i)
            self.answers_layout.addWidget(radio_button)
        
        # Enable/disable navigation
        self.back_button.setEnabled(len(self.path_history) > 0)
        self.next_button.setEnabled(True)
        self.restart_button.setVisible(False)
        
        # Update progress
        self.progress_bar.setValue(len(self.path_history) + 1)
        
        logger.debug(f"Displaying node: {node.question[:50]}...")
        
    def go_next(self):
        """Process the selected answer and move to the next step."""
        selected_button = self.answer_button_group.checkedButton()
        
        if not selected_button:
            # No answer selected
            return
        
        # Get the selected answer
        answer_index = self.answer_button_group.id(selected_button)
        if self.current_node and 0 <= answer_index < len(self.current_node.answers):
            selected_answer = self.current_node.answers[answer_index]
            
            # Add current node to history
            self.path_history.append(self.current_node.node_id)
            
            if selected_answer.is_solution:
                # Display solution
                self.display_solution(selected_answer.solution_text or "Solution found!")
            elif selected_answer.next_node_id and self.current_guide:
                # Move to next node
                next_node = self.current_guide.get_node(selected_answer.next_node_id)
                if next_node:
                    self.display_node(next_node)
                else:
                    logger.error(f"Next node not found: {selected_answer.next_node_id}")
                    self.display_solution("Error: Next step not found")
            else:
                # Dead end
                self.display_solution("End of troubleshooting path reached")
                
    def go_back(self):
        """Go back to the previous step."""
        if self.path_history and self.current_guide:
            # Get the previous node
            previous_node_id = self.path_history.pop()
            previous_node = self.current_guide.get_node(previous_node_id)
            
            if previous_node:
                self.display_node(previous_node)
            else:
                logger.error(f"Previous node not found: {previous_node_id}")
                
    def display_solution(self, solution_text: str):
        """
        Display the solution.
        
        Args:
            solution_text: The solution to display
        """
        self.solution_text.setPlainText(solution_text)
        self.solution_group.setVisible(True)
        
        # Hide answer options
        self.answers_group.setVisible(False)
        
        # Update navigation
        self.next_button.setEnabled(False)
        self.restart_button.setVisible(True)
        
        # Update progress to maximum
        self.progress_bar.setValue(self.progress_bar.maximum())
        
        # Emit completion signal
        self.guide_completed.emit(solution_text)
        
        logger.info("Guide execution completed - solution displayed")
        
    def restart_guide(self):
        """Restart the current guide from the beginning."""
        if self.current_guide:
            self.load_guide(self.current_guide)
            logger.info("Guide restarted")
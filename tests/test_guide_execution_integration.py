"""
Integration tests for guide loading and execution functionality.
Tests the complete flow from loading a guide to walking through it multiple times.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QApplication, QRadioButton
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from src.models import TroubleshootingGuide, GuideMetadata
from src.views.guide_executor_view import GuideExecutorView
from src.controllers.file_controller import FileController
from src.utils.example_guides import ExampleGuideGenerator


class GuideExecutionIntegrationTest(unittest.TestCase):
    """Integration tests for guide execution."""
    
    @classmethod
    def setUpClass(cls):
        """Set up QApplication for all tests."""
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()
    
    def setUp(self):
        """Set up test environment."""
        self.executor = GuideExecutorView()
        self.executor.show()  # Show the widget for visibility tests
        self.test_data_path = Path("tests/test_data")
        self.test_data_path.mkdir(parents=True, exist_ok=True)
        
        # Create file controller
        self.file_controller = FileController(str(self.test_data_path))
        
        # Create and save example guides for testing
        guides = ExampleGuideGenerator.create_all_guides()
        for guide_id, guide in guides.items():
            filename = f"{guide_id}.tsg"
            filepath = self.test_data_path / filename
            self.file_controller.save_guide(guide, str(filepath))
        
    def tearDown(self):
        """Clean up after tests."""
        # Clean up test data
        import shutil
        if self.test_data_path.exists():
            shutil.rmtree(self.test_data_path)
    
    def test_guide_loads_correctly(self):
        """Test that a guide loads and displays initial node correctly."""
        # Load a test guide
        guide_path = self.test_data_path / "coffee-both-hot-and-cold.tsg"
        guide = self.file_controller.load_guide(str(guide_path))
        
        self.assertIsNotNone(guide, "Guide should load successfully")
        
        # Load guide into executor
        self.executor.load_guide(guide)
        
        # Process events to ensure UI updates
        QApplication.processEvents()
        
        # Verify UI state
        self.assertEqual(self.executor.title_label.text(), 
                        "Coffee Temperature Superposition")
        self.assertTrue(self.executor.answers_group.isVisible(),
                       "Answers group should be visible")
        
        # Check that radio buttons were created
        radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
        self.assertGreater(len(radio_buttons), 0, 
                          "Should have radio buttons for answers")
        
    def test_navigation_through_guide(self):
        """Test navigating through a guide by selecting answers."""
        # Load guide
        guide_path = self.test_data_path / "duck-offering-solutions.tsg"
        guide = self.file_controller.load_guide(str(guide_path))
        self.executor.load_guide(guide)
        
        # Get initial radio buttons
        radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
        initial_count = len(radio_buttons)
        self.assertGreater(initial_count, 0, "Should have initial answer options")
        
        # Select first answer and proceed
        radio_buttons[0].setChecked(True)
        self.executor.go_next()
        
        # Verify we moved to next node
        radio_buttons_after = self.executor.answers_group.findChildren(QRadioButton)
        self.assertGreater(len(radio_buttons_after), 0, 
                          "Should still have answer options after navigation")
        
        # Verify back button is enabled
        self.assertTrue(self.executor.back_button.isEnabled(),
                       "Back button should be enabled after navigation")
        
    def test_reaching_solution(self):
        """Test reaching a solution node."""
        # Create a simple guide with immediate solution
        simple_guide = self._create_simple_guide_with_solution()
        
        self.executor.load_guide(simple_guide)
        
        # Select answer that leads to solution
        radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
        radio_buttons[0].setChecked(True)
        self.executor.go_next()
        
        # Verify solution is displayed
        self.assertTrue(self.executor.solution_group.isVisible(),
                       "Solution should be visible")
        self.assertFalse(self.executor.answers_group.isVisible(),
                        "Answers should be hidden when solution shown")
        self.assertTrue(self.executor.restart_button.isVisible(),
                       "Restart button should be visible")
        
    def test_restart_guide_after_solution(self):
        """Test that restarting a guide after reaching solution works correctly."""
        # Load guide and reach solution
        simple_guide = self._create_simple_guide_with_solution()
        self.executor.load_guide(simple_guide)
        
        # Navigate to solution
        radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
        radio_buttons[0].setChecked(True)
        self.executor.go_next()
        
        # Verify solution state
        self.assertTrue(self.executor.solution_group.isVisible())
        self.assertFalse(self.executor.answers_group.isVisible())
        
        # Restart guide
        self.executor.restart_guide()
        
        # Verify guide restarted correctly
        self.assertFalse(self.executor.solution_group.isVisible(),
                        "Solution should be hidden after restart")
        self.assertTrue(self.executor.answers_group.isVisible(),
                       "Answers should be visible after restart")
        
        # Verify radio buttons are present
        radio_buttons_after_restart = self.executor.answers_group.findChildren(QRadioButton)
        self.assertGreater(len(radio_buttons_after_restart), 0,
                          "Should have radio buttons after restart")
        
    def test_multiple_guide_walkthroughs(self):
        """Test walking through a guide multiple times."""
        guide_path = self.test_data_path / "mirror-too-enthusiastic.tsg"
        guide = self.file_controller.load_guide(str(guide_path))
        
        # Walk through guide multiple times
        for walkthrough in range(3):
            self.executor.load_guide(guide)
            
            # Verify initial state
            self.assertTrue(self.executor.answers_group.isVisible(),
                           f"Answers visible on walkthrough {walkthrough + 1}")
            
            radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
            self.assertGreater(len(radio_buttons), 0,
                              f"Has radio buttons on walkthrough {walkthrough + 1}")
            
            # Navigate to solution
            radio_buttons[0].setChecked(True)
            self.executor.go_next()
            
            # For guides with multiple levels, continue if needed
            if self.executor.answers_group.isVisible():
                radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
                if radio_buttons:
                    radio_buttons[0].setChecked(True)
                    self.executor.go_next()
            
            # Verify we can reach solution or navigate
            self.assertTrue(
                self.executor.solution_group.isVisible() or 
                self.executor.answers_group.isVisible(),
                f"Either solution or answers visible on walkthrough {walkthrough + 1}"
            )
    
    def test_back_navigation(self):
        """Test navigating backwards through a guide."""
        guide_path = self.test_data_path / "coffee-both-hot-and-cold.tsg"
        guide = self.file_controller.load_guide(str(guide_path))
        self.executor.load_guide(guide)
        
        # Navigate forward twice
        initial_question = self.executor.question_label.text()
        
        radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
        radio_buttons[0].setChecked(True)
        self.executor.go_next()
        
        second_question = self.executor.question_label.text()
        self.assertNotEqual(initial_question, second_question,
                           "Should have different question after navigation")
        
        # Navigate back
        self.executor.go_back()
        
        # Verify we're back at initial node
        self.assertEqual(self.executor.question_label.text(), initial_question,
                        "Should be back at initial question")
        self.assertTrue(self.executor.answers_group.isVisible(),
                       "Answers should be visible after going back")
        
        radio_buttons_after_back = self.executor.answers_group.findChildren(QRadioButton)
        self.assertGreater(len(radio_buttons_after_back), 0,
                          "Should have radio buttons after going back")
    
    def test_all_example_guides_load(self):
        """Test that all example guides load without errors."""
        guide_files = list(self.test_data_path.glob("*.tsg"))
        self.assertGreater(len(guide_files), 0, "Should have example guides")
        
        for guide_file in guide_files:
            with self.subTest(guide=guide_file.name):
                guide = self.file_controller.load_guide(str(guide_file))
                self.assertIsNotNone(guide, f"Guide {guide_file.name} should load")
                
                # Load and verify initial state
                self.executor.load_guide(guide)
                self.assertTrue(self.executor.answers_group.isVisible(),
                               f"Answers visible for {guide_file.name}")
                
                radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
                self.assertGreater(len(radio_buttons), 0,
                                  f"Has radio buttons for {guide_file.name}")
    
    def test_deep_guide_navigation(self):
        """Test navigating through a deep (4+ level) guide."""
        # Load a deep guide
        guide_path = self.test_data_path / "duck-offering-solutions.tsg"
        guide = self.file_controller.load_guide(str(guide_path))
        self.executor.load_guide(guide)
        
        # Navigate through multiple levels
        levels_navigated = 0
        max_levels = 6  # Try to navigate through at least 6 levels
        
        while levels_navigated < max_levels:
            if not self.executor.answers_group.isVisible():
                # Reached a solution
                break
                
            radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
            if not radio_buttons:
                break
                
            # Select first available answer
            radio_buttons[0].setChecked(True)
            self.executor.go_next()
            levels_navigated += 1
            
            # Verify UI state after each navigation
            self.assertTrue(
                self.executor.solution_group.isVisible() or 
                self.executor.answers_group.isVisible(),
                f"Should show solution or answers at level {levels_navigated}"
            )
        
        self.assertGreater(levels_navigated, 3,
                          "Should be able to navigate through at least 4 levels")
    
    def test_guide_completion_signal(self):
        """Test that guide completion signal is emitted correctly."""
        signal_received = False
        solution_text = None
        
        def on_guide_completed(text):
            nonlocal signal_received, solution_text
            signal_received = True
            solution_text = text
        
        self.executor.guide_completed.connect(on_guide_completed)
        
        # Load simple guide and complete it
        simple_guide = self._create_simple_guide_with_solution()
        self.executor.load_guide(simple_guide)
        
        radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
        radio_buttons[0].setChecked(True)
        self.executor.go_next()
        
        # Verify signal was emitted
        self.assertTrue(signal_received, "Completion signal should be emitted")
        self.assertIsNotNone(solution_text, "Solution text should be provided")
        self.assertIn("Test solution", solution_text)
    
    def _create_simple_guide_with_solution(self):
        """Create a simple guide for testing."""
        guide_data = {
            "metadata": {
                "title": "Test Guide",
                "description": "A simple test guide",
                "author": "Test",
                "version": "1.0.0",
                "created_date": "2024-01-01",
                "last_modified_date": "2024-01-01",
                "tags": ["test"],
                "difficulty_level": "Easy",
                "estimated_time_minutes": 1
            },
            "root_node_id": "root",
            "nodes": {
                "root": {
                    "node_id": "root",
                    "question": "Test question?",
                    "description": "Test description",
                    "help_text": "Test help",
                    "parent_node_id": None,
                    "answers": [
                        {
                            "answer_id": "a1",
                            "answer_text": "Solution answer",
                            "next_node_id": None,
                            "is_solution": True,
                            "solution_text": "Test solution text"
                        },
                        {
                            "answer_id": "a2",
                            "answer_text": "Another answer",
                            "next_node_id": "node2",
                            "is_solution": False,
                            "solution_text": None
                        }
                    ]
                },
                "node2": {
                    "node_id": "node2",
                    "question": "Second question?",
                    "description": None,
                    "help_text": None,
                    "parent_node_id": "root",
                    "answers": [
                        {
                            "answer_id": "a3",
                            "answer_text": "Final answer",
                            "next_node_id": None,
                            "is_solution": True,
                            "solution_text": "Another solution"
                        }
                    ]
                }
            }
        }
        
        return TroubleshootingGuide.from_dict(guide_data)


if __name__ == "__main__":
    unittest.main()
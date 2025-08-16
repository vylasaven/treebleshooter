#!/usr/bin/env python3
"""
Edge case tests for guide execution
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PyQt5.QtWidgets import QApplication, QRadioButton
from src.views.guide_executor_view import GuideExecutorView
from src.models import TroubleshootingGuide
import unittest


class EdgeCaseTests(unittest.TestCase):
    """Test edge cases in guide execution."""
    
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
        self.executor.show()
    
    def test_empty_guide(self):
        """Test loading a guide with no nodes."""
        empty_guide_data = {
            "metadata": {
                "title": "Empty Guide",
                "description": "A guide with no nodes",
                "author": "Test",
                "version": "1.0.0",
                "created_date": "2024-01-01",
                "last_modified_date": "2024-01-01",
                "tags": [],
                "difficulty_level": "Easy",
                "estimated_time_minutes": 0
            },
            "root_node_id": None,
            "nodes": {}
        }
        
        guide = TroubleshootingGuide.from_dict(empty_guide_data)
        self.executor.load_guide(guide)
        
        # Should handle gracefully
        self.assertEqual(self.executor.question_label.text(), 
                        "Error: This guide has no starting point")
    
    def test_guide_with_no_answers(self):
        """Test a node with no answer options."""
        guide_data = {
            "metadata": {
                "title": "No Answers Guide",
                "description": "A guide with a node that has no answers",
                "author": "Test",
                "version": "1.0.0",
                "created_date": "2024-01-01",
                "last_modified_date": "2024-01-01",
                "tags": [],
                "difficulty_level": "Easy",
                "estimated_time_minutes": 1
            },
            "root_node_id": "root",
            "nodes": {
                "root": {
                    "node_id": "root",
                    "question": "This question has no answers",
                    "description": None,
                    "help_text": None,
                    "parent_node_id": None,
                    "answers": []
                }
            }
        }
        
        guide = TroubleshootingGuide.from_dict(guide_data)
        self.executor.load_guide(guide)
        
        # Should display the question but no radio buttons
        self.assertEqual(self.executor.question_label.text(), 
                        "This question has no answers")
        radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
        self.assertEqual(len(radio_buttons), 0)
    
    def test_rapid_guide_switching(self):
        """Test rapidly switching between guides."""
        guide1_data = self._create_simple_guide("Guide 1", "Question 1")
        guide2_data = self._create_simple_guide("Guide 2", "Question 2")
        
        guide1 = TroubleshootingGuide.from_dict(guide1_data)
        guide2 = TroubleshootingGuide.from_dict(guide2_data)
        
        # Rapidly switch between guides
        for _ in range(5):
            self.executor.load_guide(guide1)
            QApplication.processEvents()
            self.executor.load_guide(guide2)
            QApplication.processEvents()
        
        # Should end up with guide2 loaded
        self.assertEqual(self.executor.title_label.text(), "Guide 2")
        self.assertEqual(self.executor.question_label.text(), "Question 2")
        
        # Should have exactly 2 radio buttons (from guide2)
        radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
        self.assertEqual(len(radio_buttons), 2)
    
    def test_very_long_text(self):
        """Test handling of very long question and answer text."""
        long_text = "A" * 1000  # 1000 character string
        guide_data = {
            "metadata": {
                "title": "Long Text Guide",
                "description": "Testing long text handling",
                "author": "Test",
                "version": "1.0.0",
                "created_date": "2024-01-01",
                "last_modified_date": "2024-01-01",
                "tags": [],
                "difficulty_level": "Easy",
                "estimated_time_minutes": 1
            },
            "root_node_id": "root",
            "nodes": {
                "root": {
                    "node_id": "root",
                    "question": long_text,
                    "description": None,
                    "help_text": long_text,
                    "parent_node_id": None,
                    "answers": [
                        {
                            "answer_id": "a1",
                            "answer_text": long_text,
                            "next_node_id": None,
                            "is_solution": True,
                            "solution_text": long_text
                        }
                    ]
                }
            }
        }
        
        guide = TroubleshootingGuide.from_dict(guide_data)
        self.executor.load_guide(guide)
        
        # Should handle long text without crashing
        self.assertTrue(self.executor.answers_group.isVisible())
        radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
        self.assertEqual(len(radio_buttons), 1)
    
    def test_circular_navigation(self):
        """Test guide with circular references."""
        guide_data = {
            "metadata": {
                "title": "Circular Guide",
                "description": "Testing circular navigation",
                "author": "Test",
                "version": "1.0.0",
                "created_date": "2024-01-01",
                "last_modified_date": "2024-01-01",
                "tags": [],
                "difficulty_level": "Easy",
                "estimated_time_minutes": 1
            },
            "root_node_id": "node1",
            "nodes": {
                "node1": {
                    "node_id": "node1",
                    "question": "Question 1",
                    "description": None,
                    "help_text": None,
                    "parent_node_id": None,
                    "answers": [
                        {
                            "answer_id": "a1",
                            "answer_text": "Go to question 2",
                            "next_node_id": "node2",
                            "is_solution": False,
                            "solution_text": None
                        }
                    ]
                },
                "node2": {
                    "node_id": "node2",
                    "question": "Question 2",
                    "description": None,
                    "help_text": None,
                    "parent_node_id": "node1",
                    "answers": [
                        {
                            "answer_id": "a2",
                            "answer_text": "Go back to question 1",
                            "next_node_id": "node1",
                            "is_solution": False,
                            "solution_text": None
                        }
                    ]
                }
            }
        }
        
        guide = TroubleshootingGuide.from_dict(guide_data)
        self.executor.load_guide(guide)
        
        # Navigate in circle multiple times
        for _ in range(10):
            radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
            if radio_buttons:
                radio_buttons[0].setChecked(True)
                self.executor.go_next()
                QApplication.processEvents()
        
        # Should still have exactly 1 radio button visible
        radio_buttons = self.executor.answers_group.findChildren(QRadioButton)
        self.assertEqual(len(radio_buttons), 1)
    
    def _create_simple_guide(self, title, question):
        """Helper to create a simple guide for testing."""
        return {
            "metadata": {
                "title": title,
                "description": f"Description for {title}",
                "author": "Test",
                "version": "1.0.0",
                "created_date": "2024-01-01",
                "last_modified_date": "2024-01-01",
                "tags": [],
                "difficulty_level": "Easy",
                "estimated_time_minutes": 1
            },
            "root_node_id": "root",
            "nodes": {
                "root": {
                    "node_id": "root",
                    "question": question,
                    "description": None,
                    "help_text": None,
                    "parent_node_id": None,
                    "answers": [
                        {
                            "answer_id": "a1",
                            "answer_text": "Answer 1",
                            "next_node_id": None,
                            "is_solution": True,
                            "solution_text": "Solution"
                        },
                        {
                            "answer_id": "a2",
                            "answer_text": "Answer 2",
                            "next_node_id": None,
                            "is_solution": True,
                            "solution_text": "Solution"
                        }
                    ]
                }
            }
        }


if __name__ == "__main__":
    unittest.main()
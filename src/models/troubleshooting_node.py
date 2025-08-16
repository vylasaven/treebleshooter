"""
Module: troubleshooting_node
Purpose: Defines the basic node structure for troubleshooting decision trees
Author: Allen (with Claude Code assistance)
Date Created: 2025-08-15
"""

from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field
import uuid
import logging

logger = logging.getLogger(__name__)


@dataclass
class NodeAnswer:
    """
    Represents a possible answer/choice at a troubleshooting node.
    
    Each answer leads to either another node or a final solution.
    """
    
    answer_text: str                    # The text displayed for this answer
    next_node_id: Optional[str] = None  # ID of the next node (None if this is a solution)
    is_solution: bool = False            # True if this answer ends the troubleshooting
    solution_text: Optional[str] = None  # Final solution text if this is an endpoint
    answer_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert answer to dictionary for JSON serialization."""
        return {
            'answer_id': self.answer_id,
            'answer_text': self.answer_text,
            'next_node_id': self.next_node_id,
            'is_solution': self.is_solution,
            'solution_text': self.solution_text
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NodeAnswer':
        """Create answer from dictionary."""
        return cls(
            answer_id=data.get('answer_id', str(uuid.uuid4())),
            answer_text=data['answer_text'],
            next_node_id=data.get('next_node_id'),
            is_solution=data.get('is_solution', False),
            solution_text=data.get('solution_text')
        )


class TroubleshootingNode:
    """
    Represents a single decision point in a troubleshooting guide.
    
    Each node contains:
    - A question or diagnostic step
    - Multiple possible answers
    - References to child nodes or solutions
    """
    
    def __init__(self, 
                 question: str,
                 node_id: Optional[str] = None,
                 description: Optional[str] = None,
                 help_text: Optional[str] = None):
        """
        Initialize a troubleshooting node.
        
        Args:
            question: The main question or instruction for this step
            node_id: Unique identifier (auto-generated if not provided)
            description: Extended description of this step
            help_text: Additional help information for users
        """
        self.node_id = node_id or str(uuid.uuid4())
        self.question = question
        self.description = description
        self.help_text = help_text
        self.answers: List[NodeAnswer] = []
        self.parent_node_id: Optional[str] = None
        
        logger.debug(f"Created node '{self.question}' with ID: {self.node_id}")
    
    def add_answer(self, 
                   answer_text: str,
                   next_node_id: Optional[str] = None,
                   is_solution: bool = False,
                   solution_text: Optional[str] = None) -> NodeAnswer:
        """
        Add a possible answer to this node.
        
        Args:
            answer_text: The text of the answer option
            next_node_id: ID of the next node if not a solution
            is_solution: True if this answer ends the troubleshooting
            solution_text: The solution text if this is an endpoint
            
        Returns:
            The created NodeAnswer object
        """
        answer = NodeAnswer(
            answer_text=answer_text,
            next_node_id=next_node_id,
            is_solution=is_solution,
            solution_text=solution_text
        )
        self.answers.append(answer)
        logger.debug(f"Added answer '{answer_text}' to node {self.node_id}")
        return answer
    
    def remove_answer(self, answer_id: str) -> bool:
        """
        Remove an answer from this node.
        
        Args:
            answer_id: ID of the answer to remove
            
        Returns:
            True if answer was found and removed, False otherwise
        """
        initial_count = len(self.answers)
        self.answers = [a for a in self.answers if a.answer_id != answer_id]
        removed = len(self.answers) < initial_count
        
        if removed:
            logger.debug(f"Removed answer {answer_id} from node {self.node_id}")
        else:
            logger.warning(f"Answer {answer_id} not found in node {self.node_id}")
            
        return removed
    
    def get_answer_by_id(self, answer_id: str) -> Optional[NodeAnswer]:
        """Find an answer by its ID."""
        for answer in self.answers:
            if answer.answer_id == answer_id:
                return answer
        return None
    
    def is_leaf_node(self) -> bool:
        """Check if this node has no child nodes (all answers are solutions)."""
        return all(answer.is_solution for answer in self.answers)
    
    def is_valid(self) -> Tuple[bool, str]:
        """
        Validate the node structure.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.question:
            return False, "Node must have a question"
        
        if len(self.answers) < 2:
            return False, "Node must have at least 2 answers"
        
        for answer in self.answers:
            if not answer.answer_text:
                return False, "All answers must have text"
            
            if answer.is_solution and not answer.solution_text:
                return False, "Solution answers must have solution text"
            
            if not answer.is_solution and not answer.next_node_id:
                return False, "Non-solution answers must link to next node"
        
        return True, ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary for JSON serialization."""
        return {
            'node_id': self.node_id,
            'question': self.question,
            'description': self.description,
            'help_text': self.help_text,
            'parent_node_id': self.parent_node_id,
            'answers': [answer.to_dict() for answer in self.answers]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TroubleshootingNode':
        """Create node from dictionary."""
        node = cls(
            question=data['question'],
            node_id=data.get('node_id'),
            description=data.get('description'),
            help_text=data.get('help_text')
        )
        node.parent_node_id = data.get('parent_node_id')
        
        for answer_data in data.get('answers', []):
            answer = NodeAnswer.from_dict(answer_data)
            node.answers.append(answer)
        
        return node
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"TroubleshootingNode(id={self.node_id}, question='{self.question[:30]}...', answers={len(self.answers)})"
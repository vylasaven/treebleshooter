"""
Module: troubleshooting_guide
Purpose: Container for complete troubleshooting guide with nodes and metadata
Author: Allen (with Claude Code assistance)
Date Created: 2025-08-15
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from .troubleshooting_node import TroubleshootingNode
from .guide_metadata import GuideMetadata
import logging

logger = logging.getLogger(__name__)


class TroubleshootingGuide:
    """
    Complete troubleshooting guide containing nodes and metadata.
    
    This is the main container that holds:
    - All nodes in the troubleshooting tree
    - Metadata about the guide
    - Methods for traversing and modifying the tree
    """
    
    def __init__(self, metadata: GuideMetadata):
        """
        Initialize a troubleshooting guide.
        
        Args:
            metadata: Guide metadata (title, author, etc.)
        """
        self.metadata = metadata
        self.nodes: Dict[str, TroubleshootingNode] = {}  # node_id -> node
        self.root_node_id: Optional[str] = None
        
        logger.info(f"Created guide: '{metadata.title}'")
    
    def add_node(self, node: TroubleshootingNode, is_root: bool = False) -> None:
        """
        Add a node to the guide.
        
        Args:
            node: The node to add
            is_root: Set this node as the root/starting node
        """
        self.nodes[node.node_id] = node
        
        if is_root or self.root_node_id is None:
            self.root_node_id = node.node_id
            logger.info(f"Set root node to: {node.node_id}")
        
        self.metadata.update_modified_date()
        logger.debug(f"Added node {node.node_id} to guide")
    
    def remove_node(self, node_id: str) -> bool:
        """
        Remove a node and all references to it.
        
        Args:
            node_id: ID of the node to remove
            
        Returns:
            True if node was removed, False if not found
        """
        if node_id not in self.nodes:
            logger.warning(f"Node {node_id} not found in guide")
            return False
        
        # Don't allow removing the root node
        if node_id == self.root_node_id:
            logger.error("Cannot remove root node")
            return False
        
        # Remove the node
        del self.nodes[node_id]
        
        # Remove all references to this node from other nodes
        for node in self.nodes.values():
            for answer in node.answers:
                if answer.next_node_id == node_id:
                    answer.next_node_id = None
                    answer.is_solution = True
                    answer.solution_text = "Path removed - please update this solution"
        
        self.metadata.update_modified_date()
        logger.info(f"Removed node {node_id} from guide")
        return True
    
    def get_node(self, node_id: str) -> Optional[TroubleshootingNode]:
        """Get a node by its ID."""
        return self.nodes.get(node_id)
    
    def get_root_node(self) -> Optional[TroubleshootingNode]:
        """Get the root/starting node of the guide."""
        if self.root_node_id:
            return self.nodes.get(self.root_node_id)
        return None
    
    def get_child_nodes(self, node_id: str) -> List[TroubleshootingNode]:
        """Get all direct child nodes of a given node."""
        node = self.get_node(node_id)
        if not node:
            return []
        
        child_nodes = []
        for answer in node.answers:
            if answer.next_node_id and not answer.is_solution:
                child_node = self.get_node(answer.next_node_id)
                if child_node:
                    child_nodes.append(child_node)
        
        return child_nodes
    
    def get_all_paths(self) -> List[List[str]]:
        """
        Get all possible paths through the guide.
        
        Returns:
            List of paths, where each path is a list of node IDs
        """
        if not self.root_node_id:
            return []
        
        paths = []
        
        def traverse(node_id: str, current_path: List[str]) -> None:
            """Recursive helper to find all paths."""
            # Check for cycles - if we've already visited this node in this path, stop
            if node_id in current_path:
                # Cycle detected - treat as endpoint
                paths.append(current_path.copy())
                return
            
            node = self.get_node(node_id)
            if not node:
                return
            
            current_path.append(node_id)
            
            # Check if this is an endpoint
            has_endpoint = False
            for answer in node.answers:
                if answer.is_solution:
                    # This path ends here
                    paths.append(current_path.copy())
                    has_endpoint = True
                elif answer.next_node_id:
                    # Continue traversing
                    traverse(answer.next_node_id, current_path.copy())
            
            # If no endpoints or continuations, this is also a path end
            if not has_endpoint and not any(a.next_node_id for a in node.answers):
                paths.append(current_path)
        
        traverse(self.root_node_id, [])
        return paths
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the guide.
        
        Returns:
            Dictionary with guide statistics
        """
        all_paths = self.get_all_paths()
        path_lengths = [len(path) for path in all_paths] if all_paths else [0]
        
        total_solutions = sum(
            1 for node in self.nodes.values()
            for answer in node.answers
            if answer.is_solution
        )
        
        return {
            'total_nodes': len(self.nodes),
            'total_paths': len(all_paths),
            'shortest_path': min(path_lengths),
            'longest_path': max(path_lengths),
            'average_path_length': sum(path_lengths) / len(path_lengths) if path_lengths else 0,
            'total_solutions': total_solutions
        }
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate the entire guide structure.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check if we have a root node
        if not self.root_node_id:
            errors.append("Guide has no root node")
        elif self.root_node_id not in self.nodes:
            errors.append(f"Root node {self.root_node_id} not found in nodes")
        
        # Check each node
        for node_id, node in self.nodes.items():
            is_valid, error = node.is_valid()
            if not is_valid:
                errors.append(f"Node {node_id}: {error}")
            
            # Check that all referenced nodes exist
            for answer in node.answers:
                if answer.next_node_id and answer.next_node_id not in self.nodes:
                    errors.append(f"Node {node_id} references non-existent node {answer.next_node_id}")
        
        # Check for orphaned nodes (not reachable from root)
        if self.root_node_id:
            reachable_nodes = self._get_reachable_nodes()
            orphaned = set(self.nodes.keys()) - reachable_nodes
            for orphan_id in orphaned:
                errors.append(f"Node {orphan_id} is not reachable from root")
        
        # Check for cycles
        if self._has_cycles():
            errors.append("Guide contains circular references (cycles)")
        
        return len(errors) == 0, errors
    
    def _get_reachable_nodes(self) -> Set[str]:
        """Get all nodes reachable from the root."""
        if not self.root_node_id:
            return set()
        
        visited = set()
        to_visit = [self.root_node_id]
        
        while to_visit:
            node_id = to_visit.pop()
            if node_id in visited:
                continue
            
            visited.add(node_id)
            node = self.get_node(node_id)
            
            if node:
                for answer in node.answers:
                    if answer.next_node_id and not answer.is_solution:
                        to_visit.append(answer.next_node_id)
        
        return visited
    
    def _has_cycles(self) -> bool:
        """Check if the guide has any circular references."""
        if not self.root_node_id:
            return False
        
        def has_cycle_from(node_id: str, visited: Set[str], rec_stack: Set[str]) -> bool:
            """DFS helper to detect cycles."""
            visited.add(node_id)
            rec_stack.add(node_id)
            
            node = self.get_node(node_id)
            if node:
                for answer in node.answers:
                    if answer.next_node_id and not answer.is_solution:
                        if answer.next_node_id not in visited:
                            if has_cycle_from(answer.next_node_id, visited, rec_stack):
                                return True
                        elif answer.next_node_id in rec_stack:
                            return True
            
            rec_stack.remove(node_id)
            return False
        
        visited = set()
        rec_stack = set()
        
        for node_id in self.nodes:
            if node_id not in visited:
                if has_cycle_from(node_id, visited, rec_stack):
                    return True
        
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert guide to dictionary for JSON serialization."""
        return {
            'metadata': self.metadata.to_dict(),
            'root_node_id': self.root_node_id,
            'nodes': {
                node_id: node.to_dict()
                for node_id, node in self.nodes.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TroubleshootingGuide':
        """Create guide from dictionary."""
        metadata = GuideMetadata.from_dict(data['metadata'])
        guide = cls(metadata)
        guide.root_node_id = data.get('root_node_id')
        
        # Create all nodes
        for node_id, node_data in data.get('nodes', {}).items():
            node = TroubleshootingNode.from_dict(node_data)
            guide.nodes[node_id] = node
        
        return guide
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        stats = self.get_statistics()
        return f"TroubleshootingGuide(title='{self.metadata.title}', nodes={stats['total_nodes']}, paths={stats['total_paths']})"
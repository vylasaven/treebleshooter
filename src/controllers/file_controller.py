"""
Module: file_controller
Purpose: Handle saving and loading of troubleshooting guides
Author: Allen (with Claude Code assistance)
Date Created: 2025-08-15
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from src.models import TroubleshootingGuide, ProductCatalog
from src.utils.constants import GUIDE_FILE_EXTENSION

logger = logging.getLogger(__name__)


class FileController:
    """
    Manages file operations for troubleshooting guides and catalogs.
    
    Handles:
    - Saving guides to JSON files
    - Loading guides from JSON files
    - Managing the product catalog
    - Auto-save functionality
    """
    
    def __init__(self, data_directory: str = "data"):
        """
        Initialize the file controller.
        
        Args:
            data_directory: Directory for storing guide files
        """
        self.data_dir = Path(data_directory)
        self.data_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.guides_dir = self.data_dir / "guides"
        self.guides_dir.mkdir(exist_ok=True)
        
        self.examples_dir = self.data_dir / "examples"
        self.examples_dir.mkdir(exist_ok=True)
        
        self.catalog_file = self.data_dir / "product_catalog.json"
        
        logger.info(f"File controller initialized with data directory: {self.data_dir}")
    
    def save_guide(self, guide: TroubleshootingGuide, filepath: Optional[str] = None) -> bool:
        """
        Save a troubleshooting guide to a file.
        
        Args:
            guide: The guide to save
            filepath: Optional specific filepath, otherwise auto-generated
            
        Returns:
            True if save was successful
        """
        try:
            # Generate filepath if not provided
            if not filepath:
                # Create filename from title
                safe_title = "".join(
                    c for c in guide.metadata.title 
                    if c.isalnum() or c in (' ', '-', '_')
                ).rstrip()
                safe_title = safe_title.replace(' ', '_')
                
                filename = f"{safe_title}{GUIDE_FILE_EXTENSION}"
                filepath = self.guides_dir / filename
            else:
                filepath = Path(filepath)
            
            # Ensure parent directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert guide to dictionary
            guide_data = guide.to_dict()
            
            # Add metadata
            guide_data['_metadata'] = {
                'file_version': '1.0',
                'saved_date': datetime.now().isoformat(),
                'application': 'Treebleshooter'
            }
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(guide_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Guide saved successfully: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving guide: {e}")
            return False
    
    def load_guide(self, filepath: str) -> Optional[TroubleshootingGuide]:
        """
        Load a troubleshooting guide from a file.
        
        Args:
            filepath: Path to the guide file
            
        Returns:
            The loaded guide or None if loading failed
        """
        try:
            filepath = Path(filepath)
            
            if not filepath.exists():
                logger.error(f"Guide file not found: {filepath}")
                return None
            
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                guide_data = json.load(f)
            
            # Remove file metadata if present
            guide_data.pop('_metadata', None)
            
            # Create guide from data
            guide = TroubleshootingGuide.from_dict(guide_data)
            
            logger.info(f"Guide loaded successfully: {filepath}")
            return guide
            
        except Exception as e:
            logger.error(f"Error loading guide: {e}")
            return None
    
    def save_catalog(self, catalog: ProductCatalog) -> bool:
        """
        Save the product catalog.
        
        Args:
            catalog: The catalog to save
            
        Returns:
            True if save was successful
        """
        try:
            catalog_data = catalog.to_dict()
            
            # Add metadata
            catalog_data['_metadata'] = {
                'file_version': '1.0',
                'saved_date': datetime.now().isoformat(),
                'application': 'Treebleshooter'
            }
            
            # Write to file
            with open(self.catalog_file, 'w', encoding='utf-8') as f:
                json.dump(catalog_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Catalog saved successfully: {self.catalog_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving catalog: {e}")
            return False
    
    def load_catalog(self) -> Optional[ProductCatalog]:
        """
        Load the product catalog.
        
        Returns:
            The loaded catalog or None if loading failed
        """
        try:
            if not self.catalog_file.exists():
                logger.info("No catalog file found, creating default catalog")
                return ProductCatalog.create_default_catalog()
            
            # Read file
            with open(self.catalog_file, 'r', encoding='utf-8') as f:
                catalog_data = json.load(f)
            
            # Remove file metadata if present
            catalog_data.pop('_metadata', None)
            
            # Create catalog from data
            catalog = ProductCatalog.from_dict(catalog_data)
            
            logger.info(f"Catalog loaded successfully: {self.catalog_file}")
            return catalog
            
        except Exception as e:
            logger.error(f"Error loading catalog: {e}")
            # Return default catalog on error
            return ProductCatalog.create_default_catalog()
    
    def list_guide_files(self) -> List[Path]:
        """
        List all guide files in the guides directory.
        
        Returns:
            List of guide file paths
        """
        guide_files = []
        
        # Check guides directory
        for file in self.guides_dir.glob(f"*{GUIDE_FILE_EXTENSION}"):
            guide_files.append(file)
        
        # Also check for JSON files
        for file in self.guides_dir.glob("*.json"):
            guide_files.append(file)
        
        logger.debug(f"Found {len(guide_files)} guide files")
        return sorted(guide_files)
    
    def list_example_files(self) -> List[Path]:
        """
        List all example guide files.
        
        Returns:
            List of example file paths
        """
        example_files = []
        
        for file in self.examples_dir.glob(f"*{GUIDE_FILE_EXTENSION}"):
            example_files.append(file)
        
        for file in self.examples_dir.glob("*.json"):
            example_files.append(file)
        
        logger.debug(f"Found {len(example_files)} example files")
        return sorted(example_files)
    
    def export_guide_to_format(self, guide: TroubleshootingGuide, 
                              format: str, filepath: str) -> bool:
        """
        Export a guide to different formats.
        
        Args:
            guide: The guide to export
            format: Export format ('json', 'html', 'markdown')
            filepath: Output filepath
            
        Returns:
            True if export was successful
        """
        try:
            filepath = Path(filepath)
            
            if format == 'json':
                # Standard JSON export
                return self.save_guide(guide, str(filepath))
            
            elif format == 'markdown':
                # Export as markdown
                md_content = self._guide_to_markdown(guide)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                logger.info(f"Guide exported to markdown: {filepath}")
                return True
            
            elif format == 'html':
                # Export as HTML
                html_content = self._guide_to_html(guide)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                logger.info(f"Guide exported to HTML: {filepath}")
                return True
            
            else:
                logger.error(f"Unsupported export format: {format}")
                return False
                
        except Exception as e:
            logger.error(f"Error exporting guide: {e}")
            return False
    
    def _guide_to_markdown(self, guide: TroubleshootingGuide) -> str:
        """Convert guide to markdown format."""
        md = f"# {guide.metadata.title}\n\n"
        md += f"{guide.metadata.description}\n\n"
        md += f"**Author:** {guide.metadata.author}  \n"
        md += f"**Difficulty:** {guide.metadata.difficulty_level}  \n"
        md += f"**Estimated Time:** {guide.metadata.estimated_time_minutes} minutes\n\n"
        
        md += "## Troubleshooting Steps\n\n"
        
        # Simple representation of the tree
        root = guide.get_root_node()
        if root:
            md += self._node_to_markdown(guide, root, 1)
        
        return md
    
    def _node_to_markdown(self, guide: TroubleshootingGuide, 
                          node, level: int) -> str:
        """Convert a node to markdown."""
        md = f"{'#' * (level + 1)} {node.question}\n\n"
        
        if node.help_text:
            md += f"_{node.help_text}_\n\n"
        
        for answer in node.answers:
            md += f"- **{answer.answer_text}**"
            if answer.is_solution:
                md += f" → _Solution: {answer.solution_text}_\n"
            elif answer.next_node_id:
                next_node = guide.get_node(answer.next_node_id)
                if next_node and level < 5:  # Limit depth
                    md += "\n"
                    md += self._node_to_markdown(guide, next_node, level + 1)
            md += "\n"
        
        return md
    
    def _guide_to_html(self, guide: TroubleshootingGuide) -> str:
        """Convert guide to HTML format."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{guide.metadata.title}</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; }}
        .metadata {{ background: #ecf0f1; padding: 10px; border-radius: 5px; }}
        .question {{ background: #3498db; color: white; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        .answer {{ margin-left: 20px; padding: 5px; }}
        .solution {{ background: #2ecc71; color: white; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>{guide.metadata.title}</h1>
    <div class="metadata">
        <p>{guide.metadata.description}</p>
        <p><strong>Author:</strong> {guide.metadata.author}</p>
        <p><strong>Difficulty:</strong> {guide.metadata.difficulty_level}</p>
        <p><strong>Estimated Time:</strong> {guide.metadata.estimated_time_minutes} minutes</p>
    </div>
    <h2>Troubleshooting Steps</h2>
"""
        
        root = guide.get_root_node()
        if root:
            html += self._node_to_html(guide, root, set())
        
        html += "</body></html>"
        return html
    
    def _node_to_html(self, guide: TroubleshootingGuide, 
                      node, visited: set) -> str:
        """Convert a node to HTML."""
        if node.node_id in visited:
            return ""  # Avoid infinite loops
        
        visited.add(node.node_id)
        
        html = f'<div class="question">{node.question}</div>\n'
        
        if node.help_text:
            html += f'<p style="font-style: italic;">{node.help_text}</p>\n'
        
        for answer in node.answers:
            html += f'<div class="answer">• {answer.answer_text}'
            if answer.is_solution:
                html += f'<div class="solution">Solution: {answer.solution_text}</div>'
            elif answer.next_node_id:
                next_node = guide.get_node(answer.next_node_id)
                if next_node:
                    html += self._node_to_html(guide, next_node, visited)
            html += '</div>\n'
        
        return html
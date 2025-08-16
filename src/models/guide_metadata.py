"""
Module: guide_metadata  
Purpose: Metadata for troubleshooting guides (author, version, etc.)
Author: Allen (with Claude Code assistance)
Date Created: 2025-08-15
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class GuideMetadata:
    """
    Metadata for a troubleshooting guide.
    
    Contains information about the guide itself, not the troubleshooting content.
    """
    
    title: str                                          # Guide title
    description: str                                     # What this guide helps troubleshoot
    author: str = "Unknown"                            # Who created this guide
    version: str = "1.0.0"                             # Version number
    created_date: datetime = field(default_factory=datetime.now)
    last_modified_date: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)      # Categories/tags for organization
    difficulty_level: str = "Beginner"                  # Beginner/Intermediate/Advanced
    estimated_time_minutes: Optional[int] = None        # Estimated completion time
    
    def update_modified_date(self) -> None:
        """Update the last modified date to now."""
        self.last_modified_date = datetime.now()
        logger.debug(f"Updated modified date for guide '{self.title}'")
    
    def add_tag(self, tag: str) -> None:
        """Add a tag if it doesn't already exist."""
        if tag not in self.tags:
            self.tags.append(tag)
            logger.debug(f"Added tag '{tag}' to guide '{self.title}'")
    
    def remove_tag(self, tag: str) -> bool:
        """
        Remove a tag from the guide.
        
        Returns:
            True if tag was removed, False if not found
        """
        if tag in self.tags:
            self.tags.remove(tag)
            logger.debug(f"Removed tag '{tag}' from guide '{self.title}'")
            return True
        return False
    
    def increment_version(self, major: bool = False, minor: bool = False) -> None:
        """
        Increment the version number.
        
        Args:
            major: Increment major version (X.0.0)
            minor: Increment minor version (1.X.0)
            Otherwise increments patch (1.0.X)
        """
        parts = self.version.split('.')
        if len(parts) != 3:
            logger.warning(f"Invalid version format: {self.version}")
            self.version = "1.0.0"
            return
        
        try:
            major_num = int(parts[0])
            minor_num = int(parts[1])
            patch_num = int(parts[2])
            
            if major:
                major_num += 1
                minor_num = 0
                patch_num = 0
            elif minor:
                minor_num += 1
                patch_num = 0
            else:
                patch_num += 1
            
            self.version = f"{major_num}.{minor_num}.{patch_num}"
            self.update_modified_date()
            logger.info(f"Updated guide '{self.title}' to version {self.version}")
            
        except ValueError:
            logger.error(f"Could not parse version numbers from: {self.version}")
            self.version = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for JSON serialization."""
        return {
            'title': self.title,
            'description': self.description,
            'author': self.author,
            'version': self.version,
            'created_date': self.created_date.isoformat(),
            'last_modified_date': self.last_modified_date.isoformat(),
            'tags': self.tags,
            'difficulty_level': self.difficulty_level,
            'estimated_time_minutes': self.estimated_time_minutes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GuideMetadata':
        """Create metadata from dictionary."""
        return cls(
            title=data['title'],
            description=data['description'],
            author=data.get('author', 'Unknown'),
            version=data.get('version', '1.0.0'),
            created_date=datetime.fromisoformat(data.get('created_date', datetime.now().isoformat())),
            last_modified_date=datetime.fromisoformat(data.get('last_modified_date', datetime.now().isoformat())),
            tags=data.get('tags', []),
            difficulty_level=data.get('difficulty_level', 'Beginner'),
            estimated_time_minutes=data.get('estimated_time_minutes')
        )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"GuideMetadata(title='{self.title}', version={self.version}, author='{self.author}')"
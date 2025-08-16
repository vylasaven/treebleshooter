#!/usr/bin/env python3
"""
Script to create and save example troubleshooting guides
Run this to populate the data/examples folder with .tsg files
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.example_guides import ExampleGuideGenerator
from src.controllers.file_controller import FileController
from src.models import ProductCatalog
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Create and save all example guides."""
    print("Creating example troubleshooting guides...")
    
    # Initialize file controller
    file_controller = FileController()
    
    # Create all example guides
    guides = ExampleGuideGenerator.create_all_guides()
    
    # Save each guide
    for guide_id, guide in guides.items():
        filename = f"{guide_id}.tsg"
        filepath = file_controller.examples_dir / filename
        
        success = file_controller.save_guide(guide, str(filepath))
        if success:
            print(f"✅ Created: {filename}")
        else:
            print(f"❌ Failed to create: {filename}")
    
    # Also create and save the default product catalog
    print("\nCreating product catalog...")
    catalog = ProductCatalog.create_default_catalog()
    success = file_controller.save_catalog(catalog)
    if success:
        print("✅ Created: product_catalog.json")
    else:
        print("❌ Failed to create product catalog")
    
    print(f"\n✨ Done! Created {len(guides)} example guides")
    print(f"📁 Location: {file_controller.examples_dir}")


if __name__ == "__main__":
    main()
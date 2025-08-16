"""
Module: product_catalog
Purpose: Product and problem category management for organizing guides
Author: Allen (with Claude Code assistance)
Date Created: 2025-08-15
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ProblemCategory:
    """
    Represents a category of problems for a specific product.
    
    Each category contains multiple troubleshooting guides.
    """
    
    category_id: str
    category_name: str
    description: str
    icon_name: Optional[str] = None  # For future icon support
    guide_ids: List[str] = field(default_factory=list)
    
    def add_guide(self, guide_id: str) -> None:
        """Add a guide to this category."""
        if guide_id not in self.guide_ids:
            self.guide_ids.append(guide_id)
            logger.debug(f"Added guide {guide_id} to category {self.category_name}")
    
    def remove_guide(self, guide_id: str) -> bool:
        """Remove a guide from this category."""
        if guide_id in self.guide_ids:
            self.guide_ids.remove(guide_id)
            logger.debug(f"Removed guide {guide_id} from category {self.category_name}")
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'description': self.description,
            'icon_name': self.icon_name,
            'guide_ids': self.guide_ids
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProblemCategory':
        """Create from dictionary."""
        return cls(
            category_id=data['category_id'],
            category_name=data['category_name'],
            description=data['description'],
            icon_name=data.get('icon_name'),
            guide_ids=data.get('guide_ids', [])
        )


@dataclass
class Product:
    """
    Represents a product that can have troubleshooting guides.
    
    Each product has multiple problem categories.
    """
    
    product_id: str
    product_name: str
    description: str
    manufacturer: str = "Generic Corp"
    version: str = "1.0"
    icon_name: Optional[str] = None
    problem_categories: Dict[str, ProblemCategory] = field(default_factory=dict)
    
    def add_category(self, category: ProblemCategory) -> None:
        """Add a problem category to this product."""
        self.problem_categories[category.category_id] = category
        logger.debug(f"Added category {category.category_name} to product {self.product_name}")
    
    def remove_category(self, category_id: str) -> bool:
        """Remove a problem category."""
        if category_id in self.problem_categories:
            del self.problem_categories[category_id]
            logger.debug(f"Removed category {category_id} from product {self.product_name}")
            return True
        return False
    
    def get_category(self, category_id: str) -> Optional[ProblemCategory]:
        """Get a category by ID."""
        return self.problem_categories.get(category_id)
    
    def get_all_guide_ids(self) -> List[str]:
        """Get all guide IDs across all categories."""
        guide_ids = []
        for category in self.problem_categories.values():
            guide_ids.extend(category.guide_ids)
        return guide_ids
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'description': self.description,
            'manufacturer': self.manufacturer,
            'version': self.version,
            'icon_name': self.icon_name,
            'problem_categories': {
                cat_id: cat.to_dict()
                for cat_id, cat in self.problem_categories.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create from dictionary."""
        product = cls(
            product_id=data['product_id'],
            product_name=data['product_name'],
            description=data['description'],
            manufacturer=data.get('manufacturer', 'Generic Corp'),
            version=data.get('version', '1.0'),
            icon_name=data.get('icon_name')
        )
        
        for cat_id, cat_data in data.get('problem_categories', {}).items():
            category = ProblemCategory.from_dict(cat_data)
            product.problem_categories[cat_id] = category
        
        return product


class ProductCatalog:
    """
    Manages all products and their associated problem categories and guides.
    
    This is the top-level container for organizing troubleshooting content.
    """
    
    def __init__(self):
        """Initialize the product catalog."""
        self.products: Dict[str, Product] = {}
        self.last_updated = datetime.now()
        logger.info("Product catalog initialized")
    
    def add_product(self, product: Product) -> None:
        """Add a product to the catalog."""
        self.products[product.product_id] = product
        self.last_updated = datetime.now()
        logger.info(f"Added product {product.product_name} to catalog")
    
    def remove_product(self, product_id: str) -> bool:
        """Remove a product from the catalog."""
        if product_id in self.products:
            del self.products[product_id]
            self.last_updated = datetime.now()
            logger.info(f"Removed product {product_id} from catalog")
            return True
        return False
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """Get a product by ID."""
        return self.products.get(product_id)
    
    def get_product_by_name(self, name: str) -> Optional[Product]:
        """Get a product by name (case-insensitive)."""
        for product in self.products.values():
            if product.product_name.lower() == name.lower():
                return product
        return None
    
    def find_guide_location(self, guide_id: str) -> Optional[Tuple[str, str]]:
        """
        Find which product and category a guide belongs to.
        
        Returns:
            Tuple of (product_id, category_id) or None if not found
        """
        for product_id, product in self.products.items():
            for category_id, category in product.problem_categories.items():
                if guide_id in category.guide_ids:
                    return (product_id, category_id)
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get catalog statistics."""
        total_categories = sum(
            len(product.problem_categories)
            for product in self.products.values()
        )
        
        total_guides = sum(
            len(product.get_all_guide_ids())
            for product in self.products.values()
        )
        
        return {
            'total_products': len(self.products),
            'total_categories': total_categories,
            'total_guides': total_guides,
            'last_updated': self.last_updated.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'products': {
                prod_id: prod.to_dict()
                for prod_id, prod in self.products.items()
            },
            'last_updated': self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductCatalog':
        """Create from dictionary."""
        catalog = cls()
        catalog.last_updated = datetime.fromisoformat(
            data.get('last_updated', datetime.now().isoformat())
        )
        
        for prod_id, prod_data in data.get('products', {}).items():
            product = Product.from_dict(prod_data)
            catalog.products[prod_id] = product
        
        return catalog
    
    @classmethod
    def create_default_catalog(cls) -> 'ProductCatalog':
        """
        Create a default catalog with whimsical example products.
        
        This provides Allen with fun examples to work with.
        """
        catalog = cls()
        
        # Product 1: Smart Toaster 3000
        toaster = Product(
            product_id="smart-toaster-3000",
            product_name="Smart Toaster 3000",
            description="The AI-powered toaster that knows you better than you know yourself",
            manufacturer="ToastTech Industries",
            version="3.0.1"
        )
        
        # Toaster problem categories
        toast_problems = ProblemCategory(
            category_id="toast-problems",
            category_name="Toast Malfunctions",
            description="When your toast isn't toasting quite right"
        )
        toast_problems.add_guide("toast-too-dark")
        toast_problems.add_guide("toast-too-light")
        toast_problems.add_guide("toast-uneven")
        
        ai_problems = ProblemCategory(
            category_id="ai-problems",
            category_name="AI Personality Issues",
            description="When your toaster gets too smart for its own good"
        )
        ai_problems.add_guide("toaster-too-sarcastic")
        ai_problems.add_guide("toaster-existential-crisis")
        
        connectivity = ProblemCategory(
            category_id="connectivity",
            category_name="WiFi & Bluetooth Woes",
            description="Connection problems in the modern toast era"
        )
        connectivity.add_guide("toaster-wont-connect")
        connectivity.add_guide("toaster-posting-on-social-media")
        
        toaster.add_category(toast_problems)
        toaster.add_category(ai_problems)
        toaster.add_category(connectivity)
        catalog.add_product(toaster)
        
        # Product 2: Procrastination Station Pro
        procrastinator = Product(
            product_id="procrastination-station",
            product_name="Procrastination Station Pro",
            description="The ultimate productivity tool that helps you avoid being productive",
            manufacturer="Tomorrow Corp",
            version="2.0.never"
        )
        
        # Procrastination categories
        too_productive = ProblemCategory(
            category_id="too-productive",
            category_name="Accidental Productivity",
            description="Emergency troubleshooting for when you accidentally get work done"
        )
        too_productive.add_guide("accidentally-finished-task")
        too_productive.add_guide("inbox-zero-panic")
        
        distraction_fail = ProblemCategory(
            category_id="distraction-failures",
            category_name="Distraction Failures",
            description="When your procrastination tools aren't procrastinating properly"
        )
        distraction_fail.add_guide("youtube-recommendations-too-educational")
        distraction_fail.add_guide("social-media-not-loading")
        
        procrastinator.add_category(too_productive)
        procrastinator.add_category(distraction_fail)
        catalog.add_product(procrastinator)
        
        # Product 3: Quantum Coffee Maker
        coffee_maker = Product(
            product_id="quantum-coffee",
            product_name="Quantum Coffee Maker",
            description="Brews coffee in multiple dimensions simultaneously",
            manufacturer="Schrödinger's Café",
            version="4.2.0"
        )
        
        quantum_issues = ProblemCategory(
            category_id="quantum-issues",
            category_name="Quantum Anomalies",
            description="When your coffee exists in too many states at once"
        )
        quantum_issues.add_guide("coffee-both-hot-and-cold")
        quantum_issues.add_guide("coffee-exists-doesnt-exist")
        
        temporal_problems = ProblemCategory(
            category_id="temporal-problems",
            category_name="Time-Related Issues",
            description="Coffee arriving before or after you need it"
        )
        temporal_problems.add_guide("coffee-from-yesterday")
        temporal_problems.add_guide("coffee-from-tomorrow")
        
        coffee_maker.add_category(quantum_issues)
        coffee_maker.add_category(temporal_problems)
        catalog.add_product(coffee_maker)
        
        # Product 4: Motivational Mirror
        mirror = Product(
            product_id="motivational-mirror",
            product_name="Motivational Mirror™",
            description="The smart mirror that compliments you (sometimes too much)",
            manufacturer="Self-Esteem Systems",
            version="1.3.7"
        )
        
        compliment_issues = ProblemCategory(
            category_id="compliment-issues",
            category_name="Compliment Calibration",
            description="When the encouragement level needs adjustment"
        )
        compliment_issues.add_guide("mirror-too-honest")
        compliment_issues.add_guide("mirror-too-enthusiastic")
        
        reflection_problems = ProblemCategory(
            category_id="reflection-problems",
            category_name="Reflection Issues",
            description="Technical problems with showing your reflection"
        )
        reflection_problems.add_guide("reflection-too-attractive")
        reflection_problems.add_guide("reflection-someone-else")
        
        mirror.add_category(compliment_issues)
        mirror.add_category(reflection_problems)
        catalog.add_product(mirror)
        
        # Product 5: Rubber Duck Debugger
        duck = Product(
            product_id="rubber-duck",
            product_name="Rubber Duck Debugger",
            description="The classic programmer's companion, now with AI",
            manufacturer="Quack Technologies",
            version="1.0.1"
        )
        
        listening_problems = ProblemCategory(
            category_id="listening-problems",
            category_name="Active Listening Issues",
            description="When your duck isn't being supportive enough"
        )
        listening_problems.add_guide("duck-falling-asleep")
        listening_problems.add_guide("duck-offering-solutions")
        
        duck.add_category(listening_problems)
        catalog.add_product(duck)
        
        logger.info("Created default product catalog with whimsical examples")
        return catalog
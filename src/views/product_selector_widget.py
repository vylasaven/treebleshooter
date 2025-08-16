"""
Module: product_selector_widget
Purpose: Widget for selecting products and problem categories
Author: Allen (with Claude Code assistance)
Date Created: 2025-08-15
"""

from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QGroupBox, QListWidget,
    QListWidgetItem, QTextEdit, QSplitter
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import logging

from src.models import ProductCatalog, Product, ProblemCategory
from src.utils.constants import *

logger = logging.getLogger(__name__)


class ProductSelectorWidget(QWidget):
    """
    Widget for selecting products and problem categories.
    
    Provides a hierarchical selection interface:
    Product -> Problem Category -> Troubleshooting Guides
    """
    
    # Signals
    guide_selected = pyqtSignal(str)  # Emits guide_id
    create_new_guide = pyqtSignal(str, str)  # Emits (product_id, category_id)
    
    def __init__(self, catalog: ProductCatalog):
        """
        Initialize the product selector.
        
        Args:
            catalog: The product catalog to display
        """
        super().__init__()
        self.catalog = catalog
        self.current_product: Optional[Product] = None
        self.current_category: Optional[ProblemCategory] = None
        
        self.setup_ui()
        self.load_products()
        
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(PADDING_MEDIUM)
        
        # Title
        title_label = QLabel("Select Product & Problem")
        title_label.setObjectName("section-title")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Instruction text
        instruction_label = QLabel(
            "Choose a product, then select a problem category to see available troubleshooting guides"
        )
        instruction_label.setWordWrap(True)
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setObjectName("instruction-text")
        layout.addWidget(instruction_label)
        
        # Product selection
        product_group = QGroupBox("1. Select Product")
        product_group.setObjectName("selection-group")
        product_layout = QVBoxLayout(product_group)
        
        self.product_combo = QComboBox()
        self.product_combo.setObjectName("product-selector")
        self.product_combo.currentTextChanged.connect(self.on_product_changed)
        product_layout.addWidget(self.product_combo)
        
        self.product_description = QTextEdit()
        self.product_description.setObjectName("description-text")
        self.product_description.setReadOnly(True)
        self.product_description.setMaximumHeight(60)
        product_layout.addWidget(self.product_description)
        
        layout.addWidget(product_group)
        
        # Problem category selection
        category_group = QGroupBox("2. Select Problem Category")
        category_group.setObjectName("selection-group")
        category_layout = QVBoxLayout(category_group)
        
        self.category_combo = QComboBox()
        self.category_combo.setObjectName("category-selector")
        self.category_combo.setEnabled(False)
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        category_layout.addWidget(self.category_combo)
        
        self.category_description = QTextEdit()
        self.category_description.setObjectName("description-text")
        self.category_description.setReadOnly(True)
        self.category_description.setMaximumHeight(60)
        category_layout.addWidget(self.category_description)
        
        layout.addWidget(category_group)
        
        # Available guides
        guides_group = QGroupBox("3. Available Troubleshooting Guides")
        guides_group.setObjectName("selection-group")
        guides_layout = QVBoxLayout(guides_group)
        
        self.guides_list = QListWidget()
        self.guides_list.setObjectName("guides-list")
        self.guides_list.setEnabled(False)
        self.guides_list.itemDoubleClicked.connect(self.on_guide_double_clicked)
        guides_layout.addWidget(self.guides_list)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(PADDING_SMALL)
        
        self.run_guide_button = QPushButton("Run Selected Guide")
        self.run_guide_button.setObjectName("primary-button")
        self.run_guide_button.setEnabled(False)
        self.run_guide_button.clicked.connect(self.run_selected_guide)
        button_layout.addWidget(self.run_guide_button)
        
        self.create_guide_button = QPushButton("Create New Guide")
        self.create_guide_button.setObjectName("secondary-button")
        self.create_guide_button.setEnabled(False)
        self.create_guide_button.clicked.connect(self.create_new_guide_clicked)
        button_layout.addWidget(self.create_guide_button)
        
        guides_layout.addLayout(button_layout)
        layout.addWidget(guides_group)
        
        # Statistics label
        self.stats_label = QLabel()
        self.stats_label.setObjectName("stats-label")
        self.stats_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stats_label)
        
        layout.addStretch()
        
        self.update_statistics()
    
    def load_products(self):
        """Load products into the combo box."""
        self.product_combo.clear()
        self.product_combo.addItem("-- Select a Product --")
        
        for product_id, product in sorted(
            self.catalog.products.items(),
            key=lambda x: x[1].product_name
        ):
            self.product_combo.addItem(product.product_name, product_id)
        
        logger.info(f"Loaded {len(self.catalog.products)} products")
    
    def on_product_changed(self, product_name: str):
        """Handle product selection change."""
        if product_name == "-- Select a Product --":
            self.current_product = None
            self.product_description.clear()
            self.category_combo.clear()
            self.category_combo.setEnabled(False)
            self.guides_list.clear()
            self.guides_list.setEnabled(False)
            self.create_guide_button.setEnabled(False)
            return
        
        # Get the selected product
        product_id = self.product_combo.currentData()
        if product_id:
            self.current_product = self.catalog.get_product(product_id)
            if self.current_product:
                # Update product description
                self.product_description.setPlainText(
                    f"{self.current_product.description}\n"
                    f"Manufacturer: {self.current_product.manufacturer} | "
                    f"Version: {self.current_product.version}"
                )
                
                # Load categories
                self.load_categories()
                
                logger.debug(f"Selected product: {product_name}")
    
    def load_categories(self):
        """Load problem categories for the selected product."""
        self.category_combo.clear()
        self.category_combo.setEnabled(True)
        self.category_combo.addItem("-- Select a Problem Category --")
        
        if self.current_product:
            for category_id, category in sorted(
                self.current_product.problem_categories.items(),
                key=lambda x: x[1].category_name
            ):
                self.category_combo.addItem(category.category_name, category_id)
            
            logger.debug(f"Loaded {len(self.current_product.problem_categories)} categories")
    
    def on_category_changed(self, category_name: str):
        """Handle category selection change."""
        if category_name == "-- Select a Problem Category --":
            self.current_category = None
            self.category_description.clear()
            self.guides_list.clear()
            self.guides_list.setEnabled(False)
            self.create_guide_button.setEnabled(False)
            return
        
        # Get the selected category
        category_id = self.category_combo.currentData()
        if category_id and self.current_product:
            self.current_category = self.current_product.get_category(category_id)
            if self.current_category:
                # Update category description
                self.category_description.setPlainText(self.current_category.description)
                
                # Load guides
                self.load_guides()
                
                # Enable create button
                self.create_guide_button.setEnabled(True)
                
                logger.debug(f"Selected category: {category_name}")
    
    def load_guides(self):
        """Load guides for the selected category."""
        self.guides_list.clear()
        self.guides_list.setEnabled(True)
        
        if self.current_category:
            if self.current_category.guide_ids:
                for guide_id in self.current_category.guide_ids:
                    # In a real implementation, we'd load guide metadata here
                    # For now, just display the guide ID in a friendly format
                    display_name = guide_id.replace("-", " ").title()
                    item = QListWidgetItem(display_name)
                    item.setData(Qt.UserRole, guide_id)
                    self.guides_list.addItem(item)
                
                self.run_guide_button.setEnabled(True)
                logger.debug(f"Loaded {len(self.current_category.guide_ids)} guides")
            else:
                item = QListWidgetItem("No guides available - Create one!")
                item.setEnabled(False)
                self.guides_list.addItem(item)
                self.run_guide_button.setEnabled(False)
    
    def on_guide_double_clicked(self, item: QListWidgetItem):
        """Handle double-click on a guide."""
        guide_id = item.data(Qt.UserRole)
        if guide_id:
            self.guide_selected.emit(guide_id)
            logger.info(f"Guide selected: {guide_id}")
    
    def run_selected_guide(self):
        """Run the selected guide."""
        current_item = self.guides_list.currentItem()
        if current_item:
            guide_id = current_item.data(Qt.UserRole)
            if guide_id:
                self.guide_selected.emit(guide_id)
                logger.info(f"Running guide: {guide_id}")
    
    def create_new_guide_clicked(self):
        """Handle create new guide button click."""
        if self.current_product and self.current_category:
            self.create_new_guide.emit(
                self.current_product.product_id,
                self.current_category.category_id
            )
            logger.info(
                f"Creating new guide for {self.current_product.product_name} "
                f"- {self.current_category.category_name}"
            )
    
    def update_statistics(self):
        """Update the statistics display."""
        stats = self.catalog.get_statistics()
        self.stats_label.setText(
            f"📊 {stats['total_products']} Products | "
            f"{stats['total_categories']} Categories | "
            f"{stats['total_guides']} Guides"
        )
    
    def refresh(self):
        """Refresh the entire widget."""
        self.load_products()
        self.update_statistics()
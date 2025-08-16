#!/usr/bin/env python3
"""
Treebleshooter - Interactive Troubleshooting Guide Creator
Main application entry point

Author: Allen (with Claude Code assistance)
Date Created: 2025-08-15
"""

import sys
import os
import logging
import signal
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont, QLinearGradient

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.views.main_window import MainWindow
from src.utils.constants import APP_NAME, APP_VERSION


def setup_logging():
    """Set up application logging."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app.log"),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")


def create_splash_screen(app: QApplication) -> QSplashScreen:
    """Create a fun splash screen."""
    # Create a pixmap for the splash screen
    from PyQt5.QtGui import QPainter, QBrush, QColor
    from PyQt5.QtCore import QRect
    
    pixmap = QPixmap(600, 400)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    
    # Draw gradient background - modern tech colors
    gradient = QLinearGradient(0, 0, 600, 400)
    gradient.setColorAt(0, QColor("#0A0E27"))
    gradient.setColorAt(0.5, QColor("#1A1F3A"))
    gradient.setColorAt(1, QColor("#00D4FF"))
    painter.fillRect(0, 0, 600, 400, gradient)
    
    # Set text color
    painter.setPen(QColor("white"))
    
    # Draw title
    title_font = QFont()
    title_font.setPointSize(36)
    title_font.setBold(True)
    painter.setFont(title_font)
    painter.drawText(QRect(0, 50, 600, 60), Qt.AlignCenter, f"🔧 {APP_NAME} 🔧")
    
    # Draw version
    version_font = QFont()
    version_font.setPointSize(18)
    painter.setFont(version_font)
    painter.drawText(QRect(0, 130, 600, 40), Qt.AlignCenter, f"Version {APP_VERSION}")
    
    # Draw tagline
    tagline_font = QFont()
    tagline_font.setPointSize(14)
    painter.setFont(tagline_font)
    painter.drawText(QRect(0, 200, 600, 60), Qt.AlignCenter, 
                    "Creating troubleshooting guides\none decision tree at a time!")
    
    # Draw loading message
    painter.drawText(QRect(0, 320, 600, 30), Qt.AlignCenter, "Loading awesomeness...")
    
    painter.end()
    
    splash = QSplashScreen(pixmap)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    
    return splash


def apply_application_style(app: QApplication):
    """Apply global application styling - Modern Technological Theme."""
    # Load and apply stylesheet
    style = """
    /* Global Styles - Dark Tech Theme */
    QWidget {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        font-size: 14px;
        color: #E8EAED;
        background-color: #0A0E27;
    }
    
    /* Main Window */
    QMainWindow {
        background-color: #0A0E27;
    }
    
    /* Buttons */
    QPushButton {
        padding: 8px 16px;
        border-radius: 6px;
        border: 1px solid #00D4FF;
        background-color: rgba(0, 212, 255, 0.1);
        color: #00D4FF;
        min-height: 32px;
        font-weight: 500;
    }
    
    QPushButton:hover {
        background-color: rgba(0, 212, 255, 0.2);
        border-color: #00FF88;
        color: #00FF88;
    }
    
    QPushButton#primary-button {
        background-color: #00D4FF;
        color: #0A0E27;
        border: none;
        font-weight: bold;
    }
    
    QPushButton#primary-button:hover {
        background-color: #00FF88;
    }
    
    QPushButton#success-button {
        background-color: #00FF88;
        color: #0A0E27;
        border: none;
        font-weight: bold;
    }
    
    QPushButton#danger-button {
        background-color: #FF3366;
        color: white;
        border: none;
    }
    
    QPushButton#hero-button {
        background: linear-gradient(135deg, #00D4FF 0%, #00FF88 100%);
        color: #0A0E27;
        border: none;
        font-size: 16px;
        font-weight: bold;
    }
    
    QPushButton#hero-button-secondary {
        background: transparent;
        color: #00D4FF;
        border: 2px solid #00D4FF;
        font-size: 16px;
        font-weight: bold;
    }
    
    /* Sidebar */
    QWidget#sidebar {
        background-color: #1A1F3A;
        color: #E8EAED;
        border-right: 1px solid #00D4FF;
    }
    
    QLabel#sidebar-title {
        color: #00D4FF;
        padding: 10px;
        font-weight: bold;
    }
    
    QListWidget#guide-list {
        background-color: #0A0E27;
        color: #E8EAED;
        border: 1px solid #1A1F3A;
        border-radius: 4px;
    }
    
    QListWidget#guide-list::item {
        padding: 8px;
        border-bottom: 1px solid #1A1F3A;
    }
    
    QListWidget#guide-list::item:selected {
        background-color: rgba(0, 212, 255, 0.2);
        color: #00D4FF;
    }
    
    QListWidget#guide-list::item:hover {
        background-color: rgba(0, 212, 255, 0.1);
    }
    
    /* Welcome Screen */
    QWidget#welcome-screen {
        background-color: #0A0E27;
    }
    
    QLabel#welcome-title {
        color: #00D4FF;
        padding: 20px;
        font-weight: bold;
    }
    
    QLabel#welcome-subtitle {
        color: #9AA0A6;
        padding: 10px;
    }
    
    /* Group Boxes */
    QGroupBox {
        font-weight: bold;
        border: 2px solid #00D4FF;
        border-radius: 8px;
        margin-top: 10px;
        padding-top: 10px;
        background-color: rgba(26, 31, 58, 0.5);
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
        background-color: #0A0E27;
        color: #00D4FF;
    }
    
    /* Combo Boxes */
    QComboBox {
        padding: 6px;
        border: 1px solid #00D4FF;
        border-radius: 4px;
        background-color: #1A1F3A;
        color: #E8EAED;
        min-height: 30px;
    }
    
    QComboBox:hover {
        border-color: #00FF88;
    }
    
    QComboBox::drop-down {
        border: none;
        background-color: #00D4FF;
        width: 20px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #1A1F3A;
        color: #E8EAED;
        selection-background-color: rgba(0, 212, 255, 0.2);
        border: 1px solid #00D4FF;
    }
    
    /* Text Areas */
    QTextEdit, QLineEdit {
        padding: 6px;
        border: 1px solid #00D4FF;
        border-radius: 4px;
        background-color: #1A1F3A;
        color: #E8EAED;
    }
    
    QTextEdit:focus, QLineEdit:focus {
        border-color: #00FF88;
        outline: none;
    }
    
    /* Progress Bar */
    QProgressBar {
        border: 1px solid #00D4FF;
        border-radius: 4px;
        text-align: center;
        background-color: #1A1F3A;
        color: #00D4FF;
    }
    
    QProgressBar::chunk {
        background: linear-gradient(90deg, #00D4FF 0%, #00FF88 100%);
        border-radius: 3px;
    }
    
    /* Status Bar */
    QStatusBar {
        background-color: #1A1F3A;
        color: #00D4FF;
        border-top: 1px solid #00D4FF;
    }
    
    /* Menu Bar */
    QMenuBar {
        background-color: #1A1F3A;
        color: #E8EAED;
        border-bottom: 1px solid #00D4FF;
    }
    
    QMenuBar::item:selected {
        background-color: rgba(0, 212, 255, 0.2);
        color: #00D4FF;
    }
    
    QMenu {
        background-color: #1A1F3A;
        border: 1px solid #00D4FF;
        color: #E8EAED;
    }
    
    QMenu::item:selected {
        background-color: rgba(0, 212, 255, 0.2);
        color: #00D4FF;
    }
    
    /* Tool Bar */
    QToolBar {
        background-color: #1A1F3A;
        border: none;
        spacing: 3px;
        padding: 5px;
        border-bottom: 1px solid #00D4FF;
    }
    
    QToolButton {
        background-color: transparent;
        border: none;
        padding: 5px;
        border-radius: 4px;
        color: #E8EAED;
    }
    
    QToolButton:hover {
        background-color: rgba(0, 212, 255, 0.1);
        color: #00D4FF;
    }
    
    /* Scroll Bars */
    QScrollBar:vertical {
        background-color: #1A1F3A;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #00D4FF;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #00FF88;
    }
    
    /* Labels */
    QLabel {
        color: #E8EAED;
    }
    
    QLabel#help-text {
        color: #9AA0A6;
    }
    
    /* Radio Buttons */
    QRadioButton {
        color: #E8EAED;
    }
    
    QRadioButton::indicator {
        width: 16px;
        height: 16px;
        border: 2px solid #00D4FF;
        border-radius: 8px;
        background-color: transparent;
    }
    
    QRadioButton::indicator:checked {
        background-color: #00D4FF;
    }
    
    /* Spin Box */
    QSpinBox {
        padding: 4px;
        border: 1px solid #00D4FF;
        border-radius: 4px;
        background-color: #1A1F3A;
        color: #E8EAED;
    }
    """
    
    app.setStyleSheet(style)


def main():
    """Main application entry point."""
    # Set up signal handler for Ctrl-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    
    # Set up logging
    setup_logging()
    
    # Apply styling
    apply_application_style(app)
    
    # Show splash screen
    splash = create_splash_screen(app)
    splash.show()
    app.processEvents()
    
    # Create main window
    window = MainWindow()
    
    # Close splash and show main window after a short delay
    def show_main_window():
        splash.close()
        window.show()
    
    QTimer.singleShot(2000, show_main_window)  # 2 second splash
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
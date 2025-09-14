#!/usr/bin/env python3
"""
B-Tree Visualizer - Main application entry point.
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QPalette, QColor

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from app.bridge import Bridge, register_bridge


def main():
    """Main application function."""
    app = QApplication(sys.argv)
    app.setApplicationName("B-Tree Visualizer")
    app.setApplicationDisplayName("B-Tree Visualizer")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("YGRA")
    
    # Enhanced dark theme
    app.setStyle("Fusion")
    
    # dark_palette = QPalette()
    # dark_palette.setColor(QPalette.ColorRole.Window, QColor(24, 24, 27))
    # dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(244, 244, 245))
    # dark_palette.setColor(QPalette.ColorRole.Base, QColor(39, 39, 42))
    # dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(63, 63, 70))
    # dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(244, 244, 245))
    # dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(244, 244, 245))
    # dark_palette.setColor(QPalette.ColorRole.Text, QColor(244, 244, 245))
    # dark_palette.setColor(QPalette.ColorRole.Button, QColor(39, 39, 42))
    # dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(244, 244, 245))
    # dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(220, 38, 127))
    # dark_palette.setColor(QPalette.ColorRole.Link, QColor(59, 130, 246))
    # dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(59, 130, 246))
    # dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    # app.setPalette(dark_palette)
    
    # Windows dark title bar support
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            
            def set_dark_title_bar(hwnd):
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                value = ctypes.c_int(1)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 
                    ctypes.byref(value), ctypes.sizeof(value)
                )
            
            app.set_dark_titlebar_func = set_dark_title_bar
        except Exception as e:
            print(f"Could not configure dark title bar: {e}")

    # Register QML types
    register_bridge()

    # Create QML engine
    engine = QQmlApplicationEngine()

    # Load QML file
    qml_file = Path(__file__).parent / "src" / "ui" / "main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))

    # Apply dark title bar after window creation
    if hasattr(app, 'set_dark_titlebar_func'):
        def apply_dark_titlebar():
            for window in app.allWindows():
                if window.winId():
                    try:
                        app.set_dark_titlebar_func(int(window.winId()))
                    except Exception as e:
                        print(f"Could not apply dark title bar: {e}")
        
        QTimer.singleShot(100, apply_dark_titlebar)

    # Check if QML loaded successfully
    if not engine.rootObjects():
        return -1

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

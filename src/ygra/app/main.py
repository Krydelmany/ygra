from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


APP_NAME = "ygra"
APP_TITLE = "ygra — Árvores Múltiplas"
APP_VERSION = "0.1.0"


def _qml_path() -> Path:
    # Resolve to .../src/ygra/ui/main.qml (works in dev and when frozen with PyInstaller if bundled)
    here = Path(__file__).resolve()
    ui_dir = here.parent.parent / "ui"
    main_qml = ui_dir / "main.qml"
    if not main_qml.exists():
        # fallback for some frozen layouts
        alt = Path(__file__).parent / "ui" / "main.qml"
        if alt.exists():
            return alt
        raise FileNotFoundError(f"main.qml não encontrado. Procurei em: {main_qml}")
    return main_qml


def main() -> int:
    # Qt Application
    app = QGuiApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("ygra")
    app.setOrganizationDomain("github.com/Krydelmany/ygra")

    engine = QQmlApplicationEngine()

    # Expose a minimal context (strings only for now)
    engine.rootContext().setContextProperty("APP_TITLE", APP_TITLE)
    engine.rootContext().setContextProperty("APP_VERSION", APP_VERSION)

    # Load QML
    qml_file = _qml_path()
    engine.load(str(qml_file))

    if not engine.rootObjects():
        # If QML failed to load, exit non-zero
        return 1

    return app.exec()

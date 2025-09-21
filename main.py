import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QPalette, QColor

sys.path.insert(0, str(Path(__file__).parent / "src"))

from app.bridge import Bridge, register_bridge


def main():
    aplicacao = QApplication(sys.argv)
    aplicacao.setApplicationName("Arvores Multiplas")
    aplicacao.setApplicationDisplayName("Arvores Multiplas")
    
    aplicacao.setStyle("Fusion")
    
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            
            def set_dark_title_bar(hwnd):
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                valor = ctypes.c_int(1)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 
                    ctypes.byref(valor), ctypes.sizeof(valor)
                )
            
            aplicacao.set_dark_titlebar_func = set_dark_title_bar
        except Exception as e:
            print(f"Não foi possível configurar barra de título escura: {e}")

    register_bridge()

    motor = QQmlApplicationEngine()

    arquivo_qml = Path(__file__).parent / "src" / "ui" / "main.qml"
    motor.load(QUrl.fromLocalFile(str(arquivo_qml)))

    if hasattr(aplicacao, 'set_dark_titlebar_func'):
        def aplicar_titulo_escuro():
            for janela in aplicacao.allWindows():
                if janela.winId():
                    try:
                        aplicacao.set_dark_titlebar_func(int(janela.winId()))
                    except Exception as e:
                        print(f"Não foi possível aplicar barra de título escura: {e}")
        
        QTimer.singleShot(100, aplicar_titulo_escuro)

    if not motor.rootObjects():
        return -1

    return aplicacao.exec()


if __name__ == "__main__":
    sys.exit(main())

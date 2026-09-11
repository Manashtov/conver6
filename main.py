import sys
from PySide6.QtWidgets import QApplication

from core.settings.settings_manager import SettingsManager
from ui.main_window import MainWindow


def main() -> int:
    """Punto de entrada principal para Conver6."""
    app = QApplication(sys.argv)
    app.setApplicationName("Conver6")
    app.setOrganizationName("Conver6Project")

    settings_manager = SettingsManager()
    window = MainWindow(settings_manager)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
from PySide6.QtWidgets import QStackedWidget
from core.settings.settings_manager import SettingsManager


class NavigationController:
    """Gestiona el intercambio de pestañas en el QStackedWidget sin recargar ventanas."""

    def __init__(self, stack: QStackedWidget, settings: SettingsManager) -> None:
        self.stack = stack
        self.settings = settings
        self.mapping = {
            "Imágenes": 0,
            "Audio": 1,
            "Documentos": 2
        }

    def navigate_to(self, section_name: str) -> None:
        idx = self.mapping.get(section_name, 0)
        self.stack.setCurrentIndex(idx)
        self.settings.set_last_section(section_name)
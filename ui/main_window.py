from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PySide6.QtCore import QSize

from core.settings.settings_manager import SettingsManager
from core.conversion.conversion_registry import ConversionRegistry
from core.conversion.conversion_service import ConversionService
from core.image.image_converter import ImageConverter
from core.audio.audio_converter import AudioConverter
from core.document.document_converter import DocumentConverter

from ui.widgets.sidebar import Sidebar
from ui.pages.images_page import ImagesPage
from ui.pages.audio_page import AudioPage
from ui.pages.documents_page import DocumentsPage
from ui.dialogs.settings_dialog import SettingsDialog
from ui.controllers.navigation_controller import NavigationController
from ui.styles.theme_manager import ThemeManager
from ui.styles.palettes import PALETTES


class MainWindow(QMainWindow):
    """Coordinador visual principal de Conver6."""

    def __init__(self, settings_manager: SettingsManager) -> None:
        super().__init__()
        self.settings = settings_manager

        registry = ConversionRegistry()
        registry.register("images", ImageConverter())
        registry.register("audio", AudioConverter())
        registry.register("documents", DocumentConverter())
        self.service = ConversionService(registry)

        self.setWindowTitle("Conver6 - Conversor Universal")
        self.resize(QSize(990, 670))

        root_widget = QWidget()
        root_widget.setObjectName("centralWidget")
        root_layout = QHBoxLayout(root_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        self.setCentralWidget(root_widget)

        self.sidebar = Sidebar()
        root_layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.stack.setObjectName("MainStack")
        root_layout.addWidget(self.stack, stretch=1)

        self.page_images = ImagesPage(self.service)
        self.page_audio = AudioPage(self.service)
        self.page_docs = DocumentsPage(self.service)

        self.stack.addWidget(self.page_images)
        self.stack.addWidget(self.page_audio)
        self.stack.addWidget(self.page_docs)

        self.nav_controller = NavigationController(self.stack, self.settings)

        self._connect_signals()
        self._restore_preferences()

    def _connect_signals(self) -> None:
        self.sidebar.navigation_requested.connect(self._on_navigation)
        self.sidebar.settings_requested.connect(self._open_settings)
        self.sidebar.toggle_theme_requested.connect(self._toggle_theme)

    def _on_navigation(self, section_name: str) -> None:
        self.nav_controller.navigate_to(section_name)
        palette_color = PALETTES.get(self.settings.get_color_palette(), PALETTES["Teal"])["primary"]
        self.sidebar.apply_palette(palette_color)

    def _restore_preferences(self) -> None:
        last_sec = self.settings.get_last_section()
        self.nav_controller.navigate_to(last_sec)
        self.sidebar.set_active_section(last_sec)
        self._apply_current_style()

    def _apply_current_style(self) -> None:
        mode = self.settings.get_theme_mode()
        palette_name = self.settings.get_color_palette()
        palette_color = PALETTES.get(palette_name, PALETTES["Teal"])["primary"]
        is_dark = (mode == "dark")

        self.setStyleSheet(ThemeManager.get_stylesheet(is_dark, palette_name))
        self.sidebar.update_theme_icon(is_dark)
        self.sidebar.apply_palette(palette_color)

        for page in (self.page_images, self.page_audio, self.page_docs):
            page.apply_palette_color(palette_color)

    def _toggle_theme(self) -> None:
        cur = self.settings.get_theme_mode()
        new_mode = "light" if cur == "dark" else "dark"
        self.settings.set_theme_mode(new_mode)
        self._apply_current_style()

    def _open_settings(self) -> None:
        dlg = SettingsDialog(self.settings, self)
        if dlg.exec():
            self._apply_current_style()
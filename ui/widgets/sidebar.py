from typing import Dict
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Signal, QSize, Qt
import qtawesome as qta


class Sidebar(QWidget):
    """Barra lateral cuyos iconos se integran completamente a la paleta del usuario."""
    navigation_requested = Signal(str)
    settings_requested = Signal()
    toggle_theme_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(225)
        self._current_palette_color = "#009688"
        self._is_dark_mode = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 20, 14, 20)
        layout.setSpacing(12)

        # Placeholder para logotipo
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        self.logo_placeholder = QFrame()
        self.logo_placeholder.setObjectName("LogoPlaceholder")
        self.logo_placeholder.setFixedSize(36, 36)
        self.lbl_logo_icon = QLabel(self.logo_placeholder)
        self.lbl_logo_icon.setAlignment(Qt.AlignCenter)
        layout_box = QVBoxLayout(self.logo_placeholder)
        layout_box.setContentsMargins(0, 0, 0, 0)
        layout_box.addWidget(self.lbl_logo_icon)

        title = QLabel("Conver6")
        title.setObjectName("BrandTitle")

        header_layout.addWidget(self.logo_placeholder)
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Panel agrupador de navegación
        self.nav_group = QFrame()
        self.nav_group.setObjectName("NavGroupFrame")
        group_layout = QVBoxLayout(self.nav_group)
        group_layout.setContentsMargins(8, 8, 8, 8)
        group_layout.setSpacing(8)

        self._nav_buttons: Dict[str, QPushButton] = {}
        self.btn_images = self._create_nav_btn("fa5s.images", "Imágenes")
        self.btn_audio = self._create_nav_btn("fa5s.music", "Audio")
        self.btn_docs = self._create_nav_btn("fa5s.file-invoice", "Documentos")

        group_layout.addWidget(self.btn_images)
        group_layout.addWidget(self.btn_audio)
        group_layout.addWidget(self.btn_docs)
        layout.addWidget(self.nav_group)

        layout.addStretch()

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName("SeparatorLine")
        layout.addWidget(line)

        self.btn_settings = self._create_bottom_btn("fa5s.sliders-h", "Configuración")
        self.btn_settings.clicked.connect(self.settings_requested.emit)
        layout.addWidget(self.btn_settings)

        self.btn_theme = self._create_bottom_btn("fa5s.sun", "Modo Claro")
        self.btn_theme.clicked.connect(self.toggle_theme_requested.emit)
        layout.addWidget(self.btn_theme)

        self.set_active_section("Imágenes")

    def _create_nav_btn(self, icon_name: str, text: str) -> QPushButton:
        btn = QPushButton(f"  {text}")
        btn.setObjectName("NavCardBtn")
        btn.setIconSize(QSize(20, 20))
        btn.setFixedHeight(48)
        btn.setProperty("active", "false")
        btn.setProperty("iconName", icon_name)
        self._nav_buttons[text] = btn
        btn.clicked.connect(lambda: self._on_btn_clicked(text))
        return btn

    def _create_bottom_btn(self, icon_name: str, text: str) -> QPushButton:
        btn = QPushButton(f"  {text}")
        btn.setObjectName("NavBottomBtn")
        btn.setIconSize(QSize(18, 18))
        btn.setFixedHeight(44)
        btn.setProperty("iconName", icon_name)
        return btn

    def _on_btn_clicked(self, section_name: str) -> None:
        self.set_active_section(section_name)
        self.navigation_requested.emit(section_name)

    def set_active_section(self, section_name: str) -> None:
        for name, btn in self._nav_buttons.items():
            is_active = (name == section_name)
            btn.setProperty("active", "true" if is_active else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self.apply_palette(self._current_palette_color)

    def apply_palette(self, primary_color: str) -> None:
        self._current_palette_color = primary_color
        self.lbl_logo_icon.setPixmap(qta.icon("fa5s.cubes", color=primary_color).pixmap(20, 20))

        # Iconos de secciones
        for name, btn in self._nav_buttons.items():
            icon_name = btn.property("iconName")
            is_active = btn.property("active") == "true"
            color = "#FFFFFF" if is_active else primary_color
            btn.setIcon(qta.icon(icon_name, color=color))

        # Iconos inferiores acordes a la paleta
        self.btn_settings.setIcon(qta.icon("fa5s.sliders-h", color=primary_color))
        theme_icon = "fa5s.sun" if self._is_dark_mode else "fa5s.moon"
        self.btn_theme.setIcon(qta.icon(theme_icon, color=primary_color))

    def update_theme_icon(self, is_dark: bool) -> None:
        self._is_dark_mode = is_dark
        self.btn_theme.setText("  Modo Claro" if is_dark else "  Modo Oscuro")
        self.apply_palette(self._current_palette_color)
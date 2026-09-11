from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QFileDialog
)
from core.settings.settings_manager import SettingsManager
from ui.styles.palettes import PALETTES


class SettingsDialog(QDialog):
    """Diálogo de configuración con herencia de tema claro/oscuro."""

    def __init__(self, settings_manager: SettingsManager, parent=None) -> None:
        super().__init__(parent)
        self.settings = settings_manager
        self.setWindowTitle("Configuración - Conver6")
        self.setFixedSize(480, 240)
        self.setObjectName("SettingsDialog")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Selección de color
        pal_layout = QHBoxLayout()
        lbl_pal = QLabel("Color Primario:")
        lbl_pal.setStyleSheet("font-weight: 700; font-size: 13px;")
        self.combo_palette = QComboBox()
        self.combo_palette.addItems(list(PALETTES.keys()))
        self.combo_palette.setCurrentText(self.settings.get_color_palette())
        pal_layout.addWidget(lbl_pal)
        pal_layout.addWidget(self.combo_palette, stretch=1)
        layout.addLayout(pal_layout)

        # Ruta FFmpeg
        ff_layout = QHBoxLayout()
        lbl_ff = QLabel("Ruta FFmpeg:")
        lbl_ff.setStyleSheet("font-weight: 700; font-size: 13px;")
        self.txt_ffmpeg = QLineEdit()
        self.txt_ffmpeg.setText(self.settings.get_ffmpeg_path() or "")
        self.txt_ffmpeg.setPlaceholderText("Automático (PATH del sistema)")
        btn_browse = QPushButton("Buscar")
        btn_browse.setObjectName("GhostBtn")
        btn_browse.clicked.connect(self._browse_ffmpeg)
        ff_layout.addWidget(lbl_ff)
        ff_layout.addWidget(self.txt_ffmpeg, stretch=1)
        ff_layout.addWidget(btn_browse)
        layout.addLayout(ff_layout)

        layout.addStretch()

        btn_save = QPushButton("Guardar Cambios")
        btn_save.setFixedHeight(44)
        btn_save.clicked.connect(self._save_and_close)
        layout.addWidget(btn_save)

    def _browse_ffmpeg(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar ejecutable FFmpeg", "", "Ejecutables (ffmpeg.exe);;Todos (*.*)"
        )
        if file_path:
            self.txt_ffmpeg.setText(file_path)

    def _save_and_close(self) -> None:
        self.settings.set_color_palette(self.combo_palette.currentText())
        self.settings.set_ffmpeg_path(self.txt_ffmpeg.text().strip())
        self.accept()
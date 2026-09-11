from pathlib import Path
from typing import Optional
from PySide6.QtCore import QSettings
from core.audio.audio_backend import AudioBackend


class SettingsManager:
    """Administra la persistencia de estados usando QSettings nativo del sistema."""

    def __init__(self) -> None:
        self._settings = QSettings("Conver6Project", "Conver6")
        ffmpeg = self.get_ffmpeg_path()
        if ffmpeg:
            AudioBackend.set_custom_ffmpeg_path(Path(ffmpeg))

    def get_theme_mode(self) -> str:
        return str(self._settings.value("ui/theme_mode", "dark"))

    def set_theme_mode(self, mode: str) -> None:
        self._settings.setValue("ui/theme_mode", mode)

    def get_color_palette(self) -> str:
        return str(self._settings.value("ui/color_palette", "Teal"))

    def set_color_palette(self, palette_name: str) -> None:
        self._settings.setValue("ui/color_palette", palette_name)

    def get_last_section(self) -> str:
        return str(self._settings.value("navigation/last_section", "Imágenes"))

    def set_last_section(self, section: str) -> None:
        self._settings.setValue("navigation/last_section", section)

    def get_ffmpeg_path(self) -> Optional[str]:
        val = self._settings.value("system/ffmpeg_path", "")
        return str(val) if val else None

    def set_ffmpeg_path(self, path_str: str) -> None:
        self._settings.setValue("system/ffmpeg_path", path_str)
        if path_str:
            AudioBackend.set_custom_ffmpeg_path(Path(path_str))
        else:
            AudioBackend.set_custom_ffmpeg_path(None)
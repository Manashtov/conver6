import sys
import shutil
from pathlib import Path
from typing import Optional
from core.exceptions import DependencyMissingError


class AudioBackend:
    """Gestiona la detección y ruta de FFmpeg tanto en modo desarrollo como empaquetado."""
    _custom_path: Optional[Path] = None

    @classmethod
    def set_custom_ffmpeg_path(cls, path: Optional[Path]) -> None:
        cls._custom_path = path

    @classmethod
    def get_ffmpeg_executable(cls) -> str:
        # 1. Ruta manual configurada por el usuario (si existe)
        if cls._custom_path and cls._custom_path.exists():
            return str(cls._custom_path)

        # 2. Modo empaquetado con PyInstaller (carpeta temporal interna)
        if getattr(sys, "frozen", False):
            base_dir = Path(sys._MEIPASS)
            bundled_ffmpeg = base_dir / "bin" / "ffmpeg.exe"
            if bundled_ffmpeg.exists():
                return str(bundled_ffmpeg)

        # 3. Modo desarrollo local (carpeta bin/ junto al código)
        local_bin = Path(__file__).resolve().parent.parent.parent / "bin" / "ffmpeg.exe"
        if local_bin.exists():
            return str(local_bin)

        # 4. PATH del sistema de Windows
        found = shutil.which("ffmpeg")
        if found:
            return found

        raise DependencyMissingError(
            "No se encontró FFmpeg.\n"
            "Asegúrese de incluir 'ffmpeg.exe' en la carpeta bin/ o instalarlo en el sistema."
        )

    @classmethod
    def is_available(cls) -> bool:
        try:
            cls.get_ffmpeg_executable()
            return True
        except DependencyMissingError:
            return False
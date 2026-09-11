from pathlib import Path
from core.exceptions import ValidationError


class AudioValidator:
    """Valida extensiones y presencia física de archivos de audio."""
    SUPPORTED = {"MP3", "WAV", "OGG"}

    @classmethod
    def validate(cls, path: Path) -> None:
        if not path.exists():
            raise ValidationError(f"El archivo de audio no existe: {path.name}")
        ext = path.suffix.lstrip(".").upper()
        if ext not in cls.SUPPORTED:
            raise ValidationError(f"Formato no admitido para audio: {ext}")
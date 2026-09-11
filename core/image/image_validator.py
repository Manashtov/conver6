from pathlib import Path
from PIL import Image
from core.exceptions import ValidationError


class ImageValidator:
    """Valida extensiones e integridad real del archivo de imagen."""
    SUPPORTED = {"SVG", "PNG", "JPG", "JPEG"}

    @classmethod
    def validate(cls, path: Path) -> None:
        if not path.exists():
            raise ValidationError(f"El archivo no existe: {path.name}")
        ext = path.suffix.lstrip(".").upper()
        if ext not in cls.SUPPORTED:
            raise ValidationError(f"Extensión no admitida para imagen: {ext}")
        if ext != "SVG":
            try:
                with Image.open(path) as img:
                    img.verify()
            except Exception as e:
                raise ValidationError(f"Archivo de imagen corrupto: {str(e)}")
from pathlib import Path
from core.exceptions import ValidationError


class DocumentValidator:
    """Valida extensiones soportadas por el motor de documentos."""
    SUPPORTED = {"PDF", "DOC", "DOCX", "TXT"}

    @classmethod
    def validate(cls, path: Path) -> None:
        if not path.exists():
            raise ValidationError(f"El documento no existe: {path.name}")
        ext = path.suffix.lstrip(".").upper()
        if ext not in cls.SUPPORTED:
            raise ValidationError(f"Extensión documental no soportada: {ext}")
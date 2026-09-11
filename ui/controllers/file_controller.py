from pathlib import Path
from typing import List, Set


class FileController:
    """Valida la inclusión de archivos de acuerdo a las extensiones válidas."""

    @staticmethod
    def filter_supported_files(paths: List[Path], supported_extensions: Set[str]) -> List[Path]:
        valid = set(e.upper() for e in supported_extensions)
        return [p for p in paths if p.is_file() and p.suffix.lstrip(".").upper() in valid]
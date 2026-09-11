from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ConversionResult:
    """Resultado devuelto por los conversores concretos."""
    success: bool
    output_path: Optional[Path] = None
    error_message: Optional[str] = None
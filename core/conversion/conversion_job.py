from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional
import uuid


class JobStatus(Enum):
    PENDING = "Pendiente"
    CONVERTING = "Convirtiendo..."
    COMPLETED = "Completado"
    SAVED = "Guardado"
    ERROR = "Error"


@dataclass
class ConversionJob:
    """Modelo desacoplado de datos que representa una tarea de conversión."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    input_path: Path = field(default_factory=Path)
    output_path: Optional[Path] = None
    temp_output_path: Optional[Path] = None
    source_format: str = ""
    target_format: str = ""
    compression_level: int = 80
    status: JobStatus = JobStatus.PENDING
    progress: int = 0
    error_message: Optional[str] = None
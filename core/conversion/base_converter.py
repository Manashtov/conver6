from abc import ABC, abstractmethod
from typing import Callable, List, Optional
from core.conversion.conversion_job import ConversionJob
from core.conversion.conversion_result import ConversionResult


class BaseConverter(ABC):
    """Contrato base que deben implementar todos los conversores."""

    @abstractmethod
    def supported_source_formats(self) -> List[str]:
        pass

    @abstractmethod
    def supported_target_formats(self) -> List[str]:
        pass

    @abstractmethod
    def convert(
        self,
        job: ConversionJob,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> ConversionResult:
        pass
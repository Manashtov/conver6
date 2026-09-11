from typing import Callable, Optional
from core.conversion.conversion_job import ConversionJob
from core.conversion.conversion_registry import ConversionRegistry
from core.conversion.conversion_result import ConversionResult
from core.exceptions import UnsupportedFormatError


class ConversionService:
    """Coordinador central que rutea las conversiones al motor adecuado."""

    def __init__(self, registry: ConversionRegistry) -> None:
        self._registry = registry

    def convert(
        self,
        job: ConversionJob,
        category: str,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> ConversionResult:
        converter = self._registry.get_converter(category)
        if not converter:
            raise UnsupportedFormatError(f"No hay conversor registrado para la sección: {category}")
        return converter.convert(job, progress_callback)
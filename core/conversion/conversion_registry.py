from typing import Dict, Optional
from core.conversion.base_converter import BaseConverter


class ConversionRegistry:
    """Registro desacoplado de conversores clasificados por categoría."""

    def __init__(self) -> None:
        self._converters: Dict[str, BaseConverter] = {}

    def register(self, category: str, converter: BaseConverter) -> None:
        self._converters[category.lower()] = converter

    def get_converter(self, category: str) -> Optional[BaseConverter]:
        return self._converters.get(category.lower())
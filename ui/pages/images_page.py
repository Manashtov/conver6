from core.conversion.conversion_service import ConversionService
from ui.pages.base_page import BaseConversionPage


class ImagesPage(BaseConversionPage):
    """Página especializada en conversión de formatos de imagen."""

    def __init__(self, service: ConversionService, parent=None) -> None:
        super().__init__(
            category="images",
            supported_sources={"SVG", "PNG", "JPG", "JPEG"},
            supported_targets=["PNG", "JPG", "JPEG", "SVG"],
            service=service,
            parent=parent
        )
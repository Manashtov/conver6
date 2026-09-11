from core.conversion.conversion_service import ConversionService
from ui.pages.base_page import BaseConversionPage


class AudioPage(BaseConversionPage):
    """Página especializada en conversión de audio."""

    def __init__(self, service: ConversionService, parent=None) -> None:
        super().__init__(
            category="audio",
            supported_sources={"MP3", "WAV", "OGG"},
            supported_targets=["MP3", "WAV", "OGG"],
            service=service,
            parent=parent
        )
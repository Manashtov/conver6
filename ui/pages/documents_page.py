from core.conversion.conversion_service import ConversionService
from ui.pages.base_page import BaseConversionPage


class DocumentsPage(BaseConversionPage):
    """Página especializada en transformación documental."""

    def __init__(self, service: ConversionService, parent=None) -> None:
        super().__init__(
            category="documents",
            supported_sources={"PDF", "DOC", "DOCX", "TXT"},
            supported_targets=["PDF", "DOCX", "TXT"],
            service=service,
            parent=parent
        )
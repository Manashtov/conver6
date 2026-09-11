from typing import Dict, List
from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from PySide6.QtCore import Signal, Qt

from core.conversion.conversion_job import ConversionJob, JobStatus
from ui.widgets.file_card import FileCard


class FileList(QScrollArea):
    """Lista con tarjetas espaciadas limpiamente."""
    card_deleted = Signal(str)
    card_save = Signal(str)
    card_format_changed = Signal(str, str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setObjectName("FileListScroll")
        self.setStyleSheet("border: none; background: transparent;")
        self._palette_color = "#009688"

        self._container = QWidget()
        self._container.setObjectName("FileListContainer")
        self._container.setStyleSheet("background: transparent;")
        self._layout = QVBoxLayout(self._container)
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.setSpacing(14)
        self._layout.setContentsMargins(6, 6, 12, 6)
        self.setWidget(self._container)

        self._cards: Dict[str, FileCard] = {}

    def set_palette_color(self, color: str) -> None:
        self._palette_color = color
        for card in self._cards.values():
            card.set_palette_color(color)

    def add_card(self, job: ConversionJob, target_formats: List[str]) -> None:
        card = FileCard(job, target_formats, palette_color=self._palette_color)
        card.delete_requested.connect(self._on_delete)
        card.save_requested.connect(self.card_save.emit)
        card.target_format_changed.connect(self.card_format_changed.emit)
        self._cards[job.id] = card
        self._layout.addWidget(card)

    def _on_delete(self, job_id: str) -> None:
        card = self._cards.pop(job_id, None)
        if card:
            self._layout.removeWidget(card)
            card.deleteLater()
            self.card_deleted.emit(job_id)

    def update_job_progress(self, job_id: str, status: JobStatus, progress: int, msg: str = "") -> None:
        if job_id in self._cards:
            self._cards[job_id].update_state(status, progress, msg)

    def clear(self) -> None:
        for card in self._cards.values():
            self._layout.removeWidget(card)
            card.deleteLater()
        self._cards.clear()
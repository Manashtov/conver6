from pathlib import Path
from typing import List, Set
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QMouseEvent
import qtawesome as qta


class DropArea(QFrame):
    """Área receptora con icono dinámico según paleta del usuario."""
    files_dropped = Signal(list)
    clicked = Signal()

    def __init__(self, supported_extensions: Set[str], parent=None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.supported_extensions = {ext.lower().strip() for ext in supported_extensions}
        self.setAcceptDrops(True)
        self.setFixedHeight(125)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("DropArea")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)

        self.icon_lbl = QLabel()
        self.icon_lbl.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.icon_lbl.setAlignment(Qt.AlignCenter)

        self.text_lbl = QLabel("Arrastra tus archivos aquí o haz clic para explorar")
        self.text_lbl.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.text_lbl.setObjectName("DropText")
        self.text_lbl.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.icon_lbl)
        layout.addWidget(self.text_lbl)

        self.set_icon_color("#009688")

    def set_icon_color(self, color: str) -> None:
        self.icon_lbl.setPixmap(qta.icon("fa5s.cloud-upload-alt", color=color).pixmap(38, 38))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            event.accept()
        else:
            super().mousePressEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragActive", "true")
            self.style().unpolish(self)
            self.style().polish(self)

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragLeaveEvent(self, event) -> None:
        self.setProperty("dragActive", "false")
        self.style().unpolish(self)
        self.style().polish(self)
        event.accept()

    def dropEvent(self, event: QDropEvent) -> None:
        self.setProperty("dragActive", "false")
        self.style().unpolish(self)
        self.style().polish(self)
        valid_paths: List[Path] = []
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = Path(url.toLocalFile())
                if file_path.is_file():
                    ext = file_path.suffix.lstrip(".").lower()
                    if ext in self.supported_extensions:
                        valid_paths.append(file_path)
            if valid_paths:
                self.files_dropped.emit(valid_paths)
                event.acceptProposedAction()
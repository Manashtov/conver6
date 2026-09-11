from PySide6.QtWidgets import QWidget, QHBoxLayout, QProgressBar, QLabel


class ProgressWidget(QWidget):
    """Barra global gruesa y texto de seguimiento de lote de alta legibilidad."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 6, 4, 6)
        layout.setSpacing(16)

        self.label = QLabel("Listo")
        self.label.setObjectName("BatchLabel")
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("BatchProgressBar")
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar, stretch=1)

    def update_progress(self, current: int, total: int) -> None:
        if total == 0:
            self.progress_bar.setValue(0)
            self.label.setText("Listo")
            return
        percent = int((current / total) * 100)
        self.progress_bar.setValue(percent)
        self.label.setText(f"PROCESANDO LOTE: {percent}% ({current}/{total})")
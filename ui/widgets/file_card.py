from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QProgressBar
)
from PySide6.QtCore import Signal, QSize, Qt
import qtawesome as qta

from core.conversion.conversion_job import ConversionJob, JobStatus


class FileCard(QFrame):
    """Tarjeta individual con barra visible e icono guardar acorde a la paleta."""
    delete_requested = Signal(str)
    save_requested = Signal(str)
    target_format_changed = Signal(str, str)

    def __init__(self, job: ConversionJob, target_formats: list[str], palette_color: str = "#009688", parent=None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.job = job
        self.palette_color = palette_color
        self.setObjectName("FileCard")
        self.setFixedHeight(105)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 14, 20, 14)
        main_layout.setSpacing(18)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)

        self.lbl_name = QLabel(job.input_path.name)
        self.lbl_name.setObjectName("CardTitle")

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(job.progress)

        self.lbl_status = QLabel(job.status.value)
        self.lbl_status.setObjectName("StatusPending")

        info_layout.addWidget(self.lbl_name)
        info_layout.addWidget(self.progress_bar)
        info_layout.addWidget(self.lbl_status)
        main_layout.addLayout(info_layout, stretch=1)

        self.combo_format = QComboBox()
        self.combo_format.setFixedSize(100, 42)
        for fmt in target_formats:
            self.combo_format.addItem(fmt.upper())
        if job.target_format.upper() in [t.upper() for t in target_formats]:
            self.combo_format.setCurrentText(job.target_format.upper())

        self.combo_format.currentTextChanged.connect(
            lambda fmt: self.target_format_changed.emit(self.job.id, fmt)
        )
        main_layout.addWidget(self.combo_format)

        # Botón Guardar individual: Siempre usa la paleta del usuario
        self.btn_save = QPushButton()
        self.btn_save.setObjectName("CardSaveBtn")
        self.btn_save.setFixedSize(46, 42)
        self.btn_save.setIcon(qta.icon("fa5s.arrow-down", color=self.palette_color))
        self.btn_save.setIconSize(QSize(18, 18))
        self.btn_save.setEnabled(False)
        self.btn_save.setToolTip("Guardar archivo convertido")
        self.btn_save.clicked.connect(lambda: self.save_requested.emit(self.job.id))
        main_layout.addWidget(self.btn_save)

        # Botón Eliminar individual
        self.btn_delete = QPushButton()
        self.btn_delete.setObjectName("CardDeleteBtn")
        self.btn_delete.setFixedSize(46, 42)
        self.btn_delete.setIcon(qta.icon("fa5s.trash-alt", color="#EF4444"))
        self.btn_delete.setIconSize(QSize(18, 18))
        self.btn_delete.setToolTip("Quitar archivo de la lista")
        self.btn_delete.clicked.connect(lambda: self.delete_requested.emit(self.job.id))
        main_layout.addWidget(self.btn_delete)

    def set_palette_color(self, color: str) -> None:
        self.palette_color = color
        if self.job.status != JobStatus.COMPLETED:
            self.btn_save.setIcon(qta.icon("fa5s.arrow-down", color=self.palette_color))

    def update_state(self, status: JobStatus, progress: int, msg: str = "") -> None:
        self.progress_bar.setValue(progress)
        if status == JobStatus.COMPLETED:
            self.lbl_status.setText("✓ Completado con éxito")
            self.lbl_status.setObjectName("StatusCompleted")
            self.btn_save.setEnabled(True)
            self.btn_save.setIcon(qta.icon("fa5s.download", color=self.palette_color))
        elif status == JobStatus.SAVED:
            self.lbl_status.setText("✓ Guardado correctamente")
            self.lbl_status.setObjectName("StatusSaved")
            self.btn_save.setEnabled(False)
            self.btn_save.setIcon(qta.icon("fa5s.check", color="#10B981"))
        elif status == JobStatus.ERROR:
            self.lbl_status.setText(f"✕ {msg or 'Error en conversión'}")
            self.lbl_status.setObjectName("StatusError")
        else:
            self.lbl_status.setText(f"{status.value} ({progress}%)" if progress > 0 else status.value)
            self.lbl_status.setObjectName("StatusPending")

        for w in (self.lbl_status, self.btn_save, self.progress_bar):
            w.style().unpolish(w)
            w.style().polish(w)
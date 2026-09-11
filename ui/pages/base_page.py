from pathlib import Path
from typing import List, Set
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog

from core.conversion.conversion_job import ConversionJob, JobStatus
from core.conversion.conversion_service import ConversionService
from ui.widgets.drop_area import DropArea
from ui.widgets.file_list import FileList
from ui.widgets.conversion_controls import ConversionControls
from ui.widgets.progress_widget import ProgressWidget
from ui.workers.conversion_worker import ConversionWorker
from ui.controllers.save_controller import SaveController


class BaseConversionPage(QWidget):
    """Página base funcional común con aislamiento estricto por pestaña."""

    def __init__(
        self,
        category: str,
        supported_sources: Set[str],
        supported_targets: List[str],
        service: ConversionService,
        parent=None
    ) -> None:
        super().__init__(parent)
        self.category = category
        self.supported_sources = {s.lower().lstrip(".") for s in supported_sources}
        self.supported_targets = [t.lower().lstrip(".") for t in supported_targets]
        self.service = service
        self.jobs: List[ConversionJob] = []
        self._worker = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        self.drop_area = DropArea(self.supported_sources)
        self.drop_area.files_dropped.connect(self.add_files)
        self.drop_area.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.drop_area)

        self.file_list = FileList()
        self.file_list.card_deleted.connect(self.delete_job)
        self.file_list.card_save.connect(self.save_single)
        self.file_list.card_format_changed.connect(self.change_job_format)
        layout.addWidget(self.file_list, stretch=1)

        self.progress_summary = ProgressWidget()
        layout.addWidget(self.progress_summary)

        self.controls = ConversionControls()
        self.controls.add_files_clicked.connect(self.open_file_dialog)
        self.controls.reset_section_clicked.connect(self.reset_current_section)
        self.controls.convert_all_clicked.connect(self.start_conversion)
        self.controls.save_all_clicked.connect(self.save_all)
        self.controls.compression_changed.connect(self.update_compression_level)
        layout.addWidget(self.controls)

    def apply_palette_color(self, color: str) -> None:
        """Actualiza el color de acento de la zona de soltar y las tarjetas."""
        self.drop_area.set_icon_color(color)
        self.file_list.set_palette_color(color)

    def reset_current_section(self) -> None:
        self.jobs.clear()
        self.file_list.clear()
        self._update_summary()

    def add_files(self, paths: List[Path]) -> None:
        for p in paths:
            ext = p.suffix.lstrip(".").lower()
            if ext not in self.supported_sources:
                continue

            target = self.supported_targets[0]
            for t in self.supported_targets:
                if t != ext:
                    target = t
                    break

            job = ConversionJob(
                input_path=p,
                source_format=ext,
                target_format=target
            )
            self.jobs.append(job)
            self.file_list.add_card(job, [t.upper() for t in self.supported_targets])

        self._update_summary()

    def open_file_dialog(self) -> None:
        patterns = " ".join(f"*.{e}" for e in self.supported_sources)
        filter_str = f"Archivos ({patterns});;Todos los archivos (*.*)"
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar archivos", "", filter_str)
        if files:
            self.add_files([Path(f) for f in files])

    def delete_job(self, job_id: str) -> None:
        self.jobs = [j for j in self.jobs if j.id != job_id]
        self._update_summary()

    def change_job_format(self, job_id: str, new_format: str) -> None:
        for j in self.jobs:
            if j.id == job_id:
                j.target_format = new_format.lower()
                break

    def update_compression_level(self, level: int) -> None:
        for j in self.jobs:
            j.compression_level = level

    def start_conversion(self) -> None:
        if not self.jobs or (self._worker and self._worker.isRunning()):
            return
        self._worker = ConversionWorker(self.service, self.jobs, self.category)
        self._worker.job_started.connect(
            lambda jid: self.file_list.update_job_progress(jid, JobStatus.CONVERTING, 0)
        )
        self._worker.job_progress.connect(
            lambda jid, p: self.file_list.update_job_progress(jid, JobStatus.CONVERTING, p)
        )
        self._worker.job_completed.connect(
            lambda jid: self.file_list.update_job_progress(jid, JobStatus.COMPLETED, 100)
        )
        self._worker.job_failed.connect(
            lambda jid, err: self.file_list.update_job_progress(jid, JobStatus.ERROR, 0, err)
        )
        self._worker.all_finished.connect(self._update_summary)
        self._worker.start()

    def save_single(self, job_id: str) -> None:
        for j in self.jobs:
            if j.id == job_id and j.temp_output_path and j.temp_output_path.exists():
                out = SaveController.save_single_file(self, j)
                if out:
                    j.output_path = out
                    j.status = JobStatus.SAVED
                    self.file_list.update_job_progress(j.id, JobStatus.SAVED, 100)
                break

    def save_all(self) -> None:
        saved_jobs = SaveController.save_all_files(self, self.jobs)
        for j in saved_jobs:
            self.file_list.update_job_progress(j.id, JobStatus.SAVED, 100)

    def _update_summary(self) -> None:
        completed = sum(1 for j in self.jobs if j.status in (JobStatus.COMPLETED, JobStatus.SAVED))
        self.progress_summary.update_progress(completed, len(self.jobs))
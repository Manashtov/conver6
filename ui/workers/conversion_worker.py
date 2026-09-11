from PySide6.QtCore import QThread, Signal
from core.conversion.conversion_job import ConversionJob, JobStatus
from core.conversion.conversion_service import ConversionService


class ConversionWorker(QThread):
    """Ejecuta trabajos secuencialmente en segundo plano para evitar bloqueos."""
    job_started = Signal(str)
    job_progress = Signal(str, int)
    job_completed = Signal(str)
    job_failed = Signal(str, str)
    all_finished = Signal()

    def __init__(self, service: ConversionService, jobs: list[ConversionJob], category: str) -> None:
        super().__init__()
        self._service = service
        self._jobs = jobs
        self._category = category

    def run(self) -> None:
        for job in self._jobs:
            if job.status == JobStatus.COMPLETED:
                continue

            self.job_started.emit(job.id)
            job.status = JobStatus.CONVERTING

            def on_progress(p: int) -> None:
                job.progress = p
                self.job_progress.emit(job.id, p)

            res = self._service.convert(job, self._category, on_progress)

            if res.success:
                job.temp_output_path = res.output_path
                job.status = JobStatus.COMPLETED
                job.progress = 100
                self.job_completed.emit(job.id)
            else:
                job.status = JobStatus.ERROR
                job.error_message = res.error_message
                self.job_failed.emit(job.id, res.error_message or "Fallo desconocido")

        self.all_finished.emit()
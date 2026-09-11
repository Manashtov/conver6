import shutil
from pathlib import Path
from typing import List, Optional
from PySide6.QtWidgets import QWidget, QFileDialog
from core.conversion.conversion_job import ConversionJob, JobStatus


class SaveController:
    """Coordina el guardado físico de resultados sin alertas emergentes."""

    @staticmethod
    def save_single_file(parent: QWidget, job: ConversionJob) -> Optional[Path]:
        if not job.temp_output_path or not job.temp_output_path.exists():
            return None

        default_name = f"{job.input_path.stem}_convertido.{job.target_format.lower()}"
        dest_path, _ = QFileDialog.getSaveFileName(
            parent, "Guardar archivo", default_name, f"*.{job.target_format.lower()}"
        )

        if dest_path:
            out = Path(dest_path)
            shutil.copyfile(job.temp_output_path, out)
            return out
        return None

    @staticmethod
    def save_all_files(parent: QWidget, jobs: List[ConversionJob]) -> List[ConversionJob]:
        valid_jobs = [j for j in jobs if j.status == JobStatus.COMPLETED and j.temp_output_path]
        if not valid_jobs:
            return []

        folder = QFileDialog.getExistingDirectory(parent, "Seleccionar carpeta de destino")
        if not folder:
            return []

        target_dir = Path(folder)
        saved = []
        for j in valid_jobs:
            dest = target_dir / f"{j.input_path.stem}_convertido.{j.target_format.lower()}"
            shutil.copyfile(j.temp_output_path, dest)
            j.output_path = dest
            j.status = JobStatus.SAVED
            saved.append(j)
        return saved
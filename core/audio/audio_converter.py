import subprocess
import tempfile
from pathlib import Path
from typing import Callable, List, Optional

from core.audio.audio_backend import AudioBackend
from core.conversion.base_converter import BaseConverter
from core.conversion.conversion_job import ConversionJob
from core.conversion.conversion_result import ConversionResult
from core.compression.compression_service import CompressionService
from core.exceptions import DependencyMissingError


class AudioConverter(BaseConverter):
    """Conversor robusto de formatos de audio compatible con Python 3.14+ usando FFmpeg directo."""

    def supported_source_formats(self) -> List[str]:
        return ["MP3", "WAV", "OGG"]

    def supported_target_formats(self) -> List[str]:
        return ["MP3", "WAV", "OGG"]

    def convert(
        self,
        job: ConversionJob,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> ConversionResult:
        try:
            ffmpeg_exec = AudioBackend.get_ffmpeg_executable()

            if progress_callback:
                progress_callback(15)

            tgt = job.target_format.lower()
            temp_dir = Path(tempfile.gettempdir())
            temp_target = temp_dir / f"conver6_{job.id}.{tgt}"

            bitrate = CompressionService.get_audio_bitrate(job.compression_level)

            # Construcción de argumentos seguros para el CLI de FFmpeg
            cmd = [
                ffmpeg_exec,
                "-y",                       # Sobrescribir salida temporal si existe
                "-i", str(job.input_path),  # Archivo origen
            ]

            if tgt == "mp3":
                cmd.extend(["-b:a", bitrate])
            elif tgt == "ogg":
                cmd.extend(["-c:a", "libvorbis", "-b:a", bitrate])
            elif tgt == "wav":
                cmd.extend(["-c:a", "pcm_s16le"])

            cmd.append(str(temp_target))

            if progress_callback:
                progress_callback(40)

            # Ejecución en proceso desacoplado sin mostrar consola de comandos en Windows
            startupinfo = None
            if hasattr(subprocess, "STARTUPINFO"):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo,
                text=True,
                check=False
            )

            if progress_callback:
                progress_callback(85)

            if process.returncode != 0:
                err_snippet = process.stderr.strip().splitlines()[-1] if process.stderr else "Error desconocido"
                return ConversionResult(
                    success=False,
                    error_message=f"FFmpeg falló ({err_snippet})"
                )

            if not temp_target.exists():
                return ConversionResult(
                    success=False,
                    error_message="El archivo de salida de audio no se generó correctamente."
                )

            if progress_callback:
                progress_callback(100)

            return ConversionResult(success=True, output_path=temp_target)

        except DependencyMissingError as dme:
            return ConversionResult(success=False, error_message=str(dme))
        except Exception as err:
            return ConversionResult(success=False, error_message=str(err))
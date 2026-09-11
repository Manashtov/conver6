import io
import tempfile
from pathlib import Path
from typing import Callable, List, Optional
from PIL import Image
from core.conversion.base_converter import BaseConverter
from core.conversion.conversion_job import ConversionJob
from core.conversion.conversion_result import ConversionResult
from core.compression.compression_service import CompressionService
from core.exceptions import ConversionExecutionError


class ImageConverter(BaseConverter):
    """Conversor integral de imágenes con soporte seguro opcional para Cairo."""

    def supported_source_formats(self) -> List[str]:
        return ["SVG", "PNG", "JPG", "JPEG"]

    def supported_target_formats(self) -> List[str]:
        return ["SVG", "PNG", "JPG", "JPEG"]

    def convert(
        self,
        job: ConversionJob,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> ConversionResult:
        try:
            if progress_callback:
                progress_callback(15)

            src = job.source_format.upper()
            tgt = job.target_format.upper()
            temp_dir = Path(tempfile.gettempdir())
            temp_target = temp_dir / f"conver6_{job.id}.{tgt.lower()}"

            if src == "SVG":
                img = self._load_svg(job.input_path)
            else:
                img = Image.open(job.input_path)

            if progress_callback:
                progress_callback(50)

            if tgt in ("JPG", "JPEG") and img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1])
                img = background
            elif tgt == "PNG" and img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")

            if progress_callback:
                progress_callback(75)

            if tgt == "SVG":
                self._save_to_svg(img, temp_target)
            else:
                params = CompressionService.compress_image(img, tgt, job.compression_level)
                save_fmt = "JPEG" if tgt in ("JPG", "JPEG") else tgt
                img.save(temp_target, format=save_fmt, **params)

            img.close()
            if progress_callback:
                progress_callback(100)

            return ConversionResult(success=True, output_path=temp_target)

        except Exception as err:
            return ConversionResult(success=False, error_message=str(err))

    def _load_svg(self, path: Path) -> Image.Image:
        """Carga SVG utilizando CairoSVG sólo si está disponible en el sistema."""
        try:
            import cairosvg
            png_bytes = cairosvg.svg2png(url=str(path))
            return Image.open(io.BytesIO(png_bytes))
        except (ImportError, OSError):
            raise ConversionExecutionError(
                "La conversión de SVG requiere las librerías nativas de Cairo.\n"
                "Para activarlo en Windows, instale las librerías binarias de Cairo."
            )

    def _save_to_svg(self, img: Image.Image, output_path: Path) -> None:
        """Empaqueta los datos raster dentro de un documento SVG estándar."""
        import base64
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64_data = base64.b64encode(buf.getvalue()).decode("ascii")
        svg_content = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{img.width}" height="{img.height}">'
            f'<image width="{img.width}" height="{img.height}" href="data:image/png;base64,{b64_data}"/>'
            f'</svg>'
        )
        output_path.write_text(svg_content, encoding="utf-8")
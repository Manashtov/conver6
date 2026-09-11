from pathlib import Path
from PIL import Image
from core.exceptions import ConversionExecutionError


class CompressionService:
    """Aplica estrategias de reducción y calidad según el tipo de archivo."""

    @staticmethod
    def compress_image(image: Image.Image, format_name: str, level: int) -> dict:
        """Calcula parámetros de guardado de imagen basados en el nivel (60 a 90)."""
        params = {}
        fmt = format_name.upper()
        if fmt in ("JPG", "JPEG"):
            params["quality"] = max(10, min(95, level))
            params["optimize"] = True
        elif fmt == "PNG":
            params["optimize"] = True
            params["compress_level"] = 9 if level <= 70 else 6
        return params

    @staticmethod
    def get_audio_bitrate(level: int) -> str:
        """Determina el bitrate de audio de acuerdo con el nivel porcentual."""
        if level <= 60:
            return "96k"
        elif level <= 70:
            return "128k"
        elif level <= 80:
            return "192k"
        return "320k"

    @staticmethod
    def compress_text_content(content: str, level: int) -> str:
        """Reduce espacios en blanco continuos si se requiere compresión fuerte."""
        if level <= 65:
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            return "\n".join(lines)
        return content
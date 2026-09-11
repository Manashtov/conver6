class Conver6Exception(Exception):
    """Excepción base para errores de Conver6."""
    pass


class DependencyMissingError(Conver6Exception):
    """Lanzada cuando falta un binario o librería del sistema (ej. FFmpeg, Cairo)."""
    pass


class UnsupportedFormatError(Conver6Exception):
    """Lanzada cuando la combinación de formatos no es compatible."""
    pass


class ConversionExecutionError(Conver6Exception):
    """Lanzada cuando el proceso de conversión falla durante la ejecución."""
    pass


class ValidationError(Conver6Exception):
    """Lanzada cuando el archivo de entrada está corrupto o es inválido."""
    pass
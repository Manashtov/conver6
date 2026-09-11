### README.md
```markdown
# Conver6

Conver6 es una aplicación de escritorio modular y moderna para la conversión y compresión de imágenes, audio y documentos, construida sobre PySide6 y Python 3.14.7.

## Características
- **Arquitectura desacoplada**: Menos de 300 líneas por archivo, separación estricta de responsabilidades.
- **Imágenes**: SVG, PNG, JPG, JPEG.
- **Audio**: MP3, WAV, OGG (motor FFmpeg en segundo plano).
- **Documentos**: Conversión cruzada PDF, DOCX y TXT.
- **Compresión adaptativa**: 60%, 65%, 70%, 75%, 80% y 90% configurables.
- **Soporte Drag & Drop**, Workers multi-hilo, Temas Claro/Oscuro y 11 Paletas de acento sin "Azul" (reemplazado por Teal).

## Requisitos Previos
1. Python 3.14.7 instalado.
2. (Opcional recomendado) FFmpeg para conversiones de audio.




# signtool sign /tr [http://timestamp.digicert.com](http://timestamp.digicert.com) /td sha256 /fd sha256 /a #"dist/Conver6/Conver6.exe"
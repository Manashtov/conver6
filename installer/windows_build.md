# Guía de Construcción y Empaquetado para Windows: Conver6

## 1. Generación de Ejecutable Legítimo con PyInstaller
Ejecute en la raíz del proyecto:
```powershell
pyinstaller --noconfirm --onedir --windowed `
    --name "Conver6" `
    --add-data "core;core" `
    --add-data "ui;ui" `
    main.py
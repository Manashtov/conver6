from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QMenu
from PySide6.QtCore import Signal, QSize
import qtawesome as qta


class ConversionControls(QWidget):
    """Barra de acciones con botón de compresión de despliegue directo."""
    add_files_clicked = Signal()
    reset_section_clicked = Signal()
    convert_all_clicked = Signal()
    save_all_clicked = Signal()
    compression_changed = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(12)

        self.btn_add = QPushButton(" Ingresar archivo")
        self.btn_add.setObjectName("GhostBtn")
        self.btn_add.setIcon(qta.icon("fa5s.plus-circle", color="#8C93A8"))
        self.btn_add.setIconSize(QSize(18, 18))
        self.btn_add.clicked.connect(self.add_files_clicked.emit)
        layout.addWidget(self.btn_add)

        # Botón Reiniciar para limpiar solo la sección activa
        self.btn_reset = QPushButton(" Reiniciar")
        self.btn_reset.setObjectName("ResetBtn")
        self.btn_reset.setIcon(qta.icon("fa5s.undo-alt", color="#EF4444"))
        self.btn_reset.setIconSize(QSize(16, 16))
        self.btn_reset.setToolTip("Limpiar todos los archivos de esta sección")
        self.btn_reset.clicked.connect(self.reset_section_clicked.emit)
        layout.addWidget(self.btn_reset)

        layout.addStretch()

        # Botón Redondeado de Compresión con Menú Desplegable
        self.btn_comp = QPushButton("Compresión: 80% ▾")
        self.btn_comp.setObjectName("GhostBtn")
        self.btn_comp.setToolTip("Haz clic para cambiar el nivel objetivo de compresión")

        comp_menu = QMenu(self)
        for pct in ["60%", "65%", "70%", "75%", "80%", "90%"]:
            action = comp_menu.addAction(f"Calidad objetivo {pct}")
            action.triggered.connect(lambda checked=False, p=pct: self._on_select_pct(p))
        self.btn_comp.setMenu(comp_menu)
        layout.addWidget(self.btn_comp)

        self.btn_convert = QPushButton(" Convertir")
        self.btn_convert.setIcon(qta.icon("fa5s.sync-alt", color="white"))
        self.btn_convert.setIconSize(QSize(16, 16))
        self.btn_convert.clicked.connect(self.convert_all_clicked.emit)
        layout.addWidget(self.btn_convert)

        self.btn_save_all = QPushButton(" Guardar todos")
        self.btn_save_all.setObjectName("GhostBtn")
        self.btn_save_all.setIcon(qta.icon("fa5s.check-double", color="#8C93A8"))
        self.btn_save_all.setIconSize(QSize(16, 16))
        self.btn_save_all.clicked.connect(self.save_all_clicked.emit)
        layout.addWidget(self.btn_save_all)

    def _on_select_pct(self, pct: str) -> None:
        self.btn_comp.setText(f"Compresión: {pct} ▾")
        val = int(pct.replace("%", ""))
        self.compression_changed.emit(val)
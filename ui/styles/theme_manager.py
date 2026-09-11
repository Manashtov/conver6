from ui.styles.palettes import PALETTES


class ThemeManager:
    """Generador integral de estilos modernos con alto contraste y bordes redondeados."""

    @classmethod
    def get_stylesheet(cls, is_dark: bool, palette_name: str) -> str:
        colors = PALETTES.get(palette_name, PALETTES["Teal"])
        primary = colors["primary"]
        hover = colors["hover"]

        if is_dark:
            bg_main = "#0F1015"
            bg_side = "#16171F"
            bg_nav_group = "#1C1E26"
            bg_card = "#1C1E26"
            bg_card_hover = "#232631"
            text_main = "#F9FAFB"
            text_muted = "#9CA3AF"
            border_subtle = "#2D313E"
            progress_bg = "#252834"
            combo_bg = "#1C1E26"
            combo_item_hover = "#2A2E3B"
            drop_idle_border = "#374151"
            drop_idle_bg = "rgba(255, 255, 255, 0.02)"
            drop_hover_bg = "rgba(255, 255, 255, 0.05)"
            scrollbar_handle = "#374151"
        else:
            bg_main = "#F4F6F9"
            bg_side = "#FFFFFF"
            bg_nav_group = "#EDF0F5"
            bg_card = "#FFFFFF"
            bg_card_hover = "#F8FAFC"
            text_main = "#111827"
            text_muted = "#4B5563"
            border_subtle = "#D1D5DB"
            progress_bg = "#E5E7EB"
            combo_bg = "#FFFFFF"
            combo_item_hover = "#F3F4F6"
            drop_idle_border = "#9CA3AF"
            drop_idle_bg = "rgba(0, 0, 0, 0.02)"
            drop_hover_bg = "rgba(0, 0, 0, 0.04)"
            scrollbar_handle = "#C5CBD5"

        return f"""
        /* Raíz de la ventana y diálogos */
        QMainWindow, QWidget#centralWidget, QDialog, QDialog#SettingsDialog {{
            background-color: {bg_main};
            color: {text_main};
            font-family: 'Segoe UI', system-ui, sans-serif;
        }}

        /* Todos los textos heredan color con alto contraste */
        QLabel {{
            color: {text_main};
            background: transparent;
        }}

        /* Barra Lateral Izquierda */
        QWidget#Sidebar {{
            background-color: {bg_side};
            border-right: 1.5px solid {border_subtle};
        }}

        #LogoPlaceholder {{
            background-color: {bg_nav_group};
            border: 1.5px dashed {border_subtle};
            border-radius: 10px;
        }}

        #BrandTitle {{
            font-size: 22px;
            font-weight: 800;
            color: {text_main};
            letter-spacing: 0.5px;
        }}

        #SeparatorLine {{
            color: {border_subtle};
            margin: 8px 0;
        }}

        QFrame#NavGroupFrame {{
            background-color: {bg_nav_group};
            border: 1px solid {border_subtle};
            border-radius: 14px;
        }}

        /* Botones de Barra Lateral */
        QPushButton#NavCardBtn, QPushButton#NavBottomBtn {{
            background-color: {bg_card};
            color: {text_main};
            border: 1.5px solid {border_subtle};
            border-radius: 12px;
            text-align: left;
            padding-left: 14px;
            font-weight: 700;
            font-size: 13px;
        }}
        QPushButton#NavCardBtn:hover, QPushButton#NavBottomBtn:hover {{
            border: 1.5px solid {primary};
            background-color: {bg_card_hover};
            color: {primary};
        }}
        QPushButton#NavCardBtn[active="true"] {{
            background-color: {primary};
            color: #FFFFFF;
            border: 1.5px solid {primary};
        }}

        /* Área de Soltar Archivos */
        QFrame#DropArea {{
            border: 2px dashed {drop_idle_border};
            border-radius: 14px;
            background-color: {drop_idle_bg};
        }}
        QFrame#DropArea:hover, QFrame#DropArea[dragActive="true"] {{
            border: 2px dashed {primary};
            background-color: {drop_hover_bg};
        }}
        #DropText {{
            font-size: 13px;
            font-weight: 700;
            color: {text_muted};
        }}

        /* Tarjeta de Archivo */
        QFrame#FileCard {{
            background-color: {bg_card};
            border: 1.5px solid {border_subtle};
            border-radius: 14px;
        }}
        QFrame#FileCard:hover {{
            border: 1.5px solid {primary};
            background-color: {bg_card_hover};
        }}
        #CardTitle {{
            font-size: 14px;
            font-weight: 700;
            color: {text_main};
        }}

        /* Estados dinámicos */
        #StatusPending {{
            font-size: 13px;
            font-weight: 700;
            color: {text_muted};
        }}
        #StatusCompleted {{
            font-size: 13px;
            font-weight: 800;
            color: {primary};
        }}
        #StatusSaved {{
            font-size: 13px;
            font-weight: 800;
            color: #10B981;
        }}
        #StatusError {{
            font-size: 13px;
            font-weight: 700;
            color: #EF4444;
        }}

        /* Barras de Progreso Reales y Visibles */
        QProgressBar {{
            background-color: {progress_bg};
            border: 1px solid {border_subtle};
            border-radius: 6px;
            min-height: 12px;
            max-height: 12px;
            text-align: center;
        }}
        QProgressBar::chunk {{
            background-color: {primary};
            border-radius: 5px;
        }}

        /* Botón Guardar en Tarjeta */
        QPushButton#CardSaveBtn {{
            background-color: {bg_card};
            border: 1.5px solid {border_subtle};
            border-radius: 10px;
        }}
        QPushButton#CardSaveBtn:hover {{
            border: 1.5px solid {primary};
            background-color: {bg_card_hover};
        }}
        QPushButton#CardSaveBtn:enabled {{
            border: 1.5px solid {primary};
            background-color: {bg_card_hover};
        }}
        QPushButton#CardSaveBtn:enabled:hover {{
            background-color: {primary};
        }}

        /* Botón Eliminar en Tarjeta */
        QPushButton#CardDeleteBtn {{
            background-color: {'#2A1D20' if is_dark else '#FEE2E2'};
            border: 1.5px solid {'#4A252A' if is_dark else '#FECACA'};
            border-radius: 10px;
        }}
        QPushButton#CardDeleteBtn:hover {{
            background-color: #EF4444;
            border: 1.5px solid #DC2626;
        }}

        /* Menús Desplegables y Lista Flotante */
        QComboBox {{
            background-color: {combo_bg};
            color: {text_main};
            border: 1.5px solid {border_subtle};
            border-radius: 10px;
            padding: 6px 12px;
            font-weight: 700;
            font-size: 13px;
        }}
        QComboBox:hover, QComboBox:focus {{
            border: 1.5px solid {primary};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        QComboBox QAbstractItemView, QListView {{
            background-color: {combo_bg};
            color: {text_main};
            border: 1.5px solid {border_subtle};
            border-radius: 10px;
            selection-background-color: {primary};
            selection-color: #FFFFFF;
            padding: 6px;
            outline: 0px;
        }}
        QComboBox QAbstractItemView::item, QListView::item {{
            height: 32px;
            border-radius: 6px;
            color: {text_main};
            padding-left: 8px;
        }}
        QComboBox QAbstractItemView::item:hover, QListView::item:hover {{
            background-color: {combo_item_hover};
            color: {primary};
        }}
        QComboBox QAbstractItemView::item:selected, QListView::item:selected {{
            background-color: {primary};
            color: #FFFFFF;
        }}

        /* Menú de Compresión y Popup */
        QMenu {{
            background-color: {combo_bg};
            color: {text_main};
            border: 1.5px solid {border_subtle};
            border-radius: 10px;
            padding: 6px;
        }}
        QMenu::item {{
            padding: 8px 24px 8px 16px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 13px;
            color: {text_main};
        }}
        QMenu::item:selected {{
            background-color: {primary};
            color: #FFFFFF;
        }}

        /* Botón Reiniciar */
        QPushButton#ResetBtn {{
            background-color: {'#2A1D20' if is_dark else '#FEE2E2'};
            color: #EF4444;
            border: 1.5px solid {'#4A252A' if is_dark else '#FECACA'};
            border-radius: 10px;
            padding: 9px 16px;
            font-weight: 700;
        }}
        QPushButton#ResetBtn:hover {{
            background-color: #EF4444;
            color: #FFFFFF;
            border: 1.5px solid #DC2626;
        }}

        /* Botones de Acción */
        QPushButton {{
            background-color: {primary};
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            padding: 10px 18px;
            font-weight: 700;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}
        QPushButton#GhostBtn {{
            background-color: {bg_card};
            color: {text_main};
            border: 1.5px solid {border_subtle};
            border-radius: 10px;
            padding: 9px 16px;
            font-weight: 700;
        }}
        QPushButton#GhostBtn:hover {{
            border: 1.5px solid {primary};
            color: {primary};
            background-color: {bg_card_hover};
        }}

        /* Input de texto en configuración */
        QLineEdit {{
            background-color: {combo_bg};
            color: {text_main};
            border: 1.5px solid {border_subtle};
            border-radius: 10px;
            padding: 6px 12px;
            font-weight: 600;
            font-size: 13px;
        }}
        QLineEdit:focus {{
            border: 1.5px solid {primary};
        }}

        /* Barra de Scroll estilizada, delgada y redondeada */
        QScrollBar:vertical {{
            background-color: transparent;
            width: 10px;
            margin: 4px 2px 4px 2px;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {scrollbar_handle};
            min-height: 35px;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {primary};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
            border: none;
        }}
        """
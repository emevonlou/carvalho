import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)

from PySide6.QtCore import Qt

from modules.compras import ComprasWidget


class CarvalhoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carvalho")
        self.setMinimumSize(620, 640)

        self.setStyleSheet("""
            QWidget {
                background-color: #F5F1E8;
                color: #3D2B1F;
                font-family: Arial;
            }

            QFrame#cardPrincipal {
                background-color: #FFFDF7;
                border: 2px solid #8A6A4F;
                border-radius: 22px;
            }

            QLabel#titulo {
                font-size: 38px;
                font-weight: bold;
                color: #3D2B1F;
            }

            QLabel#subtitulo {
                font-size: 17px;
                color: #5E7A4D;
            }

            QLabel#versiculo {
                font-size: 14px;
                color: #6B4F3A;
                padding: 8px;
                border-top: 1px solid #D8C7B2;
                border-bottom: 1px solid #D8C7B2;
            }

            QLabel#categorias {
                font-size: 19px;
                color: #3D2B1F;
                line-height: 1.6;
                padding: 12px;
                background-color: #F8F3EA;
                border: 1px solid #D8C7B2;
                border-radius: 14px;
            }

            QPushButton {
                background-color: #5E7A4D;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #4B5D3F;
                border-radius: 14px;
                padding: 10px;
            }

            QPushButton:hover {
                background-color: #6F8B5D;
            }

            QPushButton:pressed {
                background-color: #4B5D3F;
            }
        """)

        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("cardPrincipal")
        card.setMinimumWidth(500)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(18)
        layout.setContentsMargins(34, 34, 34, 34)

        title = QLabel("Carvalho")
        title.setObjectName("titulo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Raízes fortes. Frutos duradouros.")
        subtitle.setObjectName("subtitulo")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        verse = QLabel(
            "“Carvalhos de justiça, plantio do Senhor.”\n"
            "Isaías 61:3"
        )
        verse.setObjectName("versiculo")
        verse.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_compras = QPushButton("Compras")
        btn_cardapio = QPushButton("Cardápio")
        btn_financas = QPushButton("Finanças")
        btn_feira = QPushButton("Feira")

        btn_compras.clicked.connect(self.abrir_compras)

        for btn in [
            btn_compras,
            btn_cardapio,
            btn_financas,
            btn_feira,
        ]:
            btn.setMinimumHeight(46)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(verse)
        layout.addSpacing(4)
        layout.addWidget(btn_compras)
        layout.addWidget(btn_cardapio)
        layout.addWidget(btn_financas)
        layout.addWidget(btn_feira)

        card.setLayout(layout)
        root_layout.addWidget(card)

        self.setLayout(root_layout)

    def abrir_compras(self):
        self.compras_window = ComprasWidget()
        self.compras_window.resize(760, 540)
        self.compras_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = CarvalhoApp()
    window.show()

    sys.exit(app.exec())

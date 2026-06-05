import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt


class CarvalhoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carvalho")
        self.setMinimumSize(520, 520)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)

        title = QLabel("🌳 Carvalho")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 34px; font-weight: bold;")

        subtitle = QLabel("Raízes fortes. Frutos duradouros.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #555;")

        verse = QLabel("“Carvalhos de justiça, plantio do Senhor.”\nIsaías 61:3")
        verse.setAlignment(Qt.AlignmentFlag.AlignCenter)
        verse.setStyleSheet("font-size: 14px; color: #6b4f2a;")

        categories = QLabel("👨 Adultos\n💙 Nosso Adolescente\n🐱 Pets\n🏠 Casa")
        categories.setAlignment(Qt.AlignmentFlag.AlignCenter)
        categories.setStyleSheet("font-size: 20px; line-height: 1.6;")

        btn_compras = QPushButton("🛒 Compras")
        btn_cardapio = QPushButton("🍽️ Cardápio")
        btn_financas = QPushButton("💰 Finanças")
        btn_feira = QPushButton("🌽 Feira")

        for btn in [btn_compras, btn_cardapio, btn_financas, btn_feira]:
            btn.setMinimumHeight(42)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    border-radius: 10px;
                    padding: 8px;
                }
            """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(verse)
        layout.addSpacing(10)
        layout.addWidget(categories)
        layout.addSpacing(10)
        layout.addWidget(btn_compras)
        layout.addWidget(btn_cardapio)
        layout.addWidget(btn_financas)
        layout.addWidget(btn_feira)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarvalhoApp()
    window.show()
    sys.exit(app.exec())

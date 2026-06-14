import json
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QListWidget,
    QListWidgetItem,
)

from PySide6.QtCore import Qt


ARQUIVO_COMPRAS = Path("database/compras.json")


class ComprasWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carvalho - Compras")
        self.itens = []

        self.setStyleSheet("""
            QWidget {
                background-color: #F5F1E8;
                color: #3D2B1F;
                font-family: Arial;
            }

            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #3D2B1F;
            }

            QLineEdit, QComboBox {
                background-color: #FFFDF7;
                border: 2px solid #D8C7B2;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }

            QListWidget {
                background-color: #FFFDF7;
                border: 2px solid #8A6A4F;
                border-radius: 16px;
                padding: 8px;
                font-size: 14px;
             }

             QCheckBox {
                 font-size: 14px;
             }

             QPushButton {
                 background-color: #5E7A4D;
                 color: white;
                 font-size: 14px;
                 font-weight: bold;
                 border: 2px solid #4B5D3F;
                 border-radius: 10px;
                 padding: 8px;
             }

             QPushButton:hover {
                 background-color: #6F8B5D;
             }

             QPushButton:pressed {
                 background-color: #4B5D3F;
             }
         """)

        layout = QVBoxLayout()

        titulo = QLabel("Lista de Compras")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout = QHBoxLayout()

        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("Digite um item...")

        self.valor_input = QLineEdit()
        self.valor_input.setPlaceholderText("Valor (ex: 12.50)")

        self.categoria_input = QComboBox()
        self.categoria_input.addItems(
            [
                "Adultos",
                "Nosso Adolescente",
                "Pets",
                "Casa",
            ]
        )

        self.add_button = QPushButton("Adicionar")
        self.add_button.clicked.connect(self.adicionar_item)

        form_layout.addWidget(self.item_input)
        form_layout.addWidget(self.valor_input)
        form_layout.addWidget(self.categoria_input)
        form_layout.addWidget(self.add_button)

        self.lista = QListWidget()

        layout.addWidget(titulo)
        layout.addLayout(form_layout)
        layout.addWidget(self.lista)

        self.setLayout(layout)

        self.carregar_itens()
        self.atualizar_lista()

    def carregar_itens(self):
        ARQUIVO_COMPRAS.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not ARQUIVO_COMPRAS.exists():
            self.itens = []
            self.salvar_itens()
            return

        try:
            with ARQUIVO_COMPRAS.open(
                "r",
                encoding="utf-8",
            ) as arquivo:
                self.itens = json.load(arquivo)

        except (
            json.JSONDecodeError,
            OSError,
        ):
            self.itens = []

    def salvar_itens(self):
        with ARQUIVO_COMPRAS.open(
            "w",
            encoding="utf-8",
        ) as arquivo:
            json.dump(
                self.itens,
                arquivo,
                ensure_ascii=False,
                indent=2,
            )

    def adicionar_item(self):
        nome = self.item_input.text().strip()
        valor_texto = self.valor_input.text().strip()

        if not nome:
            return

        try:
            valor = float(
                valor_texto.replace(",", ".")
            )
        except ValueError:
            valor = 0.0

        categoria = (
            self.categoria_input.currentText()
        )

        self.itens.append(
            {
                "nome": nome,
                "categoria": categoria,
                "valor": valor,
                "comprado": False,
            }
        )

        self.salvar_itens()
        self.atualizar_lista()

        self.item_input.clear()
        self.valor_input.clear()


    def atualizar_lista(self):
        self.lista.clear()

        categorias = [
            "Adultos",
            "Nosso Adolescente",
            "Pets",
            "Casa",
        ]

        pendentes = [
            (i, item)
            for i, item in enumerate(self.itens)
            if not item["comprado"]
        ]

        comprados = [
            (i, item)
            for i, item in enumerate(self.itens)
            if item["comprado"]
        ]

        if pendentes:
            self.lista.addItem("PENDENTES")

            for categoria in categorias:
                itens_categoria = [
                    (i, item)
                    for i, item in pendentes
                    if item["categoria"] == categoria
                ]

                if itens_categoria:
                    self.lista.addItem(
                        f"  {categoria}"
                    )

                    for i, item in itens_categoria:
                        self.adicionar_checkbox(
                            i,
                            item,
                        )

        if comprados:
            self.lista.addItem("")

            self.lista.addItem(
                "COMPRADOS"
            )

            for categoria in categorias:
                itens_categoria = [
                    (i, item)
                    for i, item in comprados
                    if item["categoria"] == categoria
                ]

                if itens_categoria:
                    self.lista.addItem(
                        f"  {categoria}"
                    )

                    for i, item in itens_categoria:
                        self.adicionar_checkbox(
                            i,
                            item,
                        )

    def adicionar_checkbox(
        self,
        indice,
        item,
    ):
        valor = item.get("valor", 0.0)

        texto = (
            f"{item['nome']} | "
            f"R$ {valor:.2f} | "
            f"{item['categoria']}"
        )

        widget = QWidget()

        layout = QHBoxLayout()
        layout.setContentsMargins(
            4,
            4,
            4,
            4,
        )

        checkbox = QCheckBox(texto)

        checkbox.setChecked(
            item["comprado"]
        )

        checkbox.stateChanged.connect(
            lambda estado,
            i=indice: self.marcar_comprado(
                i,
                estado,
            )
        )

        remover_button = QPushButton("Remover")

        remover_button.clicked.connect(
            lambda _, i=indice: self.remover_por_indice(i)
        )

        layout.addWidget(checkbox)
        layout.addWidget(remover_button)

        widget.setLayout(layout)

        item_lista = QListWidgetItem()
        
        item_lista.setData(Qt.ItemDataRole.UserRole, indice)

        item_lista.setSizeHint(
            widget.sizeHint()
        )

        self.lista.addItem(item_lista)

        self.lista.setItemWidget(
            item_lista,
            widget,
        )

    def marcar_comprado(
        self,
        indice,
        estado,
    ):
        self.itens[indice][
            "comprado"
        ] = (
            estado
            == Qt.CheckState.Checked.value
        )

        self.salvar_itens()
        self.atualizar_lista()

    def remover_por_indice(self, indice):
        if 0 <= indice < len(self.itens):
            self.itens.pop(indice)

            self.salvar_itens()
            self.atualizar_lista()

    def remover_item(self):
        linha = self.lista.currentRow()

        if linha < 0:
            return

        item_lista = self.lista.item(linha)

        if item_lista is None:
            return

        indice = item_lista.data(Qt.ItemDataRole.UserRole)

        if indice is None:
            return

        self.itens.pop(indice)

        self.salvar_itens()
        self.atualizar_lista()

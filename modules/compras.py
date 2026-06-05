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

        layout = QVBoxLayout()

        titulo = QLabel("Lista de Compras")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout = QHBoxLayout()

        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("Digite um item...")

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
        form_layout.addWidget(self.categoria_input)
        form_layout.addWidget(self.add_button)

        self.lista = QListWidget()

        self.remover_button = QPushButton(
            "Remover item selecionado"
        )
        self.remover_button.clicked.connect(
            self.remover_item
        )

        layout.addWidget(titulo)
        layout.addLayout(form_layout)
        layout.addWidget(self.lista)
        layout.addWidget(self.remover_button)

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

        if not nome:
            return

        categoria = (
            self.categoria_input.currentText()
        )

        self.itens.append(
            {
                "nome": nome,
                "categoria": categoria,
                "comprado": False,
            }
        )

        self.salvar_itens()
        self.atualizar_lista()

        self.item_input.clear()

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
        texto = (
            f"{item['nome']} - "
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

        layout.addWidget(checkbox)

        widget.setLayout(layout)

        item_lista = QListWidgetItem()

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

    def remover_item(self):
        linha = self.lista.currentRow()

        if linha < 0:
            return

        item = self.lista.item(linha)

        if not item:
            return

        widget = self.lista.itemWidget(item)

        if widget is None:
            return

        texto = (
            widget.layout()
            .itemAt(0)
            .widget()
            .text()
        )

        nome = texto.split(" - ")[0]

        self.itens = [
            item
            for item in self.itens
            if item["nome"] != nome
        ]

        self.salvar_itens()
        self.atualizar_lista()

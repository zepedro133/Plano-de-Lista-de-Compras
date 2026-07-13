from __future__ import annotations

class Produto:
    def __init__(self, nome: str, preco: float):
        self.nome = str(nome)
        self.preco = float(preco)


class ItemLista:
    def __init__(self, produto: Produto, quantidade: int):
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("A quantidade tem de ser maior que zero.")
        self.produto = produto
        self.quantidade = quantidade

    def total(self) -> float:
        return self.produto.preco * self.quantidade


class ListaCompras:
    def __init__(self):
        self.itens: list[ItemLista] = []

    def adicionar_item(self, item: ItemLista) -> None:
        self.itens.append(item)

    def remover_indice(self, idx: int) -> None:
        del self.itens[idx]

    def limpar(self) -> None:
        self.itens.clear()

    def total(self) -> float:
        return sum(i.total() for i in self.itens)

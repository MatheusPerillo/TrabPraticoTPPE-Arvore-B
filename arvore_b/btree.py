from arvore_b.bnode import BNode
from arvore_b.exceptions import ChaveNaoEncontradaException


class BTree:
    def __init__(self, t: int):
        self.raiz = BNode(True)
        self.t = t

    def buscar(self, chave: int):
        return self.raiz.buscar(chave)

    def inserir(self, chave: int):
        r = self.raiz
        if len(r.chaves) == 2 * self.t - 1:
            s = BNode(False)
            s.filhos.append(r)
            s.dividir_filho(0, self.t)
            self.raiz = s
        self.raiz.inserir_nao_cheio(chave, self.t)

    def remover(self, chave: int):
        if not self.raiz:
            raise ChaveNaoEncontradaException("Árvore vazia")

        self.raiz.remover(chave, self.t)

        if not self.raiz.chaves and not self.raiz.folha:
            self.raiz = self.raiz.filhos[0]

    def __str__(self):
        return str(self.raiz)

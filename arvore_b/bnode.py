from typing import Tuple


class BNode:
    def __init__(self, t: int, folha: bool):
        self.t = t
        self.folha = folha
        self._chaves = []
        self._filhos = []

    @property
    def chaves(self):
        return self._chaves

    @chaves.setter
    def chaves(self, valor):
        self._chaves = valor

    @property
    def filhos(self):
        return self._filhos

    @filhos.setter
    def filhos(self, valor):
        self._filhos = valor

    def inserir_chave(self, chave: int):
        if not self.folha:
            raise Exception("Inserção direta de chave só em folhas")
        i = len(self._chaves) - 1
        self._chaves.append(None)
        while i >= 0 and self._chaves[i] > chave:
            self._chaves[i + 1] = self._chaves[i]
            i -= 1
        self._chaves[i + 1] = chave

    def adicionar_filho(self, filho: "BNode", pos: int = None):
        if pos is None:
            self._filhos.append(filho)
        else:
            self._filhos.insert(pos, filho)

    def dividir(self) -> Tuple[int, "BNode"]:
        meio = self.t - 1
        chave_meio = self._chaves[meio]

        novo_no = BNode(self.t, self.folha)
        novo_no.chaves = self._chaves[meio + 1:]
        self._chaves = self._chaves[:meio]

        if not self.folha:
            novo_no.filhos = self._filhos[self.t:]
            self._filhos = self._filhos[:self.t]

        return chave_meio, novo_no

    def pegar_predecessor(self) -> int:
        atual = self
        while not atual.folha:
            atual = atual.filhos[-1]
        return atual.chaves[-1]

    def pegar_sucessor(self) -> int:
        atual = self
        while not atual.folha:
            atual = atual.filhos[0]
        return atual.chaves[0]
    

    def __repr__(self):
        tipo = "Folha" if self.folha else "Interno"
        return f"{tipo}: {self._chaves}"
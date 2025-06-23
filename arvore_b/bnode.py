from typing import List, Optional
from arvore_b.exceptions import (
    ChaveNaoEncontradaException
)


class BNode:
    def __init__(self, folha: bool):
        self.folha = folha
        self.chaves: List[int] = []
        self.filhos: List[BNode] = []

    def buscar(self, chave: int) -> Optional[BNode]:
        i = 0
        while i < len(self.chaves) and chave > self.chaves[i]:
            i += 1
        if i < len(self.chaves) and chave == self.chaves[i]:
            return self
        if self.folha:
            return None
        return self.filhos[i].buscar(chave)

    def dividir_filho(self, i: int, t: int):
        y = self.filhos[i]
        z = BNode(y.folha)
        z.chaves = y.chaves[t:]
        y.chaves = y.chaves[:t - 1]

        if not y.folha:
            z.filhos = y.filhos[t:]
            y.filhos = y.filhos[:t]

        self.filhos.insert(i + 1, z)
        self.chaves.insert(i, y.chaves.pop())

    def inserir_nao_cheio(self, chave: int, t: int):
        i = len(self.chaves) - 1
        if self.folha:
            self.chaves.append(0)
            while i >= 0 and chave < self.chaves[i]:
                self.chaves[i + 1] = self.chaves[i]
                i -= 1
            self.chaves[i + 1] = chave
        else:
            while i >= 0 and chave < self.chaves[i]:
                i -= 1
            i += 1
            if len(self.filhos[i].chaves) == 2 * t - 1:
                self.dividir_filho(i, t)
                if chave > self.chaves[i]:
                    i += 1
            self.filhos[i].inserir_nao_cheio(chave, t)

    def fundir_com(self, i: int, t: int):
        filho = self.filhos[i]
        irmao = self.filhos[i + 1]
        chave_do_meio = self.chaves.pop(i)

        filho.chaves.append(chave_do_meio)
        filho.chaves.extend(irmao.chaves)

        if not filho.folha:
            filho.filhos.extend(irmao.filhos)

        self.filhos.pop(i + 1)

    def remover(self, chave: int, t: int):
        i = 0
        while i < len(self.chaves) and chave > self.chaves[i]:
            i += 1

        if i < len(self.chaves) and self.chaves[i] == chave:
            if self.folha:
                self.chaves.pop(i)
            else:
                self.remover_interno(i, t)
        else:
            if self.folha:
                raise ChaveNaoEncontradaException(f"Chave {chave} não encontrada.")

            precisa_ajustar = len(self.filhos[i].chaves) < t
            if precisa_ajustar:
                self.ajustar_filhos(i, t)

            self.filhos[i].remover(chave, t)

    def remover_interno(self, i: int, t: int):
        chave = self.chaves[i]
        if len(self.filhos[i].chaves) >= t:
            pred = self.get_predecessor(i)
            self.chaves[i] = pred
            self.filhos[i].remover(pred, t)
        elif len(self.filhos[i + 1].chaves) >= t:
            succ = self.get_sucessor(i)
            self.chaves[i] = succ
            self.filhos[i + 1].remover(succ, t)
        else:
            self.fundir_com(i, t)
            self.filhos[i].remover(chave, t)

    def ajustar_filhos(self, i: int, t: int):
        if i > 0 and len(self.filhos[i - 1].chaves) >= t:
            self.emprestar_do_irmao_esquerdo(i)
        elif i < len(self.filhos) - 1 and len(self.filhos[i + 1].chaves) >= t:
            self.emprestar_do_irmao_direito(i)
        else:
            if i < len(self.filhos) - 1:
                self.fundir_com(i, t)
            else:
                self.fundir_com(i - 1, t)

    def emprestar_do_irmao_esquerdo(self, i: int):
        filho = self.filhos[i]
        irmao = self.filhos[i - 1]

        filho.chaves.insert(0, self.chaves[i - 1])
        self.chaves[i - 1] = irmao.chaves.pop()

        if not irmao.folha:
            filho.filhos.insert(0, irmao.filhos.pop())

    def emprestar_do_irmao_direito(self, i: int):
        filho = self.filhos[i]
        irmao = self.filhos[i + 1]

        filho.chaves.append(self.chaves[i])
        self.chaves[i] = irmao.chaves.pop(0)

        if not irmao.folha:
            filho.filhos.append(irmao.filhos.pop(0))

    def get_predecessor(self, i: int) -> int:
        atual = self.filhos[i]
        while not atual.folha:
            atual = atual.filhos[-1]
        return atual.chaves[-1]

    def get_sucessor(self, i: int) -> int:
        atual = self.filhos[i + 1]
        while not atual.folha:
            atual = atual.filhos[0]
        return atual.chaves[0]

    def __str__(self, nivel=0) -> str:
        tipo = "Folha" if self.folha else "Interno"
        result = "   " * nivel + f"{tipo}: {self.chaves}\n"
        for filho in self.filhos:
            result += filho.__str__(nivel + 1)
        return result

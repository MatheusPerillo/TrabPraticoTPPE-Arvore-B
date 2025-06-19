from .bnode import BNode
from .contratos import verificar_invariantes

class BTree:
    def __init__(self, t: int):
        self.t = t
        self.raiz = BNode(t, folha=True)
        self.altura = 1

    def buscar(self, chave: int):
        return self._buscar(self.raiz, chave)

    def _buscar(self, no: BNode, chave: int):
        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1
        if i < len(no.chaves) and chave == no.chaves[i]:
            return True
        elif no.folha:
            return False
        else:
            return self._buscar(no.filhos[i], chave)

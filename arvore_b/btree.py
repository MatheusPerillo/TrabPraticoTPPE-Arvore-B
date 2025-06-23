from .bnode import BNode
import icontract
from .contratos import verificar_invariantes

@icontract.invariant(
    lambda self: all(no.chaves == sorted(no.chaves) for no in self._todos_nos()),
    "Todas as chaves nos nós estão ordenadas"
)
@icontract.invariant(
    lambda self: all(
        len(no.chaves) >= self.t - 1 or no is self.raiz
        for no in self._todos_nos() if not no.folha
    ),
    "Cada nó interno possui no mínimo t-1 chaves (exceto raiz)"
)
@icontract.invariant(
    lambda self: all(len(no.chaves) <= 2 * self.t - 1 for no in self._todos_nos()),
    "Cada nó possui no máximo 2t-1 chaves"
)
@icontract.invariant(
    lambda self: self._verificar_niveis_folhas(),
    "Todos os nós folhas estão no mesmo nível"
)
class BTree:
    def __init__(self, t: int):
        self.t = t
        self.raiz = BNode(t, folha=True)
        self.altura = 1

    def _todos_nos(self):
        nos = []
        fila = [self.raiz]
        while fila:
            no = fila.pop()
            nos.append(no)
            if not no.folha:
                fila.extend(no.filhos)
        return nos

    def _verificar_niveis_folhas(self):
        def profundidade(no):
            d = 0
            while not no.folha:
                no = no.filhos[0]
                d += 1
            return d

        nivel = profundidade(self.raiz)

        def verificar(no, nivel_atual):
            if no.folha:
                return nivel_atual == nivel
            return all(verificar(filho, nivel_atual + 1) for filho in no.filhos)

        return verificar(self.raiz, 0)

    def buscar(self, chave: int) -> bool:
        return self._buscar(self.raiz, chave)

    def _buscar(self, no: BNode, chave: int) -> bool:
        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1
        if i < len(no.chaves) and chave == no.chaves[i]:
            return True
        elif no.folha:
            return False
        else:
            return self._buscar(no.filhos[i], chave)

    @icontract.require(
        lambda self, chave: not self.buscar(chave),
        "A chave a ser inserida não pode existir na árvore"
    )
    def inserir(self, chave: int):
        if len(self.raiz.chaves) == 2 * self.t - 1:
            nova_raiz = BNode(self.t, folha=False)
            nova_raiz.filhos.append(self.raiz)
            self._dividir_filhos(nova_raiz, 0)
            self.raiz = nova_raiz
            self.altura += 1
        self._inserir_nao_cheio(self.raiz, chave)
        verificar_invariantes(self)

    def _inserir_nao_cheio(self, no: BNode, chave: int):
        if no.folha:
            no.inserir_chave(chave)
        else:
            i = len(no.chaves) - 1
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            i += 1
            if len(no.filhos[i].chaves) == 2 * self.t - 1:
                self._dividir_filhos(no, i)
                if chave > no.chaves[i]:
                    i += 1
            self._inserir_nao_cheio(no.filhos[i], chave)

    def _dividir_filhos(self, pai: BNode, indice: int):
        chave_meio, novo_no = pai.filhos[indice].dividir()

        pai.chaves.insert(indice, chave_meio)
        pai.filhos.insert(indice + 1, novo_no)

    def imprimir(self, no=None, nivel=0):
        if no is None:
            no = self.raiz
        print("   " * nivel + str(no))
        if not no.folha:
            for filho in no.filhos:
                self.imprimir(filho, nivel + 1)

    @icontract.require(
        lambda self, chave: self.buscar(chave),
        "A chave a ser removida deve existir na árvore"
    )
    @icontract.ensure(
        lambda self, chave: not self.buscar(chave),
        "Após remoção, a chave não pode existir na árvore"
    )
    def remover(self, chave: int):
        self._remover(self.raiz, chave)
        if len(self.raiz.chaves) == 0 and not self.raiz.folha:
            self.raiz = self.raiz.filhos[0]
            self.altura -= 1
        verificar_invariantes(self)

    def _remover(self, no: BNode, chave: int):
        t = self.t
        idx = self._encontrar_indice(no, chave)

        if idx < len(no.chaves) and no.chaves[idx] == chave:
            if no.folha:
                no.chaves.pop(idx)
                return
            else:
                if len(no.filhos[idx].chaves) >= t:
                    pred = no.filhos[idx].pegar_predecessor()
                    no.chaves[idx] = pred
                    self._remover(no.filhos[idx], pred)
                elif len(no.filhos[idx + 1].chaves) >= t:
                    succ = no.filhos[idx + 1].pegar_sucessor()
                    no.chaves[idx] = succ
                    self._remover(no.filhos[idx + 1], succ)
                else:
                    self._fundir(no, idx)
                    self._remover(no.filhos[idx], chave)
        else:
            if no.folha:
                return
            if len(no.filhos[idx].chaves) == t - 1:
                if idx > 0 and len(no.filhos[idx - 1].chaves) >= t:
                    self._pegar_do_irmao_esquerdo(no, idx)
                elif idx < len(no.filhos) - 1 and len(no.filhos[idx + 1].chaves) >= t:
                    self._pegar_do_irmao_direito(no, idx)
                else:
                    if idx < len(no.filhos) - 1:
                        self._fundir(no, idx)
                    else:
                        self._fundir(no, idx - 1)
                    if idx > len(no.chaves):
                        idx -= 1
            self._remover(no.filhos[idx], chave)

    def _encontrar_indice(self, no: BNode, chave: int) -> int:
        idx = 0
        while idx < len(no.chaves) and chave > no.chaves[idx]:
            idx += 1
        return idx

    def _fundir(self, no: BNode, idx: int):
        filho = no.filhos[idx]
        irmao = no.filhos[idx + 1]
        chave_meio = no.chaves.pop(idx)

        filho.chaves.append(chave_meio)
        filho.chaves.extend(irmao.chaves)

        if not filho.folha:
            filho.filhos.extend(irmao.filhos)

        no.filhos.pop(idx + 1)

    def _pegar_do_irmao_esquerdo(self, no: BNode, idx: int):
        filho = no.filhos[idx]
        irmao = no.filhos[idx - 1]

        filho.chaves.insert(0, no.chaves[idx - 1])
        no.chaves[idx - 1] = irmao.chaves.pop(-1)

        if not irmao.folha:
            filho.filhos.insert(0, irmao.filhos.pop(-1))

    def _pegar_do_irmao_direito(self, no: BNode, idx: int):
        filho = no.filhos[idx]
        irmao = no.filhos[idx + 1]

        filho.chaves.append(no.chaves[idx])
        no.chaves[idx] = irmao.chaves.pop(0)

        if not irmao.folha:
            filho.filhos.append(irmao.filhos.pop(0))
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .btree import BTree


# --- Pré-condições --- #

def pre_inserir(tree: 'BTree', chave: int) -> bool:
    return not tree.buscar(chave)

def pre_remover(tree: 'BTree', chave: int) -> bool:
    return tree.buscar(chave)

# --- Pós-condições --- #

def pos_remover(tree: 'BTree', chave: int) -> bool:
    return not tree.buscar(chave)

def pos_raiz_chaves(tree: 'BTree') -> bool:
    raiz = tree.raiz
    return 1 <= len(raiz.chaves) <= 2 * tree.t - 1

def pos_no_interno_chaves(tree: 'BTree') -> bool:
    for no in tree._todos_nos():
        if no is not tree.raiz and not no.folha:
            if not (tree.t - 1 <= len(no.chaves) <= 2 * tree.t - 1):
                return False
    return True

def pos_raiz_filhos(tree: 'BTree') -> bool:
    raiz = tree.raiz
    return 2 <= len(raiz.filhos) <= 2 * tree.t


def pos_no_interno_filhos(tree: 'BTree') -> bool:
    for no in tree._todos_nos():
        if no is not tree.raiz and not no.folha:
            if not (tree.t <= len(no.filhos) <= 2 * tree.t):
                return False
    return True


# --- Invariantes Manuais --- #

def verificar_invariantes(tree: 'BTree') -> None:
    assert all(no.chaves == sorted(no.chaves) for no in tree._todos_nos()), \
        "Erro: As chaves dos nós não estão ordenadas"

    assert all(
        (len(no.chaves) >= tree.t - 1 or no is tree.raiz)
        for no in tree._todos_nos() if not no.folha
    ), "Erro: Nós internos (exceto raiz) com menos de t-1 chaves"

    assert all(
        len(no.chaves) <= 2 * tree.t - 1 for no in tree._todos_nos()
    ), "Erro: Nó com mais do que 2t-1 chaves"

    assert tree._verificar_niveis_folhas(), \
        "Erro: Nem todos os nós folhas estão no mesmo nível"
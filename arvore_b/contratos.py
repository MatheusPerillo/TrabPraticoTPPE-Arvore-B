from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .btree import BTree


# --- Pré-condições --- #

def pre_inserir(tree: 'BTree', chave: int) -> bool:
    """Pré-condição: A chave a ser inserida não pode existir na árvore."""
    return not tree.buscar(chave)


def pre_remover(tree: 'BTree', chave: int) -> bool:
    """Pré-condição: A chave a ser removida deve existir na árvore."""
    return tree.buscar(chave)


# --- Pós-condições --- #

def pos_remover(tree: 'BTree', chave: int) -> bool:
    """Pós-condição: Após remover, a chave não deve mais existir na árvore."""
    return not tree.buscar(chave)


def pos_raiz_chaves(tree: 'BTree') -> bool:
    """Pós-condição: Para o nó raiz, número de chaves entre 1 e 2t-1."""
    raiz = tree.raiz
    return 1 <= len(raiz.chaves) <= 2 * tree.t - 1


def pos_no_interno_chaves(tree: 'BTree') -> bool:
    """Pós-condição: Para nós internos, número de chaves entre t-1 e 2t-1."""
    for no in tree._todos_nos():
        if no is not tree.raiz and not no.folha:
            if not (tree.t - 1 <= len(no.chaves) <= 2 * tree.t - 1):
                return False
    return True


def pos_raiz_filhos(tree: 'BTree') -> bool:
    """Pós-condição: Para a raiz, número de filhos entre 2 e 2t."""
    raiz = tree.raiz
    return 2 <= len(raiz.filhos) <= 2 * tree.t


def pos_no_interno_filhos(tree: 'BTree') -> bool:
    """Pós-condição: Para nós internos, número de filhos entre t e 2t."""
    for no in tree._todos_nos():
        if no is not tree.raiz and not no.folha:
            if not (tree.t <= len(no.filhos) <= 2 * tree.t):
                return False
    return True


# --- Invariantes Manuais --- #

def verificar_invariantes(tree: 'BTree') -> None:
    """Verifica os invariantes da Árvore-B."""

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
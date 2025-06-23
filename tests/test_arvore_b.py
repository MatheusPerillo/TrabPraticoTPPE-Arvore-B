import pytest
from arvore_b.btree import BTree

@pytest.fixture
def arvore_padrao():
    arvore = BTree(3)
    elementos = [10, 20, 5, 6, 12, 30, 40, 50, 60, 70, 80, 90]
    for e in elementos:
        arvore.inserir(e)
    return arvore

def test_insercao_e_busca(arvore_padrao):
    for chave in [5, 10, 20, 60]:
        assert arvore_padrao.buscar(chave)
    assert not arvore_padrao.buscar(999)

def test_remocao_em_folha(arvore_padrao):
    arvore_padrao.inserir(99)
    assert arvore_padrao.buscar(99)
    arvore_padrao.remover(99)
    assert not arvore_padrao.buscar(99)

def test_remocao_com_fusao():
    arvore = BTree(3)
    for valor in [10, 20, 5, 6, 12, 30, 40, 50]:
        arvore.inserir(valor)
    arvore.remover(6)
    assert not arvore.buscar(6)

def test_remocao_com_redistribuicao():
    arvore = BTree(3)
    for valor in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        arvore.inserir(valor)
    arvore.remover(2)
    assert not arvore.buscar(2)

def test_divisao_de_raiz():
    arvore = BTree(3)
    for v in [1, 2, 3, 4, 5, 6, 7]:
        arvore.inserir(v)
    assert arvore.altura > 1

def test_ordem_das_chaves():
    arvore = BTree(3)
    for v in [15, 5, 25, 10, 20]:
        arvore.inserir(v)
    todos = arvore._todos_nos()
    for no in todos:
        assert no.chaves == sorted(no.chaves)

def test_niveis_folhas_iguais():
    arvore = BTree(3)
    for v in [10, 20, 5, 6, 12, 30, 40, 50, 60, 70, 80, 90]:
        arvore.inserir(v)
    assert arvore._verificar_niveis_folhas()

def test_pre_condicao_inserir():
    arvore = BTree(3)
    arvore.inserir(10)
    with pytest.raises(Exception):
        arvore.inserir(10)

def test_pre_condicao_remover():
    arvore = BTree(3)
    with pytest.raises(Exception):
        arvore.remover(99)

def test_pos_condicao_remover():
    arvore = BTree(3)
    arvore.inserir(33)
    arvore.remover(33)
    assert not arvore.buscar(33)

# tests/test_arvore_b.py
import pytest
from arvore_b.btree import BTree
from arvore_b.bnode import BNode
from arvore_b.contratos import (
    pos_raiz_chaves, pos_no_interno_chaves, pos_raiz_filhos,
    pos_no_interno_filhos, pre_inserir, pre_remover, pos_remover
)
import random

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

def test_ordem_maior():
    arvore = BTree(5)
    for v in range(100):
        arvore.inserir(v)
    for v in range(100):
        assert arvore.buscar(v)

def test_insercao_remocao_aleatoria():
    arvore = BTree(3)
    valores = list(range(200))
    random.shuffle(valores)
    for v in valores:
        arvore.inserir(v)
    random.shuffle(valores)
    for v in valores[:100]:
        arvore.remover(v)
        assert not arvore.buscar(v)
    for v in valores[100:]:
        assert arvore.buscar(v)

def test_estrutura_nos_internos():
    arvore = BTree(3)
    for i in range(1, 50):
        arvore.inserir(i)
    for no in arvore._todos_nos():
        if not no.folha:
            assert len(no.filhos) == len(no.chaves) + 1

def test_inserir_em_no_interno_deve_falhar():
    no = BNode(t=3, folha=False)
    with pytest.raises(Exception):
        no.inserir_chave(5)

def test_contratos_pos_condicoes():
    arvore = BTree(3)
    for i in range(10, 40, 5):
        arvore.inserir(i)
    assert pos_raiz_chaves(arvore)
    assert pos_no_interno_chaves(arvore)
    if not arvore.raiz.folha:
        assert pos_raiz_filhos(arvore)
    for no in arvore._todos_nos():
        if no is not arvore.raiz and not no.folha:
            assert pos_no_interno_filhos(arvore)

def test_contratos_pre():
    arvore = BTree(3)
    arvore.inserir(15)
    assert pre_remover(arvore, 15)
    assert not pre_remover(arvore, 99)
    assert pre_inserir(arvore, 99)
    assert not pre_inserir(arvore, 15)

def test_contratos_pos_remover():
    arvore = BTree(3)
    arvore.inserir(42)
    arvore.remover(42)
    assert pos_remover(arvore, 42)

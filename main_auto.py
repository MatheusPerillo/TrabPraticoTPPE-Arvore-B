import random
from arvore_b.btree import BTree

def main():
    ordem = 3
    qtd_insercoes = 20
    qtd_buscas = 10
    qtd_remocoes = 5

    arvore = BTree(ordem)

    valores_inseridos = random.sample(range(1, 100), qtd_insercoes)
    print(f"Inserindo {qtd_insercoes} valores automaticamente:")
    for v in valores_inseridos:
        print(f"  Inserindo {v}")
        arvore.inserir(v)

    print("\nÁrvore após inserções:")
    arvore.imprimir()

    valores_para_buscar = random.sample(valores_inseridos, qtd_buscas // 2) + \
                          random.sample(range(101, 200), qtd_buscas // 2)
    print("\nBuscando valores:")
    for v in valores_para_buscar:
        resultado = arvore.buscar(v)
        print(f"  Busca por {v}: {'Encontrado' if resultado else 'Não encontrado'}")

    valores_para_remover = random.sample(valores_inseridos, qtd_remocoes)
    print("\nRemovendo valores:")
    for v in valores_para_remover:
        print(f"  Tentando remover {v}...")
        try:
            arvore.remover(v)
            print(f"  {v} removido com sucesso.")
        except:
            print(f"  Não foi possível remover {v} (pode não existir na árvore)")

    print("\nÁrvore após remoções:")
    arvore.imprimir()

if __name__ == "__main__":
    main()

from arvore_b.btree import BTree

def main():
    print("Criando Árvore-B de ordem 3...")
    t = 3
    arvore = BTree(t)

    elementos = [5, 7, 10, 12, 15, 18, 20, 25, 30, 35, 40,
                 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 92, 95, 98, 99]

    for elem in elementos:
        arvore.inserir(elem)

    print("\n\u00c1rvore-B construída com os elementos:")
    arvore.imprimir()

    print("\nBuscando alguns valores:")
    for chave in [25, 55, 99, 100]:
        encontrado = arvore.buscar(chave)
        print(f"Buscar({chave}) -> {'Encontrado' if encontrado else 'N\u00e3o encontrado'}")

    print("\nRemovendo algumas chaves:")
    for chave in [25, 40, 80]:
        print(f"Removendo {chave}...")
        arvore.remover(chave)
        arvore.imprimir()

if __name__ == "__main__":
    main()
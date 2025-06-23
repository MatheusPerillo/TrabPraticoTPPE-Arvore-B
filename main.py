from arvore_b.btree import BTree

if __name__ == "__main__":
    t = 3
    arvore = BTree(t)

    elementos = [40, 20, 60, 80, 10, 15, 30, 50, 70, 90,
                  5, 7, 12, 18, 25, 35, 45, 55, 65, 75, 85, 92, 98, 99]

    for elemento in elementos:
        arvore.inserir(elemento)

    print("Árvore original:")
    arvore.imprimir()

    print("\nRemovendo 55...")
    arvore.remover(55)
    arvore.imprimir()

    print("\nRemovendo 70...")
    arvore.remover(70)
    arvore.imprimir()

    print("\nRemovendo 20...")
    arvore.remover(20)
    arvore.imprimir()

    print("\nRemovendo 40...")
    arvore.remover(40)
    arvore.imprimir()


    print("Implementação inicial da Árvore-B criada.")

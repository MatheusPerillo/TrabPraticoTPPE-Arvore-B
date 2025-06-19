# Define a classe BNode (nó da árvore)
class BNode:
    def __init__(self, t: int, folha: bool):
        self.t = t
        self.folha = folha
        self.chaves = []
        self.filhos = []

    def __repr__(self):
        return f"{'Folha' if self.folha else 'Interno'}: {self.chaves}"

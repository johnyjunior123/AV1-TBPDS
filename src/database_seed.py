from biblioteca import Biblioteca


def criar_biblioteca_exemplo():
    biblioteca = Biblioteca()

    biblioteca.add_livro("L1", "Clean Code", "Robert Martin", "tecnico", 2)
    biblioteca.add_livro("L2", "O Hobbit", "Tolkien", "ficcao", 1)
    biblioteca.add_livro("L3", "SICP", "Abelson", "tecnico", 3)

    biblioteca.add_usuario("U1", "Ana", "11122233344", "ana@email.com", "comum")
    biblioteca.add_usuario("U2", "Bruno", "55566677788", "bruno@email.com", "premium")
    biblioteca.add_usuario("U3", "Carla", "99988877766", "carla@email.com", "funcionario")

    return biblioteca

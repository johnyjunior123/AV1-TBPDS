class BibliotecaDatabase:
    def __init__(self):
        self.livros = {}
        self.usuarios = {}
        self.emprestimos = []
        self.reservas = []

    def salvar_livro(self, livro):
        self.livros[livro.id] = livro

    def salvar_usuario(self, usuario):
        self.usuarios[usuario.id] = usuario

    def salvar_emprestimo(self, emprestimo):
        self.emprestimos.append(emprestimo)

    def salvar_reserva(self, reserva):
        self.reservas.append(reserva)

    def buscar_livro(self, livro_id):
        return self.livros.get(livro_id)

    def buscar_usuario(self, usuario_id):
        return self.usuarios.get(usuario_id)

    def buscar_emprestimo_ativo(self, usuario_id, livro_id):
        for emprestimo in self.emprestimos:
            if (
                emprestimo.usuario_id == usuario_id
                and emprestimo.livro_id == livro_id
                and not emprestimo.devolvido
            ):
                return emprestimo
        return None

    def listar_livros(self):
        return list(self.livros.values())

    def listar_usuarios(self):
        return list(self.usuarios.values())

    def listar_reservas(self):
        return list(self.reservas)

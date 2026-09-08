def mascarar_cpf(cpf):
    if len(cpf) < 4:
        return "***"
    return f"***{cpf[-4:]}"

class RelatorioDetalhado:
    def formatar(self, livros, usuarios, reservas):
        linhas = ["=== RELATORIO DA BIBLIOTECA ==="]

        for livro in livros:
            linhas.append(
                "Livro: "
                f"{livro.titulo} | Disponivel: "
                f"{livro.quantidade_disponivel}/{livro.quantidade_total}"
            )

        for usuario in usuarios:
            linhas.append(
                "Usuario: "
                f"{usuario.nome} CPF: {mascarar_cpf(usuario.cpf)} | "
                f"Emprestimos: {usuario.emprestimos_ativos}"
            )

        return "\n".join(linhas)


class RelatorioResumo:
    def formatar(self, livros, usuarios, reservas):
        total_livros = sum(livro.quantidade_total for livro in livros)
        livros_disponiveis = sum(livro.quantidade_disponivel for livro in livros)
        emprestimos_ativos = sum(usuario.emprestimos_ativos for usuario in usuarios)

        return (
            f"Livros: {livros_disponiveis}/{total_livros} disponiveis | "
            f"Usuarios: {len(usuarios)} | "
            f"Emprestimos ativos: {emprestimos_ativos} | "
            f"Reservas: {len(reservas)}"
        )

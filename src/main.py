import datetime as dt
import logging

from database_seed import criar_biblioteca_exemplo


def configurar_logs():
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def registrar_titulo(titulo):
    logging.info("")
    logging.info(titulo)


def forcar_vencimento(biblioteca, usuario_id, livro_id, dias_atraso):
    for emprestimo in biblioteca.database.emprestimos:
        if emprestimo.usuario_id == usuario_id and emprestimo.livro_id == livro_id:
            emprestimo.vencimento = dt.date.today() - dt.timedelta(days=dias_atraso)


def executar_cenarios():
    biblioteca = criar_biblioteca_exemplo()

    registrar_titulo("========== CENARIO 1: emprestimos normais ==========")
    biblioteca.emprestar("U1", "L1")
    biblioteca.emprestar("U2", "L2")
    biblioteca.emprestar("U3", "L3")

    registrar_titulo("========== CENARIO 2: livro esgotado e reserva ==========")
    biblioteca.emprestar("U1", "L2")
    biblioteca.reservar("U1", "L2")

    registrar_titulo("========== CENARIO 3: limite de emprestimos (comum = 3) ==========")
    biblioteca.add_livro("L4", "Livro Extra 1", "Autor", "geral", 5)
    biblioteca.add_livro("L5", "Livro Extra 2", "Autor", "geral", 5)
    biblioteca.add_livro("L6", "Livro Extra 3", "Autor", "geral", 5)
    biblioteca.emprestar("U1", "L4")
    biblioteca.emprestar("U1", "L5")
    biblioteca.emprestar("U1", "L6")

    registrar_titulo("========== CENARIO 4: devolucao no prazo (sem multa) ==========")
    biblioteca.devolver("U1", "L1")

    registrar_titulo("========== CENARIO 5: devolucao com ATRASO e multa por tipo ==========")
    forcar_vencimento(biblioteca, "U1", "L4", 5)
    biblioteca.devolver("U1", "L4")

    forcar_vencimento(biblioteca, "U2", "L2", 10)
    biblioteca.devolver("U2", "L2")

    forcar_vencimento(biblioteca, "U3", "L3", 20)
    biblioteca.devolver("U3", "L3")

    registrar_titulo("========== CENARIO 6: relatorio final ==========")
    logging.info(biblioteca.gerar_relatorio())

    registrar_titulo("========== CENARIO 7: professor e relatorio resumido ==========")
    biblioteca.add_usuario("U4", "Daniel", "12312312399", "daniel@email.com", "professor")
    biblioteca.add_livro("L7", "Domain-Driven Design", "Eric Evans", "tecnico", 1)
    biblioteca.emprestar("U4", "L7")
    forcar_vencimento(biblioteca, "U4", "L7", 30)
    biblioteca.devolver("U4", "L7")
    logging.info(biblioteca.gerar_relatorio_resumido())


if __name__ == "__main__":
    configurar_logs()
    executar_cenarios()

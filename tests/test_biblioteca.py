import datetime as dt
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from database_seed import criar_biblioteca_exemplo


class BibliotecaTest(unittest.TestCase):
    def test_preserva_fluxo_principal_do_legado(self):
        biblioteca = criar_biblioteca_exemplo()

        self.assertTrue(biblioteca.emprestar("U1", "L1"))
        self.assertTrue(biblioteca.emprestar("U2", "L2"))
        self.assertTrue(biblioteca.emprestar("U3", "L3"))
        self.assertFalse(biblioteca.emprestar("U1", "L2"))

        biblioteca.add_livro("L4", "Livro Extra 1", "Autor", "geral", 5)
        biblioteca.add_livro("L5", "Livro Extra 2", "Autor", "geral", 5)
        biblioteca.add_livro("L6", "Livro Extra 3", "Autor", "geral", 5)

        self.assertTrue(biblioteca.emprestar("U1", "L4"))
        self.assertTrue(biblioteca.emprestar("U1", "L5"))
        self.assertFalse(biblioteca.emprestar("U1", "L6"))
        self.assertEqual(0, biblioteca.devolver("U1", "L1"))

        self._forcar_vencimento(biblioteca, "U1", "L4", 5)
        self._forcar_vencimento(biblioteca, "U2", "L2", 10)
        self._forcar_vencimento(biblioteca, "U3", "L3", 20)

        self.assertEqual(10, biblioteca.devolver("U1", "L4"))
        self.assertEqual(10, biblioteca.devolver("U2", "L2"))
        self.assertEqual(0, biblioteca.devolver("U3", "L3"))

        relatorio = biblioteca.gerar_relatorio()
        self.assertIn("Livro: Clean Code | Disponivel: 2/2", relatorio)
        self.assertIn("Usuario: Ana CPF: ***3344 | Emprestimos: 1", relatorio)

    def test_corrige_bug_de_usuario_inexistente_no_emprestimo(self):
        biblioteca = criar_biblioteca_exemplo()

        self.assertFalse(biblioteca.emprestar("U999", "L1"))

    def test_professor_tem_prazo_maior_e_multa_zero(self):
        biblioteca = criar_biblioteca_exemplo()
        biblioteca.add_usuario("U4", "Daniel", "12312312399", "daniel@email.com", "professor")

        self.assertTrue(biblioteca.emprestar("U4", "L1"))

        emprestimo = biblioteca.database.buscar_emprestimo_ativo("U4", "L1")
        self.assertEqual(dt.date.today() + dt.timedelta(days=60), emprestimo.vencimento)

        self._forcar_vencimento(biblioteca, "U4", "L1", 30)
        with self.assertLogs("biblioteca", level="INFO") as logs:
            self.assertEqual(0, biblioteca.devolver("U4", "L1"))
        self.assertTrue(
            any("Devolucao com atraso. Multa: 0" in mensagem for mensagem in logs.output)
        )

    def test_reserva_so_e_aceita_para_livro_indisponivel(self):
        biblioteca = criar_biblioteca_exemplo()

        self.assertFalse(biblioteca.reservar("U1", "L1"))

        self.assertTrue(biblioteca.emprestar("U2", "L2"))
        self.assertTrue(biblioteca.reservar("U1", "L2"))
        self.assertEqual(1, len(biblioteca.database.reservas))

    def test_relatorio_resumido(self):
        biblioteca = criar_biblioteca_exemplo()

        self.assertEqual(
            "Livros: 6/6 disponiveis | Usuarios: 3 | Emprestimos ativos: 0 | Reservas: 0",
            biblioteca.gerar_relatorio_resumido(),
        )

    def _forcar_vencimento(self, biblioteca, usuario_id, livro_id, dias_atraso):
        emprestimo = biblioteca.database.buscar_emprestimo_ativo(usuario_id, livro_id)
        emprestimo.vencimento = dt.date.today() - dt.timedelta(days=dias_atraso)


if __name__ == "__main__":
    unittest.main()

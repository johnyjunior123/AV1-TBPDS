import logging
from datetime import date, timedelta
from database import BibliotecaDatabase
from entidades import Emprestimo, Livro, Reserva, Usuario, criar_tipo_usuario
from formatadores import RelatorioDetalhado, RelatorioResumo

logger = logging.getLogger(__name__)

class Biblioteca:
    def __init__(self, database=None):
        self.database = database or BibliotecaDatabase()

    def add_livro(self, livro_id, titulo, autor, categoria, quantidade):
        livro = Livro(livro_id, titulo, autor, categoria, quantidade)
        self.database.salvar_livro(livro)
        return livro

    def add_usuario(self, usuario_id, nome, cpf, email, tipo):
        usuario = Usuario(usuario_id, nome, cpf, email, criar_tipo_usuario(tipo))
        self.database.salvar_usuario(usuario)
        return usuario

    def emprestar(self, usuario_id, livro_id):
        logger.info("Processando emprestimo: usuario %s livro %s", usuario_id, livro_id)

        usuario = self.database.buscar_usuario(usuario_id)
        if usuario is None:
            logger.warning("Usuario nao encontrado: %s", usuario_id)
            return False

        livro = self.database.buscar_livro(livro_id)
        if livro is None:
            logger.warning("Livro nao encontrado: %s", livro_id)
            return False

        if usuario.bloqueado:
            logger.warning("Usuario bloqueado: %s", usuario_id)
            return False

        if not livro.disponivel:
            logger.warning("Livro indisponivel: %s", livro_id)
            return False

        if usuario.atingiu_limite_emprestimos():
            logger.warning("Limite de emprestimos atingido: usuario %s", usuario_id)
            return False

        return self._registrar_emprestimo(usuario, livro)

    def devolver(self, usuario_id, livro_id):
        logger.info("Processando devolucao: usuario %s livro %s", usuario_id, livro_id)

        usuario = self.database.buscar_usuario(usuario_id)
        if usuario is None:
            logger.warning("Usuario nao encontrado: %s", usuario_id)
            return -1

        livro = self.database.buscar_livro(livro_id)
        if livro is None:
            logger.warning("Livro nao encontrado: %s", livro_id)
            return -1

        emprestimo = self.database.buscar_emprestimo_ativo(usuario_id, livro_id)
        if emprestimo is None:
            logger.warning("Emprestimo nao encontrado: usuario %s livro %s", usuario_id, livro_id)
            return -1

        emprestimo.devolvido = True
        livro.devolver_exemplar()
        usuario.registrar_devolucao()

        multa = self._calcular_multa(usuario, emprestimo)
        if self._emprestimo_atrasado(emprestimo):
            logger.info("Devolucao com atraso. Multa: %s", multa)
        else:
            logger.info("Devolucao OK no prazo")
        return multa

    def reservar(self, usuario_id, livro_id):
        logger.info("Processando reserva: usuario %s livro %s", usuario_id, livro_id)

        usuario = self.database.buscar_usuario(usuario_id)
        if usuario is None:
            logger.warning("Usuario nao encontrado: %s", usuario_id)
            return False

        livro = self.database.buscar_livro(livro_id)
        if livro is None:
            logger.warning("Livro nao encontrado: %s", livro_id)
            return False

        if livro.disponivel:
            logger.warning("Livro disponivel; reserva nao aceita: %s", livro_id)
            return False

        reserva = Reserva(usuario_id=usuario.id, livro_id=livro.id)
        self.database.salvar_reserva(reserva)
        logger.info("Reserva registrada: usuario %s livro %s", usuario_id, livro_id)
        return True

    def gerar_relatorio(self, formatador=None):
        formatador = formatador or RelatorioDetalhado()
        return formatador.formatar(
            self.database.listar_livros(),
            self.database.listar_usuarios(),
            self.database.listar_reservas(),
        )

    def gerar_relatorio_resumido(self):
        return self.gerar_relatorio(RelatorioResumo())

    def _registrar_emprestimo(self, usuario, livro):
        try:
            livro.emprestar_exemplar()
            usuario.registrar_emprestimo()
            vencimento = date.today() + timedelta(days=usuario.tipo.prazo_dias)
            emprestimo = Emprestimo(usuario.id, livro.id, vencimento)
            self.database.salvar_emprestimo(emprestimo)
        except Exception:
            logger.exception(
                "Erro ao registrar emprestimo: usuario %s livro %s",
                usuario.id,
                livro.id,
            )
            return False

        logger.info(
            "Emprestimo OK para usuario %s livro %s vence em %s",
            usuario.id,
            livro.id,
            vencimento,
        )
        return True

    def _calcular_multa(self, usuario, emprestimo):
        if not self._emprestimo_atrasado(emprestimo):
            return 0

        dias_atraso = (date.today() - emprestimo.vencimento).days
        return usuario.tipo.calcular_multa(dias_atraso)

    def _emprestimo_atrasado(self, emprestimo):
        return date.today() > emprestimo.vencimento

    def addLivro(self, livro_id, titulo, autor, categoria, quantidade):
        return self.add_livro(livro_id, titulo, autor, categoria, quantidade)

    def addUsuario(self, usuario_id, nome, cpf, email, tipo):
        return self.add_usuario(usuario_id, nome, cpf, email, tipo)

    def relatorio(self):
        return self.gerar_relatorio()

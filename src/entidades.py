from dataclasses import dataclass, field
from datetime import date

from constantes import (
    LIMITE_EMPRESTIMOS_COMUM,
    LIMITE_EMPRESTIMOS_FUNCIONARIO,
    LIMITE_EMPRESTIMOS_PADRAO,
    LIMITE_EMPRESTIMOS_PREMIUM,
    LIMITE_EMPRESTIMOS_PROFESSOR,
    MULTA_POR_DIA_COMUM,
    MULTA_POR_DIA_FUNCIONARIO,
    MULTA_POR_DIA_PADRAO,
    MULTA_POR_DIA_PREMIUM,
    MULTA_POR_DIA_PROFESSOR,
    PRAZO_DIAS_COMUM,
    PRAZO_DIAS_FUNCIONARIO,
    PRAZO_DIAS_PADRAO,
    PRAZO_DIAS_PREMIUM,
    PRAZO_DIAS_PROFESSOR,
)


class TipoUsuario:
    nome = "padrao"
    limite_emprestimos = LIMITE_EMPRESTIMOS_PADRAO
    prazo_dias = PRAZO_DIAS_PADRAO
    multa_por_dia = MULTA_POR_DIA_PADRAO

    def calcular_multa(self, dias_atraso):
        return dias_atraso * self.multa_por_dia


class UsuarioComum(TipoUsuario):
    nome = "comum"
    limite_emprestimos = LIMITE_EMPRESTIMOS_COMUM
    prazo_dias = PRAZO_DIAS_COMUM
    multa_por_dia = MULTA_POR_DIA_COMUM


class UsuarioPremium(TipoUsuario):
    nome = "premium"
    limite_emprestimos = LIMITE_EMPRESTIMOS_PREMIUM
    prazo_dias = PRAZO_DIAS_PREMIUM
    multa_por_dia = MULTA_POR_DIA_PREMIUM


class UsuarioFuncionario(TipoUsuario):
    nome = "funcionario"
    limite_emprestimos = LIMITE_EMPRESTIMOS_FUNCIONARIO
    prazo_dias = PRAZO_DIAS_FUNCIONARIO
    multa_por_dia = MULTA_POR_DIA_FUNCIONARIO


class UsuarioProfessor(TipoUsuario):
    nome = "professor"
    limite_emprestimos = LIMITE_EMPRESTIMOS_PROFESSOR
    prazo_dias = PRAZO_DIAS_PROFESSOR
    multa_por_dia = MULTA_POR_DIA_PROFESSOR


TIPOS_USUARIO = {
    UsuarioComum.nome: UsuarioComum,
    UsuarioPremium.nome: UsuarioPremium,
    UsuarioFuncionario.nome: UsuarioFuncionario,
    UsuarioProfessor.nome: UsuarioProfessor,
}


def criar_tipo_usuario(nome):
    return TIPOS_USUARIO.get(nome, TipoUsuario)()


@dataclass
class Livro:
    id: str
    titulo: str
    autor: str
    categoria: str
    quantidade_disponivel: int
    quantidade_total: int = field(init=False)

    def __post_init__(self):
        self.quantidade_total = self.quantidade_disponivel

    @property
    def disponivel(self):
        return self.quantidade_disponivel > 0

    def emprestar_exemplar(self):
        if not self.disponivel:
            raise ValueError("Livro indisponivel")
        self.quantidade_disponivel -= 1

    def devolver_exemplar(self):
        self.quantidade_disponivel += 1


@dataclass
class Usuario:
    id: str
    nome: str
    cpf: str
    email: str
    tipo: TipoUsuario
    emprestimos_ativos: int = 0
    bloqueado: bool = False

    def atingiu_limite_emprestimos(self):
        return self.emprestimos_ativos >= self.tipo.limite_emprestimos

    def registrar_emprestimo(self):
        self.emprestimos_ativos += 1

    def registrar_devolucao(self):
        if self.emprestimos_ativos > 0:
            self.emprestimos_ativos -= 1


@dataclass
class Emprestimo:
    usuario_id: str
    livro_id: str
    vencimento: date
    devolvido: bool = False


@dataclass
class Reserva:
    usuario_id: str
    livro_id: str
    data: date = field(default_factory=date.today)

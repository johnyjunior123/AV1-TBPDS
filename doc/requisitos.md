# Sistema de Biblioteca

Esse será um levantamento de requisitos ou entendimento do sistema antes de começar a refatoração afim de confirmar o que o sistema precisa que funcione no final.

## Requisitos Básicos

- Adicionar Livro
- Adicionar Usuário
- Emprestar Livro

## O que cada entidade possuí

### Livro

- titulo: string
- autor: string
- categoria: string
- qntde: number
- qntde total: number

### Usuário

- nome: string
- cpf: string
- email: string
- tipo: string
- emprestimos_ativos: number
- bloqueado: boolean

### Emprestimo

- id_usuario: number
- id_livro: number
- vencimento: date
- devolvido: boolean

## Regras

### Limite de Emprestimos

Um usuário deverá ter limite de quantidade de livros emprestados de acordo com o tipo do usuário:

- comum : 3
- premium : 5
- funcionario : 10
- outros : 1

E também um limite de tempo:

- comum : 7 dias
- premium : 14 dias
- funcionario : 30 dias
- outros : 3

## Bloqueio de Usuário

Caso um usuário esteja bloqueado não poderá fazer um emprestimo.

## Multa por atraso

Em caso de atraso na devolução deverá ser feito um calculo da multa:

- comum = dias * 2
- premium = dias * 1
- funcionario = 0

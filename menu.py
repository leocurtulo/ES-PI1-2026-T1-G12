
def menu_principal():
    print("="*40)
    print(" SISTEMA DE VOTAÇÃO ".center(40))
    print("="*40)
    print("1 - Gerenciamento")
    print("2 - Votação")
    print("0 - Sair")
    print("="*40)
    opcao = int(input("Escolha: "))
    return opcao


def menu_gerenciamento():
    print("="*40)
    print(" GERENCIAMENTO ".center(40))
    print("="*40)
    print("1 - Eleitores")
    print("2 - Candidatos")
    print("0 - Voltar")
    print("="*40)
    opcao = int(input("Escolha: "))
    return opcao


def menu_eleitores():
    print("="*40)
    print(" ELEITORES ".center(40))
    print("="*40)
    print("1 - Cadastrar")
    print("2 - Listar")
    print("3 - Buscar")
    print("4 - Editar")
    print("5 - Remover")
    print("6 - Tornar Mesário")
    print("7 - Listar Mesário")
    print("0 - Voltar")
    print("="*40)

    opcao = int(input("Escolha: "))
    return opcao


def menu_candidatos():
    print("="*40)
    print(" CANDIDATOS ".center(40))
    print("="*40)
    print("1 - Cadastrar")
    print("2 - Listar")
    print("3 - Buscar")
    print("4 - Editar")
    print("5 - Remover")
    print("0 - Voltar")
    print("="*40)

    opcao = int(input("Escolha: "))
    return opcao


def menu_votacao():
    print("="*40)
    print(" VOTAÇÃO ".center(40))
    print("="*40)
    print("1 - Abrir sistema de votação")
    print("2 - Votar")
    print("3 - Encerrar sistema de votação")
    print("4 - Auditoria")
    print("5 - Resultados")
    print("0 - Voltar")
    print("="*40)

    opcao = int(input("Escolha: "))
    return opcao


def menu_abertura():
    print("="*40)
    print(" ABERTURA ".center(40))
    print("="*40)
    print("1 - Votar")
    print("2 - Encerrar")
    print("0 - Voltar")
    print("="*40)

    opcao = int(input("Escolha: "))
    return opcao


def menu_auditoria():
    print("="*40)
    print(" AUDITORIA ".center(40))
    print("="*40)
    print("1 - Logs")
    print("2 - Protocolos")
    print("0 - Voltar")
    print("="*40)

    opcao = int(input("Escolha: "))
    return opcao


def menu_resultados():
    print("="*40)
    print(" RESULTADOS ".center(40))
    print("="*40)
    print("1 - Boletim")
    print("2 - Estatísticas")
    print("3 - Partido")
    print("4 - Integridade")
    print("0 - Voltar")
    print("="*40)

    opcao = int(input("Escolha: "))
    return opcao


def menu_mesarios():
    print("="*40)
    print(" MESÁRIOS ".center(40))
    print("="*40)
    print("1 - Cadastrar")
    print("2 - Listar")
    print("3 - Buscar")
    print("4 - Editar")
    print("5 - Remover")
    print("0 - Voltar")
    print("="*40)

    opcao = int(input("Escolha: "))
    return opcao
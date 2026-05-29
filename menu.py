import os

def limpar_tela():
    os.system("cls" if os.name == "nt" else clear)

def ler_opcao():
    opcao = input("Escolha: ").strip()

    while not opcao.isdigit():
        print("Digite apenas números.")
        opcao = input("Escolha: ").strip()
    return int(opcao)



def menu_principal():
    print("="*40)
    print(" SISTEMA DE VOTAÇÃO ".center(40))
    print("="*40)
    print("1 - Gerenciamento")
    print("2 - Votação")
    print("0 - Sair")
    print("="*40)
    return ler_opcao()


def menu_gerenciamento():
    limpar_tela()
    print("="*40)
    print(" GERENCIAMENTO ".center(40))
    print("="*40)
    print("1 - Eleitores")
    print("2 - Candidatos")
    print("0 - Voltar")
    print("="*40)
    return ler_opcao()


def menu_eleitores():
    limpar_tela()
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

    return ler_opcao()


def menu_candidatos():
    limpar_tela()
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

    return ler_opcao()


def menu_votacao():
    limpar_tela()
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

    return ler_opcao()


def menu_abertura():
    limpar_tela()
    print("="*40)
    print(" ABERTURA ".center(40))
    print("="*40)
    print("1 - Votar")
    print("2 - Encerrar")
    print("0 - Voltar")
    print("="*40)

    opcao = int(input("Escolha: "))
    return ler_opcao()


def menu_auditoria():
    limpar_tela()
    print("="*40)
    print(" AUDITORIA ".center(40))
    print("="*40)
    print("1 - Logs")
    print("2 - Protocolos")
    print("0 - Voltar")
    print("="*40)

    return ler_opcao()


def menu_resultados():
    limpar_tela()
    print("="*40)
    print(" RESULTADOS ".center(40))
    print("="*40)
    print("1 - Boletim")
    print("2 - Estatísticas")
    print("3 - Partido")
    print("4 - Integridade")
    print("0 - Voltar")
    print("="*40)

    return ler_opcao()


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

    return ler_opcao()


def menu_votacao_fechada():
    limpar_tela()
    print("="*40)
    print(" VOTAÇÃO ".center(40))
    print("="*40)
    print("1 - Abrir sistema de votação")
    print("0 - Voltar")
    print("="*40)

    return ler_opcao()

def menu_urna():
    limpar_tela()
    print("="*40)
    print(" URNA EM FUNCIONAMENTO ".center(40))
    print("="*40)
    print("1 - Votar")
    print("2 - Encerrar sistema de votação")
    print("3 - Auditoria")
    print("4 - Resultados")
    print("0 - Voltar")
    print("="*40)

    return ler_opcao()


def menu_votacao_inicial():
    limpar_tela()
    print("="*40)
    print(" VOTAÇÃO ".center(40))
    print("="*40)
    print("1 - Abrir votação")
    print("2 - Resultados")
    print("3 - Auditoria")
    print("4 - Entrar na urna")
    print("0 - Voltar")
    print("="*40)

    return ler_opcao()

import conexao
from za import validar_titulo
import random


def validar_cpf(cpf):
    cpf = cpf.strip()
    cpf = cpf.replace(".", "")
    cpf = cpf.replace("-", "")
    if len(cpf) != 11:
        return False       
    elif not cpf.isdigit():
        return False
    elif cpf == cpf[0] * 11:
        return False
    soma = 0
    for i in range (9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma  % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1= (11 - resto)

    soma = 0
    for i in range (10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = (11 - resto)
    if digito2 >= 10:
        digito2 = 0


    return cpf[9] == str(digito1) and cpf[10] == str(digito2)






def cadastro_eleitores():
    nome = input("Digite Seu nome completo: ").strip()

    titulo_eleitor = input("Digite seu titulo de eleitor: ").strip()
    titulo_eleitor = titulo_eleitor.replace(" ", "")
    if not validar_titulo(titulo_eleitor):
        print ("Título inváldo. Cadastro não realizado.")
        return


    cpf = input("Digite seu CPF: ").strip()
    cpf = cpf.replace(".", "").replace("-", "")

    
    if not validar_cpf(cpf):
        print("CPF inválido. Cadastro não realizado.")
        return  

    print("CPF válido.")

    chave = chave_acesso(nome)
    if chave == "":
        print("Cadastro cancelado.")
        return
    print(f"SUA CHAVE DE ACESSO: {chave}")
    print("Guarde sua chave de acesso, ela será necessária no momento da votação!")

    mesario = input("Você atuará como mesário? (SIM) ou (NÃO): ").strip().upper()
    valor_mesario = True if mesario == "SIM" else False

    

    sql = """
        INSERT INTO eleitores 
        (cpf, nome_completo, titulo_eleitor, chave_acesso, is_mesario)
        VALUES (%s, %s, %s, %s, %s)
    """

    valores = (
        cpf,
        nome,
        titulo_eleitor,
        chave,
        valor_mesario,
        
    )

    conexao.cursor.execute(sql, valores)
    conexao.conexao.commit()

    print("Eleitor cadastrado com sucesso!")





def buscar_eleitor():

    cpf = input("Digite o CPF para buscar: ")
    cpf = cpf.strip()
    cpf = cpf.replace(".", "")
    cpf = cpf.replace("-", "")


    sql = "SELECT * FROM eleitores WHERE cpf = %s"

    valores = (cpf,)

    conexao.cursor.execute(sql, valores)

    resultado = conexao.cursor.fetchone()

    if resultado:
        print("Eleitor encontrado!")
        print(f"\nID: {resultado[0]}")
        print(f"Nome Completo: {resultado[2]}")
        print(f"CPF: {resultado[1]}")
        print(f"Título de Eleitor: {resultado[3]}")
        print(f"Chave de Acesso: {resultado[4]}")
        print(f"Mesário: {'Sim' if resultado[5] == 1 else 'Não'}")
        
    else:
        print("Eleitor não encontrado.")




def listar_eleitores():
    sql = """
        SELECT cpf, nome_completo, titulo_eleitor, is_mesario, ja_votou
        FROM eleitores
    """
    conexao.cursor.execute(sql)
    resultados = conexao.cursor.fetchall()

    if not resultados:
        print("Nenhum eleitor cadastrado")
        return
    
    for e in resultados:
        if e[3] == 0:
            print(f"\nNome: {e[1]}")
            print(f"CPF: {e[0]}")
            print(f"Título: {e[2]}")
            print(f"Mesário: {'Sim' if e[3]== 1 else 'Não'}")
            print(f"Já votou: {'Sim' if e[4]== 1 else 'Não'}")




def remover_eleitores():
    cpf = input("Digite o CPF do eleitor que deseja remover: ")
    cpf = cpf.strip()
    cpf = cpf.replace("-", "")
    cpf = cpf.replace(".", "")

    sql = "SELECT nome_completo FROM eleitores WHERE cpf = %s"
    conexao.cursor.execute(sql, (cpf,))
    eleitor = conexao.cursor.fetchone()

    if not eleitor:
        print("Eleitor não encontrado!")
        return
    confirmacao = input(f"Tem certeza que deseja remover {eleitor[0]}? Sim (S) ou Não (N): ")
    confirmacao = confirmacao.upper()

    if confirmacao != "S":
        print("A remoção foi cancelada!")
        return
    
    sql_delete = "DELETE FROM eleitores WHERE cpf = %s"
    conexao.cursor.execute(sql_delete, (cpf,))
    conexao.conexao.commit()

    print("Eleitor removido com sucesso!")




def listar_mesarios():
    sql = """
        SELECT cpf, nome_completo, titulo_eleitor, is_mesario, ja_votou
        FROM eleitores WHERE is_mesario = 1
    """
    conexao.cursor.execute(sql)
    resultados = conexao.cursor.fetchall()

    if not resultados:
        print("Nenhum mesário cadastrado")
        return
    
    for e in resultados:
        print(f"\nNome: {e[1]}")
        print(f"CPF: {e[0]}")
        print(f"Título: {e[2]}")
        print(f"Mesário: {'Sim' if e[3]== 1 else 'Não'}")
        print(f"Já votou: {'Sim' if e[4]== 1 else 'Não'}")


def cadastrar_candidato():
    nome = input("Digite o nome do candidato: ").strip()
    if nome == "":
        print("O nome do candidato deve ser preenchido.")
        return
    
    numero = input("Digite o número do candidato: ").strip()
    if not numero.isdigit():
        print("Digite apenas números.")
        return
    numero_int = int(numero)
    if numero_candidato(numero_int):
        print("Esse número pertence a outro candidato.")
        return
    

    partido = input("Digite o partido do candidato: ").strip()
    if partido == "":
        print("O partido do candidato deve ser preenchido.")
        return
    
    sql = """ 
        INSERT INTO candidatos (nome, numero, partido)
        VALUES (%s, %s, %s)
    """
    valores = (nome, numero_int, partido)
    
    conexao.cursor.execute(sql, valores)
    conexao.conexao.commit()

    print("Candidato cadastrado com sucesso!!")

    



def numero_candidato(numero):
    sql = "SELECT 1 FROM candidatos WHERE numero = %s"
    conexao.cursor.execute(sql,(numero,))
    resultado = conexao.cursor.fetchone()
    if resultado:
        return True 
    else:
        return False

    
        
def buscar_candidatos():
    numero = input("Digite o número do candidato que deseja buscar: ").strip()
    if not numero.isdigit():
        print("Busca inválida, digite apenas números.")
        return
    
    numero_int = int(numero)
    
    sql = """
        SELECT nome, numero, partido
        FROM candidatos
        WHERE numero = %s
    """
    conexao.cursor.execute(sql, (numero_int,))
    candidato = conexao.cursor.fetchone()

    if candidato:
        print("Candidato encontrado!")
        print(f"\nNome: {candidato[0]}")
        print(f"Número: {candidato[1]}")
        print(f"Partido: {candidato[2]}")
    else:
        print("Candidato não encontrado.")


def listar_candidatos():
    sql = """
        SELECT nome, numero, partido
        FROM candidatos
    """
    conexao.cursor.execute(sql)
    resultados = conexao.cursor.fetchall()

    if not resultados:
        print("Nenhum candidato cadastrado.")
        return
    
    for c in resultados:
        print(f"\nNome: {c[0]}")
        print(f"Número: {c[1]}")
        print(f"Partido: {c[2]}")


def remover_candidato():
    numero = input("Digite o número do candidato que deseja remover: ")
    numero = numero.strip()
    if not numero.isdigit():
        print("Digite apenas números.")
        return
    numero_int = int(numero)


    sql = "SELECT nome FROM candidatos WHERE numero = %s"
    conexao.cursor.execute(sql, (numero_int,))
    candidato = conexao.cursor.fetchone()

    if not candidato:
        print("Candidato não encontrado.")
        return

    confirmacao = input(f"Tem certeza que deseja remover {candidato[0]}? Sim (S) ou Não (N): ")
    confirmacao = confirmacao.upper()

    if confirmacao != "S":
        print("A remoção foi cancelada!")
        return
    
    sql_delete = "DELETE FROM candidatos WHERE numero = %s"
    conexao.cursor.execute(sql_delete, (numero_int,))
    conexao.conexao.commit()

    print("Candidato removido com sucesso!")
    


def chave_acesso(nome_completo):
    nome_completo = nome_completo.strip()
    nome_completo = nome_completo.split()
    partes_nome = nome_completo

    if len(partes_nome) < 2:
        print ("Deve ser digitado o nome e o sobrenome")
        return 
    
    
    primeiro_nome = partes_nome [0]
    segundo_nome = partes_nome [1]

    letras = primeiro_nome[:2].upper() + segundo_nome[0].upper()
    numeros = f"{random.randint(0, 9999):04d}"
    return letras + numeros






def validar_mesario(titulo_eleitor, cpf4, chave):
    sql = """
        SELECT cpf, chave_acesso, is_mesario
        FROM eleitores
        WHERE titulo_eleitor = %s
    """
    conexao.cursor.execute(sql, (titulo_eleitor,))
    resultado = conexao.cursor.fetchone()

    if not resultado:
        return False

    cpf_banco = resultado[0]
    chave_banco = resultado[1]
    is_mesario = resultado[2]

    # valida 4 primeiros dígitos do CPF
    if cpf_banco[:4] != cpf4:
        return False

    # valida chave
    if chave_banco != chave:
        return False

    # valida se é mesário
    if is_mesario != 1:
        return False

    return True







def zerezima():
    print("\n=== REALLIZANDO A ZERÉZIMA ===")

    conexao.cursor.execute("DELETE FROM votos")# limpar votos
    conexao.conexao.commit()

    sql = "SELECT nome, numero FROM candidatos ORDER BY nome"
    conexao.cursor.execute(sql)
    candidatos = conexao.cursor.fetchall()

    for c in candidatos:
        print(f"{c[0]} ({c[1]}) - 0 votos")

    print("\nZerézima realizada com sucesso, todos os votos foram zerados.")






def abrir_votacao():
    titulo = input("Título: ")
    cpf4 = input("CPF (4 dígitos): ")
    chave = input("Chave: ")

    if not validar_mesario(titulo, cpf4, chave):
        print("Acesso negado.")
        return False

    print("Mesário autenticado com sucesso!")
    zerezima()

    return True




def encerrar_votacao():
    print("\n=== ENCERRAR VITAÇÃO ===")

    titulo = input("Título de eleitor: ")
    cpf4 = input("4 primeiros dígitos do CPF: ")
    chave = input("Chave de acesso: ")

    if not validar_mesario(titulo, cpf4, chave):
        print("Validação não realizada")
        return

    confirm = input("Deseja realmente encerrar? (Sim/Não): ").lower()

    if confirm != "sim":
        print("Encerramento cancelado")
        return

    chave2 = input("Digite novamente a chave de acesso: ")

    if chave2 != chave:
        print("Chave incorreta")
        return

    print("Votação encerrada com sucesso!")






def registrar_ocorrencia(tipo, descricao, cpf_eleitor=None):
    sql = """
        INSERT INTO auditoria (tipo, descricao, cpf_eleitor)
        VALUES (%s, %s, %s)
    """
    valores = (tipo, descricao, cpf_eleitor)
    conexao.cursor.execute(sql, valores)
    conexao.conexao.commit()
    print("Ocorrência registrada na auditoria.")
    registrar_ocorrencia("TENTATIVA DUPLA VOTO", "Eleitor tentou votar novamente.")
    registrar_ocorrencia("ERRO CPF", "CPF inválido informado no cadastro.")

def listar_ocorrencias():
    sql = "SELECT id, data_hora, tipo, descricao, cpf_eleitor FROM auditoria ORDER BY data_hora DESC"
    conexao.cursor.execute(sql)
    resultados = conexao.cursor.fetchall()

    if not resultados:
        print("Nenhuma ocorrência registrada.")
        return
    
    for o in resultados:
        print(f"\nID: {o[0]}")
        print(f"Data/Hora: {o[1]}")
        print(f"Tipo: {o[2]}")
        print(f"Descrição: {o[3]}")
        print(f"CPF Eleitor: {o[4] if o[4] else 'N/A'}")
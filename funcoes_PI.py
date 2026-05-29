import conexao
from za import validar_titulo
import random
from datetime import datetime
votacao_aberta = False
import string

LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

MATRIZ = [[3, 5], [1, 2]]

def determinante_matriz(mat):
    return (mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]) % 36

def inversa_modular(mat, mod):
    det = determinante_matriz(mat)
    
    det_inv = -1
    for i in range(mod):
        if (det * i) % mod == 1:
            det_inv = i
            break
    
    if det_inv == -1:
        return None
    
    inv = [[0, 0], [0, 0]]
    inv[0][0] = (mat[1][1] * det_inv) % mod
    inv[0][1] = (-mat[0][1] * det_inv) % mod
    inv[1][0] = (-mat[1][0] * det_inv) % mod
    inv[1][1] = (mat[0][0] * det_inv) % mod
    
    return inv

MATRIZ_INV = inversa_modular(MATRIZ, 36)

def cifrar_bloco(a, b, mat):
    tam = len(LETRAS)
    x = (mat[0][0] * a + mat[0][1] * b) % tam
    y = (mat[1][0] * a + mat[1][1] * b) % tam
    return x, y

def criptografar(texto):
    texto = texto.upper()
    
    if len(texto) % 2 != 0:
        texto += "A"
    
    cifrado = ""
    i = 0
    
    while i < len(texto):
        a = LETRAS.index(texto[i])
        b = LETRAS.index(texto[i + 1])
        
        x, y = cifrar_bloco(a, b, MATRIZ)
        
        cifrado += LETRAS[x] + LETRAS[y]
        i += 2
    
    return cifrado

def descriptografar(texto):
    texto = texto.upper()
    
    
    if MATRIZ_INV is None:
        return "Erro: matriz não possui inversa"
    
    original = ""
    i = 0
    
    while i < len(texto):
        a = LETRAS.index(texto[i])
        b = LETRAS.index(texto[i + 1])
        
        x, y = cifrar_bloco(a, b, MATRIZ_INV)
        
        original += LETRAS[x] + LETRAS[y]
        i += 2
    
    return original

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
    """Realiza cadastro dos eleitores, solicitando a entrada de nome, título de eleitor e CPF,
      fazendo a validação dos mesmos. Além disso também verifica se o eleitor é mesário.
      Args: nenhum
      Returns: nenhum
      """

    print("\n=== CADASTRAR ELEITOR ===")
    #Entrada do nome e validação
    nome = input("Digite Seu nome completo: ").strip()
    while nome == "" or not nome.replace(" ", "").isalpha():
        print("Nome inválido. Tente digitar sem acento.")
        nome = input("Digite Seu nome completo: ").strip()
    
    #Entrada do título e validação
    titulo_eleitor = input("Digite seu titulo de eleitor: ").strip()
    titulo_eleitor = titulo_eleitor.replace(" ", "")
    while not validar_titulo(titulo_eleitor):
        print ("Título inváldo. Tente novamente.")
        titulo_eleitor = input("Digite seu titulo de eleitor: ").strip()
        titulo_eleitor = titulo_eleitor.replace(" ", "")

    titulo_existe = 1
    #verifica se o título já esta cadastrado
    while titulo_existe == 1:
        sql = "SELECT titulo_eleitor FROM eleitores WHERE titulo_eleitor = %s"
        conexao.cursor.execute(sql, (titulo_eleitor,))
        titulo_existente = conexao.cursor.fetchone()

        if titulo_existente:
            print("Este título de eleitor já está cadastrado. Digite outro título.")
            titulo_eleitor = input("Digite seu titulo de eleitor: ").strip()
            titulo_eleitor = titulo_eleitor.replace(" ", "")

            while not validar_titulo(titulo_eleitor):
                print ("Título inváldo. Tente novamente.")
                titulo_eleitor = input("Digite seu titulo de eleitor: ").strip()
                titulo_eleitor = titulo_eleitor.replace(" ", "")

        else:
            titulo_existe = 0


    #Entrada do CPF e validação
    cpf = input("Digite seu CPF: ").strip()
    cpf = cpf.replace(".", "").replace("-", "")

    
    while not validar_cpf(cpf):
        print("CPF inválido. Tente novamente.")
        cpf = input("Digite seu CPF: ").strip()
        cpf = cpf.replace(".", "").replace("-", "")

    cpf_existe = 1
    #Verificação se já existe no banco
    while cpf_existe == 1:
        sql = "SELECT cpf FROM eleitores WHERE cpf = %s"
        conexao.cursor.execute(sql, (cpf,))
        existente = conexao.cursor.fetchone()

        if existente:
            print("Este CPF já está cadastrado. Digite outro CPF.")
            cpf = input("Digite seu CPF: ").strip()
            cpf = cpf.replace(".", "").replace("-", "")

            while not validar_cpf(cpf):
                print("CPF inválido. Tente novamente.")
                cpf = input("Digite seu CPF: ").strip()
                cpf = cpf.replace(".", "").replace("-", "")
        
        else:
            cpf_existe = 0


    print("CPF válido.")
    #Geração da chave de acesso
    chave = chave_acesso(nome)
    chave_cripto = criptografar(chave)
    while chave == "":
        print("Nome inválido. Digite o nome e o sobrenome.")
        nome = input("Digite Seu nome completo: ").strip()
        chave = chave_acesso(nome)



    print(f"SUA CHAVE DE ACESSO: {chave}")
    print("Guarde sua chave de acesso, ela será necessária no momento da votação!")

    #Verifica se o eleitor vai atuar como mesário
    mesario = input("Você atuará como mesário? SIM (S) ou NÃO (N): ").strip().upper()
    while mesario not in ["S", "N"]:
        print("Digite S para SIM ou N para NÃO.")
        mesario = input("(S/N): ").strip()
        mesario = mesario.upper()

    valor_mesario = 1 if mesario == "S" else 0

    
    #Adiciona as informações no banco de dados
    sql = """
        INSERT INTO eleitores 
        (cpf, nome_completo, titulo_eleitor, chave_acesso, is_mesario)
        VALUES (%s, %s, %s, %s, %s)
    """
    cpf_cripto = criptografar(cpf)
    valores = (
        cpf_cripto,
        nome,
        titulo_eleitor,
        chave_cripto,
        valor_mesario,
        
    )

    conexao.cursor.execute(sql, valores)
    conexao.conexao.commit()

    print("Eleitor cadastrado com sucesso!")





def buscar_eleitor():
    """
    Busca um eleitor no banco de dados a partir do CPF informado
    Args: nenhum
    Return: nenhum

    
    """
    print("\n=== BUSCAR ELEITOR ===")

    continuar = "S"

    while continuar == "S":
        #Entrada do cpf para busca
        cpf = input("Digite o CPF para buscar: ")
        cpf = cpf.strip()
        cpf = cpf.replace(".", "")
        cpf = cpf.replace("-", "")

        #Validação do cpf
        while not cpf.isdigit():
            print("CPF inválido.")
            cpf = input("Digite o CPF para buscar: ").strip()
            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")

        #consulta no banco de dados
        sql = "SELECT * FROM eleitores WHERE cpf = %s"
        #Criptografa para consulta
        cpf_cripto = criptografar(cpf)
        valores = (cpf_cripto,)

        conexao.cursor.execute(sql, valores)

        resultado = conexao.cursor.fetchone()
        #Caso exista, retorna o eleitor e suas informações ja descriptografadas
        if resultado:
            cpf_real = descriptografar(resultado[1])
            chave_real = descriptografar(resultado[4])
            print("Eleitor encontrado!")
            print(f"\nID: {resultado[0]}")
            print(f"Nome Completo: {resultado[2]}")
            print(f"CPF: {cpf_real}")
            print(f"Título de Eleitor: {resultado[3]}")
            print(f"Chave de Acesso: {chave_real}")
            print(f"Mesário: {'Sim' if resultado[5] == 1 else 'Não'}")
            return

        #Caso não exista retorna eleitor nao encontrado e pergunta se deseja continuar a busca    
        else:
            print("Eleitor não encontrado.")
            continuar = input("Deseja continuar a busca? (S/N): ").strip().upper()
            while continuar not in ["S", "N"]:
                print("Digite S para SIM ou N para NÃO.")
                continuar = input("(S/N): ").strip().upper()
    print("Voltando ao menu")



def listar_eleitores():
    """
    Busca e mosstra todos os eleitores cadastrados no sistema e suas informações
    args: nenhum
    returns: nenhum
    
    
    """
    print("\n=== LISTA DE ELEITORES ===")

    # Exibe do banco de dados as informacoes de todos os eleitores cadastrados
    sql = """
        SELECT cpf, nome_completo, titulo_eleitor, is_mesario, ja_votou
        FROM eleitores
    """
    conexao.cursor.execute(sql)
    resultados = conexao.cursor.fetchall()
    # se nao tiver nenhum essa é a mensagem
    if not resultados:
        print("Nenhum eleitor cadastrado")
        return
    #se tiver, pra cada um ele exibe as informacoes em linhas diferentes
    for e in resultados:
        if e[3] == 0:
            cpf_real = descriptografar(e[0])
            print(f"\nNome: {e[1]}")
            print(f"CPF: {cpf_real}")
            print(f"Título: {e[2]}")
            print(f"Mesário: {'Sim' if e[3]== 1 else 'Não'}")
            print(f"Já votou: {'Sim' if e[4]== 1 else 'Não'}")




def remover_eleitores():
    """
    Remove eleitores cadastrados a partir de seu CPF

    args: nenhum
    returns: nenhum
    
    """
    print("\n=== REMOÇÃO DE ELEITORES ===")
    # entrada CPF
    cpf = input("Digite o CPF do eleitor que deseja remover: ")
    cpf = cpf.strip()
    cpf = cpf.replace("-", "")
    cpf = cpf.replace(".", "")

    cpf_cripto = criptografar(cpf)
    #consulta no banco de dados
    sql = "SELECT nome_completo FROM eleitores WHERE cpf = %s"
    conexao.cursor.execute(sql, (cpf_cripto,))
    eleitor = conexao.cursor.fetchone()
    #se nao achar exibe essa mensagem
    if not eleitor:
        print("Eleitor não encontrado!")
        return
    
    # se achar pede uma confirmação para o usuário 
    confirmacao = input(f"Tem certeza que deseja remover {eleitor[0]}? Sim (S) ou Não (N): ").strip()
    confirmacao = confirmacao.upper()

    # filtra a confirmação para receber apenas S ou N sem travamento
    while confirmacao not in ["S", "N"]:
        print("Digite S para SIM ou N para NÃO.")
        confirmacao = input("(S/N): ").strip()
        confirmacao = confirmacao.upper()

    if confirmacao != "S":
        print("A remoção foi cancelada!")
        return
    # deleta do banco de dados
    sql_delete = "DELETE FROM eleitores WHERE cpf = %s"
    conexao.cursor.execute(sql_delete, (cpf_cripto,))
    conexao.conexao.commit()

    print("Eleitor removido com sucesso!")




def listar_mesarios():
    """
    Busca todos os mesários do banco de dados e exibe suas informações
    args: nenhum
    returns: nenhum
    
    """
    print("\n=== LISTA DE MESÁRIOS ===")

    # consulta os mesários do banco de dados
    sql = """
        SELECT cpf, nome_completo, titulo_eleitor, is_mesario, ja_votou
        FROM eleitores WHERE is_mesario = 1
    """
    conexao.cursor.execute(sql)
    resultados = conexao.cursor.fetchall()

    # se não existir exibe essa mensagem
    if not resultados:
        print("Nenhum mesário cadastrado")
        return
    
    # pra cada mesario no banco é feita uma exibição de suas informações uma em cada linha
    for e in resultados:
        cpf_real = descriptografar(e[0])
        print(f"\nNome: {e[1]}")
        print(f"CPF: {cpf_real}")
        print(f"Título: {e[2]}")
        print(f"Mesário: {'Sim' if e[3]== 1 else 'Não'}")
        print(f"Já votou: {'Sim' if e[4]== 1 else 'Não'}")


def cadastrar_candidato():
    """
    Cadastra os candidatos pedindo nome, numero e partido
    args: nenhum
    returns: nenhum
    
    """
    print("\n=== CADASTRAR CANDIDATO ===")

    #entrada do nome e eliminação de alguns possiveis erros
    nome = input("Digite o nome do candidato: ").strip()
    while nome == "":
        print("O nome do candidato deve ser preenchido. Tente novamente.")
        nome = input("Digite o nome do candidato: ").strip()
    
    #entrada do numero e eliminação de alguns possiveis erros
    numero = input("Digite o número do candidato: ").strip()
    while not numero.isdigit():
        print("Digite apenas números. Tente novamente")
        numero = input("Digite o número do candidato: ").strip()
    
    #verifica a autenticidade do numero
    numero_int = int(numero)
    while numero_candidato(numero_int):
        print("Esse número pertence a outro candidato.")
        numero = input("Digite outro número: ").strip()
        
        while not numero.isdigit():
            print("Digite apenas números.")
            numero = input("Digite o número do candidato: ").strip()

        numero_int = int(numero)

    
    #entrada do partido e eliminação de alguns possiveis erros
    partido = input("Digite o partido do candidato: ").strip()
    while partido == "":
        print("O partido do candidato deve ser preenchido.")
        partido = input("Digite o partido do candidato: ").strip()
    
    sql = """ 
        INSERT INTO candidatos (nome, numero, partido)
        VALUES (%s, %s, %s)
    """
    valores = (nome, numero_int, partido)
    
    conexao.cursor.execute(sql, valores)
    conexao.conexao.commit()

    print("Candidato cadastrado com sucesso!!")

    



def numero_candidato(numero):
    """
    Verifica a autenticidade do numero do candidato
    args: Número do candidato
    returns: 1 se existir 0 se não 
    """
    sql = "SELECT 1 FROM candidatos WHERE numero = %s"
    conexao.cursor.execute(sql,(numero,))
    resultado = conexao.cursor.fetchone()
    if resultado:
        return 1
    else:
        return 0

    
        
def buscar_candidatos():
    """
    Consulta o banco de dados e busca todos os candidatos cadastrados
    args: nenhum
    returns: nenhum 
    
    """
    print("\n=== BUSCAR CANDIDATOS ===")

    continuar = "S"


    while continuar == "S":
        # entrada do numero do candidato para a busca
        numero = input("Digite o número do candidato que deseja buscar: ").strip()
        while not numero.isdigit():
            print("Busca inválida, digite apenas números. tente novamente.")
            numero = input("Digite o número do candidato que deseja buscar: ").strip()
            
        numero_int = int(numero)
        #consulta no banco de dados
        sql = """
            SELECT nome, numero, partido
            FROM candidatos
            WHERE numero = %s
        """
        conexao.cursor.execute(sql, (numero_int,))
        candidato = conexao.cursor.fetchone()

        #se existir imprime as informacoes do candidato
        if candidato:
            print("Candidato encontrado!")
            print(f"\nNome: {candidato[0]}")
            print(f"Número: {candidato[1]}")
            print(f"Partido: {candidato[2]}")
            return
        else:
            print("Candidato não encontrado.")

            # caso não tenha o programa exibe uma pergunta se o usuário deseja continuar a busca
        
            continuar = input("Deseja continuar a busca? (S/N): ").strip().upper()
            while continuar not in["S", "N"]:
                print("Digite S para SIM ou N para NÃO.")
                continuar = input("(S/N): ").strip().upper()
    print("Voltando ao menu")


def listar_candidatos():
    """
    Exibição de todos os candidatos cadastrados
    args: nenhum
    returns: nenhum
    
    """
    print("\n=== LISTA DE CANDIDATOS ===")
    #pega do banco todos os candidatos cadastrados
    sql = """
        SELECT nome, numero, partido
        FROM candidatos
    """
    conexao.cursor.execute(sql)
    resultados = conexao.cursor.fetchall()

    if not resultados:
        print("Nenhum candidato cadastrado.")
        return
    #se existir imprime pra cada um todas as informações
    for c in resultados:
        print(f"\nNome: {c[0]}")
        print(f"Número: {c[1]}")
        print(f"Partido: {c[2]}")


def remover_candidato():
    """
    Remove o candidato de acordo com o seu número
    args: nenhum
    returns: nenhum

    
    """
    print("\n=== REMOÇÃO DE CANDIDATOS ===")
    #entrada do numero do candidato a ser removido
    numero = input("Digite o número do candidato que deseja remover: ")
    numero = numero.strip()
    while not numero.isdigit():
        print("Digite apenas números. Tente novamente.")
        numero = input("Digite o número do candidato que deseja remover: ")
        numero = numero.strip()

    numero_int = int(numero)

    #busca do numero no banco de dados
    sql = "SELECT nome FROM candidatos WHERE numero = %s"
    conexao.cursor.execute(sql, (numero_int,))
    candidato = conexao.cursor.fetchone()

    if not candidato:
        print("Candidato não encontrado.")
        return
    # se existir exibe uma confirmação
    confirmacao = input(f"Tem certeza que deseja remover {candidato[0]}? Sim (S) ou Não (N): ").strip()
    confirmacao = confirmacao.upper()
    # filtra a confirmação para S e N
    while confirmacao not in ["S", "N"]:
        print("Digite S para SIM ou N para NÃO.")
        confirmacao = input("(S/N): ").strip()
        confirmacao = confirmacao.upper()
    # caso S remove o candidato do banco de dados
    if confirmacao != "S":
        print("A remoção foi cancelada!")
        return
    
    sql_delete = "DELETE FROM candidatos WHERE numero = %s"
    conexao.cursor.execute(sql_delete, (numero_int,))
    conexao.conexao.commit()

    print("Candidato removido com sucesso!")
    


def chave_acesso(nome_completo):
    """
    gerador da chave de acesso
    args: nome completo do eleitor
    return: chave de acesso (Mistura das duas letras do primeiro nome + primeira letra do sobrenome + 4 números aleatorios)
    
    """
    #nome completo
    nome_completo = nome_completo.strip()
    nome_completo = nome_completo.split()
    partes_nome = nome_completo

    if len(partes_nome) < 2:
        print ("Deve ser digitado o nome e o sobrenome")
        return ""
    
    
    primeiro_nome = partes_nome [0]
    segundo_nome = partes_nome [1]
    # pega as 2 primeiras letras do primeiro nome soma com a primeira do segundo nome e soma com 4 numeros aleatorios 
    letras = primeiro_nome[:2].upper() + segundo_nome[0].upper()
    numeros = f"{random.randint(0, 9999):04d}"
    return letras + numeros






def validar_mesario(titulo_eleitor, cpf4, chave):
    """
    Valida se os dados informados pertencem a um mesário de fato
    args: titulo de eleitor - INT -, os 4 primeiros digitos do cpf- INT -  e a chave de acesso -STRG-
    returns: 0 se nao for um mesário, 1 se for um mesário 
    """
    # consulta no banco de dados o mesario com o titulo de eleitor inserido
    sql = """
        SELECT cpf, chave_acesso, is_mesario
        FROM eleitores
        WHERE titulo_eleitor = %s
    """
    conexao.cursor.execute(sql, (titulo_eleitor,))
    resultado = conexao.cursor.fetchone()

    if not resultado:
        return 0

    cpf_banco = resultado[0]
    chave_banco = resultado[1]
    is_mesario = resultado[2]

    cpf_real = descriptografar(cpf_banco).strip("A")


    # valida 4 primeiros dígitos do CPF
    if cpf_real[:4] != cpf4:
        return 0

    # valida chave
    chave_real = descriptografar(chave_banco).strip("A")
    if chave_real != chave:
        return 0

    # valida se é mesário
    if is_mesario != 1:
        return 0

    return 1







def zerezima():
    """
    Zera todos os votos recebidos pelos candidatos assim como o status ja_votou dos eleitores voltam a ser zero
    args: nenhum
    returns: nenhum

    """
    print("\n=== REALIZANDO A ZERÉZIMA ===")
    # deleta informacoes do banco de dados
    conexao.cursor.execute("DELETE FROM voto")
    #atualiza todos os eleitores one o ja_votou é 1 pra 0
    conexao.cursor.execute("UPDATE eleitores SET ja_votou = FALSE")


    conexao.conexao.commit()

    sql = "SELECT nome, numero FROM candidatos ORDER BY nome ASC"
    conexao.cursor.execute(sql)
    candidatos = conexao.cursor.fetchall()

    if not candidatos:
        print("Nenhum candidato cadastrado.")
    else:
        for c in candidatos:
            print(f"{c[0]} ({c[1]}) | 0 votos")

    

    print("\nZerézima realizada com sucesso. Sistema pronto para votação.")
    registrar_log("Votação iniciada com sucesso. Votos zerados.")






def abrir_votacao():
    """
    Realiza a abertura da votação - informações sobre o mesario que vai abrir e verificação
    args: nenhum
    returns: nenhum
    
    
    """
    # faz uma verificação pra caso haja erro de digitação o usuario digite novamente antes de seguir(titulo de eleitor)
    titulo_valido = 0
    while titulo_valido ==0:
        titulo = input("Título: ").strip()

        while titulo == "":
            print("Título inválido. Tente novamente.")
            titulo = input("Título: ").strip()
        sql = "SELECT id, cpf, chave_acesso FROM eleitores WHERE titulo_eleitor = %s AND is_mesario = 1"
        conexao.cursor.execute(sql,(titulo,))
        mesario = conexao.cursor.fetchone()
        conexao.cursor.fetchall()

        if mesario:
            titulo_valido = 1
        else:
            print("Título não encontrado ou não é mesário.")
    
# faz uma verificação pra caso haja erro de digitação o usuario digite novamente antes de seguir(cpf(4 digitos))
    cpf_valido = 0

    while cpf_valido == 0:
        cpf4 = input("CPF (4 dígitos): ").strip()

        while not cpf4.isdigit() or len(cpf4) != 4:
            print("CPF inválido. Digite 4 números.")
            cpf4 = input("CPF (4 dígitos): ").strip()
        cpf_banco = descriptografar(mesario[1]).rstrip("A")

        if cpf_banco[:4] == cpf4:
            cpf_valido = 1
        else:
            print("CPF incorreto.")
    
# faz uma verificação pra caso haja erro de digitação o usuario digite novamente antes de seguir (chave de acesso)
    chave_valida = 0
    while chave_valida == 0:
        chave = input("Chave: ").strip()

        while chave == "":
            print("Chave inválida.")
            chave = input("Chave: ").strip()
        chave_real = descriptografar(mesario[2]).rstrip("A")
        if chave_real.upper() == chave.upper():
            chave_valida = 1
        else:
            print("Chave incorreta.")    

    if not validar_mesario(titulo, cpf4, chave):
        print("Acesso negado.")
        return 0
    
    

    print("Mesário autenticado com sucesso!")
    zerezima()


    registrar_log("Abertura da votação concluída.")

    print("Votação Aberta.")

    return 1




def encerrar_votacao():
    """
    Encerramento da votação, informações do mesário que vai encerrar e verificação
    args: 0
    returns: nenhum
    
    
    """

    print("\n=== ENCERRAR VOTAÇÃO ===")
    # faz uma verificação pra caso haja erro de digitação o usuario digite novamente antes de seguir (titulo eleitor)
    titulo_valido = 0
    while titulo_valido == 0:
        titulo = input("Título de eleitor: ").strip()

        while titulo == "":
            print("Título inválido. Tente novamente.")
            titulo = input("Título: ").strip()
        sql = "SELECT id, cpf, chave_acesso FROM eleitores WHERE titulo_eleitor = %s AND is_mesario = 1"
        conexao.cursor.execute(sql,(titulo,))
        mesario = conexao.cursor.fetchone()
        conexao.cursor.fetchall()

        if mesario:
            titulo_valido = 1
        else:
            print("Título não encontrado ou não é mesário.")

# faz uma verificação pra caso haja erro de digitação o usuario digite novamente antes de seguir (cpf)
    cpf_valido = 0
    while cpf_valido == 0:    
        cpf4 = input("4 primeiros dígitos do CPF: ")

        while not cpf4.isdigit() or len(cpf4) != 4:
            print("CPF inválido. Digite 4 números.")
            cpf4 = input("CPF (4 dígitos): ").strip()
        cpf_banco = descriptografar(mesario[1]).rstrip("A")
        if cpf_banco[:4] == cpf4:
            cpf_valido = 1
        else:
            print("CPF incorreto.")
# faz uma verificação pra caso haja erro de digitação o usuario digite novamente antes de seguir (chave)
    chave_valida = 0
    while chave_valida == 0:
        chave = input("Chave de acesso: ")

        while chave == "":
            print("Chave inválida.")
            chave = input("Chave: ").strip()
        chave_real = descriptografar(mesario[2]).rstrip("A")
        if chave_real.upper() == chave.upper():
            chave_valida = 1
        else:
            print("Chave incorreta.") 



    if not validar_mesario(titulo, cpf4, chave):
        print("Validação não realizada")
        registrar_log("Tentativa de acesso negado.")
        return 0
    
    
#confirmação se realmente for para encerrar
    confirm = input("Deseja realmente encerrar? SIM (S) ou NÃO(N): ").strip().upper()

    while confirm not in ["S", "N"]:
        print("Digite S para SIM ou N para NÃO.")
        confirm = input("Deseja realmente encerrar? (S/N): ").strip().upper()


    if confirm != "S":
        print("Encerramento cancelado")
        return 0

    chave2 = input("Digite novamente a chave de acesso: ").strip()

    while chave2 == "":
        print("Chave inválida.")
        chave2 = input("Digite novamente a chave de acesso: ").strip()

    if chave2 != chave:
        print("Chave incorreta")
        return 0
    
    

    registrar_log("Encerramento da votação concluído.")

    print("Votação encerrada com sucesso!")
    return 1


def votar():
    """
    Hora do voto
    args: nenhum
    returns: nenhum
    
    """

    print("\n=== IDENTIFICAÇÃO DO ELEITOR ===")
## faz uma verificação pra caso haja erro de digitação o usuario digite novamente antes de seguir
    titulo_valido = 0


    while titulo_valido == 0:
        titulo = input("Título de eleitor: ").strip()

        while titulo == "":
            print("Título inválido.")
            titulo = input("Título de eleitor: ").strip()
        
        sql = "SELECT id, ja_votou, chave_acesso, cpf FROM eleitores WHERE titulo_eleitor = %s"

        conexao.cursor.execute(sql,(titulo,))
        eleitor = conexao.cursor.fetchone()
        if eleitor:
            titulo_valido = 1
        else:
            print("Título não encontrado.")
    # faz uma verificação pra caso haja erro de digitação o usuario digite novamente antes de seguir
    cpf_valido = 0

    while cpf_valido == 0:
        cpf = input("4 primeiros dígitos do CPF: ").strip()

        while not cpf.isdigit() or len(cpf) != 4:
            print("CPF inválido. Digite 4 números.")
            cpf = input("4 primeiros dígitos do CPF: ").strip()
        cpf_banco = descriptografar(eleitor[3]).rstrip("A")
        if cpf_banco[:4] == cpf:
            cpf_valido = 1
        else:
            print("CPF não corresponde ao título.")
    # faz uma verificação pra caso haja erro de digitação o usuario digite novamente antes de seguir
    chave_valida = 0

    while chave_valida == 0:
        chave = input("Chave de acesso: ").strip()

        while chave == "":
            print("Chave inválida.")
            chave = input("Chave de acesso: ").strip()
        chave_real = descriptografar(eleitor[2]).rstrip("A")
        if chave_real.strip().upper() == chave.strip().upper():
            chave_valida = 1
        else:
            print("Chave incorreta.")
#verifica se o eleitor ja votou, se sim não poderá votar novamente
    if eleitor[1] == 1:
        print("Este eleitor já votou.")
        registrar_log("Tentativa de votar novamente (voto duplo).")
        return

    #numero do candidato que deseja votar
    numero = input("\nDigite o número do candidato: ").strip()
    #valida o número
    while not numero.isdigit():
        print("Número inválido. Digite apenas números.")
        numero = input("Digite o número do candidato: ").strip()
    numero = int(numero)
    #mostra o candidato selecionado
    sql = """
        SELECT id, nome, partido
        FROM candidatos
        WHERE numero = %s
    """
    
    conexao.cursor.execute(sql, (numero,))
    candidato = conexao.cursor.fetchone()

   
    #pede confirmação do voto
    if candidato:
        print(f"Candidato: {candidato[1]} - {candidato[2]}")
        confirmar = input("Confirmar voto? SIM (S) ou NÃO (N): ").strip().upper()

    #caso nao exista o número consultado, o voto sera contado como nulo
    else:
        print("Número inválido. Voto será NULO.")
        candidato = None
        confirmar = input("Confirmar voto nulo? SIM (S) ou NÃO (N): ").strip().upper()

    #filtro de confirmação
    if confirmar == "SIM":
        confirmar = "S"
    elif confirmar in ["NAO", "NÃO"]:
        confirmar = "N"

    while confirmar not in ["S", "N"]:
        print("Digite S para SIM ou N para NÃO.")
        confirmar = input("(S/N): ").strip().upper()

        if confirmar == "SIM":
            confirmar = "S"
        elif confirmar in ["NAO", "NÃO"]:
            confirmar = "N"

    #pede o numero do candidato até que a confirmação seja S
    while confirmar != "S":

        numero = input("\nDigite o número do candidato: ").strip()

        while not numero.isdigit():
            print("Número inválido.")
            numero = input("Digite o número do candidato: ").strip()

        conexao.cursor.execute(sql, (numero,))
        candidato = conexao.cursor.fetchone()

        if candidato:
            print(f"Candidato: {candidato[1]} - {candidato[2]}")
            confirmar = input("Confirmar voto? SIM (S) ou NÃO (N): ").strip().upper()
        else:
            print("Número inválido. Voto será NULO.")
            candidato = None
            confirmar = input("Confirmar voto nulo? SIM (S) ou NÃO (N): ").strip().upper()

        if confirmar == "SIM":
            confirmar = "S"
        elif confirmar in ["NAO", "NÃO"]:
            confirmar = "N"

        while confirmar not in ["S", "N"]:
            print("Digite S para SIM ou N para NÃO.")
            confirmar = input("(S/N): ").strip().upper()

            if confirmar == "SIM":
                confirmar = "S"
            elif confirmar in ["NAO", "NÃO"]:
                confirmar = "N"

    if candidato:
        candidato_id = candidato[0]
    else:
        candidato_id = None                


    #protocolo 
    letras=''.join(random.choice(string.ascii_uppercase) for _ in range(2))
    if candidato_id is None:
        numero_str="00"
    else:
        numero_str=str(numero).zfill(2)

    aleatorio=f"{random.randint(0,99999):05d}"
    protocolo =f"V{letras}26{numero_str}{aleatorio}" 

    protocolo_cripto = criptografar(protocolo)


    data_hora = datetime.now()


    sql_voto = """
        INSERT INTO voto (candidato_id, data_hora, protocolo)
        VALUES (%s, %s, %s)
    """
    conexao.cursor.execute(sql_voto, (candidato_id, data_hora, protocolo_cripto))

    
    sql_update = "UPDATE eleitores SET ja_votou = TRUE WHERE id = %s"
    conexao.cursor.execute(sql_update, (eleitor[0],))

    conexao.conexao.commit()

    print("\nVOTO REGISTRADO COM SUCESSO")
    print(f"Protocolo de votação: {protocolo}")
    registrar_log("Voto realizado.")





def registrar_log(mensagem):
    """
    Registrar as ações que necessitam ser registradas, abre um arquivo txt para registra-las
    args: mensagens - STRG-
    return:nenhum
    
    """
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    arquivo = open("auditoria.txt", "a", encoding="utf-8")
    arquivo.write("[" + data_hora + "] " + mensagem + "\n")
    arquivo.close()


def exibir_logs():
    """
    Exibe as ações que foram registradas no arquivo txt
    args: nenhum
    returns: nenhum
    """
    arquivo = open("auditoria.txt", "r", encoding="utf-8")
    conteudo = arquivo.read()

    print("\n=== LOGS DE AUDITORIA ===")
    print(conteudo)

    arquivo.close()






def editar_candidato():
    """
    Edição de informações do candidato como mudança de número ou partido
    args: nenhum
    returns: nenhum 
    
    """

    print("\n=== EDITAR CANDIDATO ===")
    # número do candidato a ser atualizado
    numero = input("Digite o número do candidato: ").strip()
#filtragem para receber apenas números
    while not numero.isdigit():
        print("Digite apenas números.")
        numero = input("Digite o número do candidato: ").strip()

    numero_int = int(numero)
# consulta o candidato no banco de dados
    sql = "SELECT id, nome, numero, partido FROM candidatos WHERE numero = %s"
    conexao.cursor.execute(sql, (numero_int,))
    candidato = conexao.cursor.fetchone()

    if not candidato:
        print("Candidato não encontrado.")
        return
# caso encontre, pede pra colocar as novas informações
    print(f"\nCandidato encontrado: {candidato[1]}")

    nome = input("Digite o novo nome: ").strip()

    while nome == "":
        print("Nome inválido.")
        nome = input("Digite o novo nome: ").strip()

    novo_numero = input("Digite o novo número: ").strip()

    while not novo_numero.isdigit():
        print("Digite apenas números.")
        novo_numero = input("Digite o novo número: ").strip()

    novo_numero_int = int(novo_numero)

    numero_existe = 1
# verifica a autenticidade do número ao consultar a existência no banco de dados e pede um novo número até ser único
    while numero_existe == 1:
        sql = "SELECT id FROM candidatos WHERE numero = %s"
        conexao.cursor.execute(sql, (novo_numero_int,))
        existente = conexao.cursor.fetchone()

        if existente and existente[0] != candidato[0]:
            print("Esse número já pertence a outro candidato.")

            novo_numero = input("Digite outro número: ").strip()

            while not novo_numero.isdigit():
                print("Digite apenas números.")
                novo_numero = input("Digite o número: ").strip()

            novo_numero_int = int(novo_numero)
        else:
            numero_existe = 0

    partido = input("Digite o novo partido: ").strip()

    while partido == "":
        print("Partido inválido.")
        partido = input("Digite o novo partido: ").strip()

    confirm = input("Deseja salvar? (S/N): ").strip().upper()

    while confirm not in ["S", "N"]:
        print("Digite S ou N.")
        confirm = input("(S/N): ").strip().upper()

    if confirm != "S":
        print("Edição cancelada.")
        return
# comando UPDATE para atualizar as informações
    sql_update = """
        UPDATE candidatos
        SET nome = %s, numero = %s, partido = %s
        WHERE id = %s
    """

    valores = (nome, novo_numero_int, partido, candidato[0])

    conexao.cursor.execute(sql_update, valores)
    conexao.conexao.commit()

    print("Candidato atualizado com sucesso!")


def editar_eleitor():
    """
    Edição de informações do eleitor como mudança de nome, titulo 
    args: nenhum
    returns: nenhum
    """
    print("\n=== EDITAR ELEITOR ===")
# busca do eleitor pelo seu CPF
    cpf = input("Digite o CPF: ").strip()
    cpf = cpf.replace(".", "").replace("-", "")

    while not cpf.isdigit():
        print("Digite apenas números.")
        cpf = input("Digite o CPF: ").strip()
        cpf = cpf.replace(".", "").replace("-", "")

    cpf_cripto = criptografar(cpf)
    sql = "SELECT id, nome_completo, titulo_eleitor, is_mesario FROM eleitores WHERE cpf = %s"
    conexao.cursor.execute(sql, (cpf_cripto,))
    eleitor = conexao.cursor.fetchone()

    if not eleitor:
        print("Eleitor não encontrado.")
        return
# após encontrar o eleitor começa a pedir as novas informações
    print(f"\nEleitor encontrado: {eleitor[1]}")

    nome = input("Digite o novo nome: ").strip()

    while nome == "":
        print("Nome inválido.")
        nome = input("Digite o novo nome: ").strip()

    titulo = input("Digite o novo título: ").strip()
    titulo = "".join(t for t in titulo if t.isdigit())
# valida o titulo de eleitor novo
    while not validar_titulo(titulo):
        print("Título inválido.")
        titulo = input("Digite o novo título: ").strip()
        titulo = "".join(t for t in titulo if t.isdigit())

    titulo_existe = 1
#verifica se o titulo de eleitor novo é único
    while titulo_existe == 1:
        sql = "SELECT id FROM eleitores WHERE titulo_eleitor = %s"
        conexao.cursor.execute(sql, (titulo,))
        existente = conexao.cursor.fetchone()

        if existente and existente[0] != eleitor[0]:
            print("Esse título já pertence a outro eleitor.")

            titulo = input("Digite outro título: ").strip()
            titulo = "".join(t for t in titulo if t.isdigit())

            while not validar_titulo(titulo):
                print("Título inválido.")
                titulo = input("Digite o novo título: ").strip()
                titulo = "".join(t for t in titulo if t.isdigit())
        else:
            titulo_existe = 0

    mesario = input("Deseja ser mesário? (S/N): ").strip().upper()

    while mesario not in ["S", "N"]:
        print("Digite S ou N.")
        mesario = input("(S/N): ").strip().upper()

    valor_mesario = 1 if mesario == "S" else 0

    confirm = input("Deseja salvar? (S/N): ").strip().upper()

    while confirm not in ["S", "N"]:
        print("Digite S ou N.")
        confirm = input("(S/N): ").strip().upper()

    if confirm != "S":
        print("Edição cancelada.")
        return
# atualiza as informações do eleitor no banco de dados
    sql_update = """
        UPDATE eleitores
        SET nome_completo = %s, titulo_eleitor = %s, is_mesario = %s
        WHERE id = %s
    """

    valores = (nome, titulo, valor_mesario, eleitor[0])

    conexao.cursor.execute(sql_update, valores)
    conexao.conexao.commit()

    print("Eleitor atualizado com sucesso!")



def tornar_mesario():
    """
    Tornar um eleitor mesário, a partir de seu CPF
    args: nenhum
    returns: nenhum
    """
    print("\n=== TORNAR ELEITOR MESÁRIO ===")
# pede o CPF do eleitor
    cpf = input("Digite o CPF do eleitor: ").strip()
    cpf = cpf.replace('.', '')
    cpf = cpf.replace('-', '')

    while not cpf.isdigit():
        print("CPF inválido. Digite apenas números")
        cpf = input("Digite o CPF do eleitor: ").strip()
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
# consulta no banco de dados
    cpf_cripto = criptografar(cpf)
    sql = "SELECT id, nome_completo, is_mesario FROM eleitores WHERE cpf = %s"
    conexao.cursor.execute(sql, (cpf_cripto,))
    eleitor = conexao.cursor.fetchone()

    if not eleitor:
        print("Eleitor não encontrado.")
        registrar_log("Tentativa de tornar mesário um eleitor não existente.")
        return
    # caso o eleitor já for um mesário aparece essa mensagem
    if eleitor[2] == 1:
        print(f"{eleitor[1]} já é mesário.")
        return
    #confirmação se realmente deseja tornar o eleitor um mesário 
    confirmacao = input(f"Deseja tornar {eleitor[1]} um mesário? Sim (S) ou Não (N)").strip().upper()

    while confirmacao not in ["S", "N"]:
        print("Digite S ou N.")
        confirmacao = input("(S/N): ").strip().upper()

    if confirmacao != "S":
        print("Operação cancelada.")
        return
    #atualiza a informação nova no banco de dados
    sql_update = "UPDATE eleitores SET is_mesario = TRUE WHERE id = %s"
    conexao.cursor.execute(sql_update, (eleitor[0],))
    conexao.conexao.commit()

    print(f"{eleitor[1]} agora é mesário!")

    registrar_log("Eleitor promovido a mesário.")


def boletim_urna():
    """
    Resultados da votação, pega quantos votos cada um dos candidatos teve e quantos votos foram nulo 
    args: nenhum
    returns: nenhum 
    
    """
    print("\n=== BOLETIM DE URNA ===")
# chama no banco de dados e pega todas as informações do candidato, juntando seu id e a quantidade de votos que ele conquistou
    sql = """ 
        SELECT c.nome, c.numero, c.partido, COUNT(v.id) as total
        FROM candidatos c
        LEFT JOIN voto v ON c.id = v.candidato_id
        GROUP BY c.id
        ORDER BY c.nome


    """

    conexao.cursor.execute(sql)
    resultados = conexao.cursor.fetchall()

    maior_votos = -1
    vencedores = []
# exibe a quantidade de votos de cada candidato
    for c in resultados:
        print(f"{c[0]} ({c[1]}) - {c[2]} | {c[3]} voto(s)")
# a cada candidato verifica-se se a quantidade de votos foi maior do que a do anterior
        if c[3] > maior_votos:
            maior_votos = c[3]
            vencedores = [c]

        elif c[3] == maior_votos:
            vencedores.append(c)
    # votos nulo 
    sql_nulo = "SELECT COUNT(*) FROM voto WHERE candidato_id IS NULL"
    conexao.cursor.execute(sql_nulo)
    votos_nulos = conexao.cursor.fetchone()[0]
    print(f"NULO - {votos_nulos} voto (s)")
        
    print("\n=== RESULTADO FINAL ===")
# resultado final caso só haja 1 vencedor
    if len(vencedores) == 1:
        v = vencedores[0]
        print(f"VENCEDOR: {v[0]} ({v[1]}) - {v[2]}")
        print(f"Total de votos: {v[3]}")
# resultado caso dois candidatos tenham a mesma quantidade de votos
    else:
        print("EMPATE ENTRE:")
        for v in vencedores:
            print(f"{v[0]} ({v[1]}) - {v[2]} | {v[3]} votos")


        

def estatisticas_comparecimento():
    """
    Verifica quantos eleitores estão cadastrados e quantos eleitores compareceram para votar
    args: nenhum
    returns: nenhum
    """
    print("\n=== ESTATÍSTICAS DE COMPARECIMENTO ===")
# conta a quantidade de eleitores cadastrados
    sql_total = "SELECT COUNT(*) FROM eleitores"
    conexao.cursor.execute(sql_total)
    total = conexao.cursor.fetchone()[0]
# conta quantos eleitores ja votaram
    sql_votaram = "SELECT COUNT(*) FROM eleitores WHERE ja_votou = 1"
    conexao.cursor.execute(sql_votaram)
    votaram = conexao.cursor.fetchone()[0]

    if total == 0:
        print("Nenhum eleitor cadastrado.")
        return
    # calcula a porcentagem de eleitores que compareceram
    percentual = (votaram / total) * 100
    print(f"Total de eleitores: {total}")
    print(f"Eleitores que votaram: {votaram}")
    print(f"Comparecimento: {percentual:.2f}%")

def votos_por_partido():
    """
    Calcula a quantidade de votos que cada partido recebeu 
    args: nenhum
    returns: nenhum
    
    """
# consulta no banco de dados as quantidades de voto por partido 
    sql = """
        SELECT 
            c.partido, 
            COUNT(v.id) AS total_votos
        FROM candidatos c
        LEFT JOIN voto v ON c.id = v.candidato_id
        GROUP BY c.partido
        ORDER BY total_votos DESC
    """

    conexao.cursor.execute(sql)
    resultados = conexao.cursor.fetchall()

    print("\n=== VOTOS POR PARTIDO ===")
#exibe a quantidade de votos, caso nao tenha nenhum exibe isso
    if not resultados:
        print("Nenhum dado disponível.")
        return
# caso tenha imprime o partido e sua quantidade
    for r in resultados:
        partido = r[0]
        votos = r[1]
        print(f"Partido: {partido} -> {votos} votos") 
    

def validar_integridade():
    """
    Valida a integridade da votação, se teve votos equivalentes a pessoas votando e nenhum tipo de voto duplo ou manipulação
    args: nenhum
    returns: nenhum
    """
    #conta a quantidade de votos
    sql_votos = "SELECT COUNT(*) FROM voto"
    conexao.cursor.execute(sql_votos)
    total_votos = conexao.cursor.fetchone()[0]

    #conta a quantidade de eleitores que votaram
    sql_eleitores = "SELECT COUNT(*) FROM eleitores WHERE ja_votou = TRUE"
    conexao.cursor.execute(sql_eleitores)
    total_eleitores = conexao.cursor.fetchone()[0]

    print("\n=== VALIDAÇÃO DE INTEGRIDADE ===")
# imprime as quantidades
    print(f"Total de votos registrados: {total_votos}")
    print(f"Total de eleitores que votaram: {total_eleitores}")

    # se for igual as quantidades não existem inconsistencias, caso contrario existe divergencia
    if total_votos == total_eleitores:
        print("\nINTEGRIDADE CONFIRMADA")
        print("Não há inconsistências no sistema.")
    else:
        print("\nERRO DE INTEGRIDADE")
        print("Há divergência entre votos e eleitores.")




def exibir_protocolos():
    """
    Exibe os protocolos de votação 
    args: nenhun
    returns: nenhum
    
    """
    print("\n=== PROTOCOLOS DE VOTAÇÃO ===")
    
    # pega do banco de dados os protocolos
    conexao.cursor.execute("SELECT protocolo FROM voto")
    resultados = conexao.cursor.fetchall()

    if not resultados:
        print("Nenhum protocolo encontrado.")
        return
    # coloca numa lista os protocolos ja descriptografados
    protocolos = []
    for p in resultados:
        protocolo_real = descriptografar(p[0]).strip("A")
        protocolos.append(protocolo_real)
    # coloca em ordem alfabetica
    protocolos.sort()
# imprime os protocolos
    for protocolo in protocolos:
        print(protocolo)
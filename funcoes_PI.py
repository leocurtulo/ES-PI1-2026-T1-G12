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
    print("\n=== CADASTRAR ELEITOR ===")

    nome = input("Digite Seu nome completo: ").strip()
    while nome == "":
        print("Nome inválido. Tente novamente.")
        nome = input("Digite Seu nome completo: ").strip()
    

    titulo_eleitor = input("Digite seu titulo de eleitor: ").strip()
    titulo_eleitor = titulo_eleitor.replace(" ", "")
    while not validar_titulo(titulo_eleitor):
        print ("Título inváldo. Tente novamente.")
        titulo_eleitor = input("Digite seu titulo de eleitor: ").strip()
        titulo_eleitor = titulo_eleitor.replace(" ", "")

    titulo_existe = True

    while titulo_existe:
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
            titulo_existe = False



    cpf = input("Digite seu CPF: ").strip()
    cpf = cpf.replace(".", "").replace("-", "")

    
    while not validar_cpf(cpf):
        print("CPF inválido. Tente novamente.")
        cpf = input("Digite seu CPF: ").strip()
        cpf = cpf.replace(".", "").replace("-", "")

    cpf_existe = True

    while cpf_existe:
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
            cpf_existe = False


    print("CPF válido.")

    chave = chave_acesso(nome)
    chave_cripto = criptografar(chave)
    while chave == "":
        print("Nome inválido. Digite o nome e o sobrenome.")
        nome = input("Digite Seu nome completo: ").strip()
        chave = chave_acesso(nome)



    print(f"SUA CHAVE DE ACESSO: {chave}")
    print("Guarde sua chave de acesso, ela será necessária no momento da votação!")

    mesario = input("Você atuará como mesário? SIM (S) ou NÃO (N): ").strip().upper()
    while mesario not in ["S", "N"]:
        print("Digite S para SIM ou N para NÃO.")
        mesario = input("(S/N): ").strip()
        mesario = mesario.upper()

    valor_mesario = True if mesario == "S" else False

    

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
    print("\n=== BUSCAR ELEITOR ===")

    cpf = input("Digite o CPF para buscar: ")
    cpf = cpf.strip()
    cpf = cpf.replace(".", "")
    cpf = cpf.replace("-", "")

    while not cpf.isdigit():
        print("CPF inválido.")
        cpf = input("Digite o CPF para buscar: ").strip()
        cpf = cpf.replace(".", "")
        cpf = cpf.replace("-", "")


    sql = "SELECT * FROM eleitores WHERE cpf = %s"

    cpf_cripto = criptografar(cpf)
    valores = (cpf_cripto,)

    conexao.cursor.execute(sql, valores)

    resultado = conexao.cursor.fetchone()

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
        
    else:
        print("Eleitor não encontrado.")




def listar_eleitores():
    print("\n=== LISTA DE ELEITORES ===")

    
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
            cpf_real = descriptografar(e[0])
            print(f"\nNome: {e[1]}")
            print(f"CPF: {cpf_real}")
            print(f"Título: {e[2]}")
            print(f"Mesário: {'Sim' if e[3]== 1 else 'Não'}")
            print(f"Já votou: {'Sim' if e[4]== 1 else 'Não'}")




def remover_eleitores():
    print("\n=== REMOÇÃO DE ELEITORES ===")

    cpf = input("Digite o CPF do eleitor que deseja remover: ")
    cpf = cpf.strip()
    cpf = cpf.replace("-", "")
    cpf = cpf.replace(".", "")

    cpf_cripto = criptografar(cpf)

    sql = "SELECT nome_completo FROM eleitores WHERE cpf = %s"
    conexao.cursor.execute(sql, (cpf_cripto,))
    eleitor = conexao.cursor.fetchone()

    if not eleitor:
        print("Eleitor não encontrado!")
        return
    confirmacao = input(f"Tem certeza que deseja remover {eleitor[0]}? Sim (S) ou Não (N): ").strip()
    confirmacao = confirmacao.upper()

    while confirmacao not in ["S", "N"]:
        print("Digite S para SIM ou N para NÃO.")
        confirmacao = input("(S/N): ").strip()
        confirmacao = confirmacao.upper()

    if confirmacao != "S":
        print("A remoção foi cancelada!")
        return
    
    sql_delete = "DELETE FROM eleitores WHERE cpf = %s"
    conexao.cursor.execute(sql_delete, (cpf_cripto,))
    conexao.conexao.commit()

    print("Eleitor removido com sucesso!")




def listar_mesarios():
    print("\n=== LISTA DE MESÁRIOS ===")

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
        cpf_real = descriptografar(e[0])
        print(f"\nNome: {e[1]}")
        print(f"CPF: {cpf_real}")
        print(f"Título: {e[2]}")
        print(f"Mesário: {'Sim' if e[3]== 1 else 'Não'}")
        print(f"Já votou: {'Sim' if e[4]== 1 else 'Não'}")


def cadastrar_candidato():
    print("\n=== CADASTRAR CANDIDATO ===")

    nome = input("Digite o nome do candidato: ").strip()
    while nome == "":
        print("O nome do candidato deve ser preenchido. Tente novamente.")
        nome = input("Digite o nome do candidato: ").strip()
    
    numero = input("Digite o número do candidato: ").strip()
    while not numero.isdigit():
        print("Digite apenas números. Tente novamente")
        numero = input("Digite o número do candidato: ").strip()
        
    numero_int = int(numero)
    while numero_candidato(numero_int):
        print("Esse número pertence a outro candidato.")
        numero = input("Digite outro número: ").strip()
        
        while not numero.isdigit():
            print("Digite apenas números.")
            numero = input("Digite o número do candidato: ").strip()

        numero_int = int(numero)

    

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
    sql = "SELECT 1 FROM candidatos WHERE numero = %s"
    conexao.cursor.execute(sql,(numero,))
    resultado = conexao.cursor.fetchone()
    if resultado:
        return True 
    else:
        return False

    
        
def buscar_candidatos():
    print("\n=== BUSCAR CANDIDATOS ===")

    numero = input("Digite o número do candidato que deseja buscar: ").strip()
    while not numero.isdigit():
        print("Busca inválida, digite apenas números. tente novamente.")
        numero = input("Digite o número do candidato que deseja buscar: ").strip()
        
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
    print("\n=== LISTA DE CANDIDATOS ===")

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
    print("\n=== REMOÇÃO DE CANDIDATOS ===")

    numero = input("Digite o número do candidato que deseja remover: ")
    numero = numero.strip()
    while not numero.isdigit():
        print("Digite apenas números. Tente novamente.")
        numero = input("Digite o número do candidato que deseja remover: ")
        numero = numero.strip()

    numero_int = int(numero)


    sql = "SELECT nome FROM candidatos WHERE numero = %s"
    conexao.cursor.execute(sql, (numero_int,))
    candidato = conexao.cursor.fetchone()

    if not candidato:
        print("Candidato não encontrado.")
        return

    confirmacao = input(f"Tem certeza que deseja remover {candidato[0]}? Sim (S) ou Não (N): ").strip()
    confirmacao = confirmacao.upper()

    while confirmacao not in ["S", "N"]:
        print("Digite S para SIM ou N para NÃO.")
        confirmacao = input("(S/N): ").strip()
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
        return ""
    
    
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

    cpf_real = descriptografar(cpf_banco).strip("A")


    # valida 4 primeiros dígitos do CPF
    if cpf_real[:4] != cpf4:
        return False

    # valida chave
    chave_real = descriptografar(chave_banco).strip("A")
    if chave_real != chave:
        return False

    # valida se é mesário
    if is_mesario != 1:
        return False

    return True







def zerezima():
    print("\n=== REALIZANDO A ZERÉZIMA ===")

    conexao.cursor.execute("DELETE FROM voto")# limpar votos
    conexao.conexao.commit()

    sql = "SELECT nome, numero FROM candidatos ORDER BY nome"
    conexao.cursor.execute(sql)
    candidatos = conexao.cursor.fetchall()

    for c in candidatos:
        print(f"{c[0]} ({c[1]}) - 0 votos")

    print("\nZerézima realizada com sucesso, todos os votos foram zerados.")






def abrir_votacao():
    global votacao_aberta

    titulo = input("Título: ")

    while titulo == "":
        print("Título inválido. Tente novamente.")
        titulo = input("Título: ").strip()


    cpf4 = input("CPF (4 dígitos): ")

    while not cpf4.isdigit() or len(cpf4) != 4:
        print("CPF inválido. Digite 4 números.")
        cpf4 = input("CPF (4 dígitos): ").strip()


    chave = input("Chave: ")

    while chave == "":
        print("Chave inválida.")
        chave = input("Chave: ").strip()

    if not validar_mesario(titulo, cpf4, chave):
        print("Acesso negado.")
        return False
    
    if votacao_aberta:
        print("A votação já está aberta.")
        registrar_log("Tentativa de abrir votação já aberta.")
        return False
    

    print("Mesário autenticado com sucesso!")
    zerezima()

    votacao_aberta = True

    registrar_log("Abertura da votação concluída.")

    print("Votação Aberta.")

    return True




def encerrar_votacao():
    global votacao_aberta


    print("\n=== ENCERRAR VOTAÇÃO ===")

    titulo = input("Título de eleitor: ")

    while titulo == "":
        print("Título inválido. Tente novamente.")
        titulo = input("Título: ").strip()

        
    cpf4 = input("4 primeiros dígitos do CPF: ")

    while not cpf4.isdigit() or len(cpf4) != 4:
        print("CPF inválido. Digite 4 números.")
        cpf4 = input("CPF (4 dígitos): ").strip()

    chave = input("Chave de acesso: ")

    while chave == "":
        print("Chave inválida.")
        chave = input("Chave: ").strip()


    if not validar_mesario(titulo, cpf4, chave):
        print("Validação não realizada")
        registrar_log("Tentativa de acesso negado.")
        return
    
    if not votacao_aberta:
        print("A votação já está encerrada.")
        return
    

    confirm = input("Deseja realmente encerrar? SIM (S) ou NÃO(N): ").strip().upper()

    while confirm not in ["S", "N"]:
        print("Digite apenas SIM ou NÃO.")
        confirm = input("Deseja realmente encerrar? (SIM/NÃO): ").strip().upper()


    if confirm != "S":
        print("Encerramento cancelado")
        return

    chave2 = input("Digite novamente a chave de acesso: ")

    while chave == "":
        print("Chave inválida.")
        chave2 = input("Digite novamente a chave de acesso: ").strip()

    if chave2 != chave:
        print("Chave incorreta")
        return
    
    votacao_aberta = False

    registrar_log("Encerramento da votação concluído.")

    print("Votação encerrada com sucesso!")



def votar():
    if not votacao_aberta:
        print("A votação está fechada.")
        return

    print("\n=== IDENTIFICAÇÃO DO ELEITOR ===")

    titulo = input("Título de eleitor: ").strip()

    while titulo == "":
        print("Título inválido.")
        titulo = input("Título de eleitor: ").strip()

    cpf = input("4 primeiros dígitos do CPF: ").strip()

    while not cpf.isdigit() or len(cpf) != 4:
        print("CPF inválido. Digite 4 números.")
        cpf = input("4 primeiros dígitos do CPF: ").strip()

    chave = input("Chave de acesso: ").strip()

    while chave == "":
        print("Chave inválida.")
        chave = input("Chave de acesso: ").strip()

   
    sql = """
        SELECT id, ja_votou, chave_acesso, cpf
        FROM eleitores
        WHERE titulo_eleitor = %s
          
          
    """
    

    conexao.cursor.execute(sql, (titulo,))
    eleitor = conexao.cursor.fetchone()

    if not eleitor:
        print("Eleitor não encontrado ou dados inválidos.")
        return
    
    cpf_banco = descriptografar(eleitor[3]).strip("A")
    if cpf_banco[:4] != cpf:
        print("CPF incorreto.")
        return
    
    chave_real = descriptografar(eleitor[2]).strip("A")  
    if chave_real.strip().upper() != chave.strip().upper():
        print("Chave incorreta")
        return


    if eleitor[1] == 1:
        print("Este eleitor já votou.")
        registrar_log("Tentativa de votar novamente (voto duplo).")
        return

    
    numero = input("\nDigite o número do candidato: ").strip()

    while not numero.isdigit():
        print("Número inválido. Digite apenas números.")
        numero = input("Digite o número do candidato: ").strip()

    sql = """
        SELECT id, nome, partido
        FROM candidatos
        WHERE numero = %s
    """
    
    conexao.cursor.execute(sql, (numero,))
    candidato = conexao.cursor.fetchone()

   
    if candidato:
        print(f"Candidato: {candidato[1]} - {candidato[2]}")
        confirmar = input("Confirmar voto? SIM (S) ou NÃO(N): ").upper().strip()

        while confirmar not in ["S", "N"]:
            print("Digite S para SIM ou N para NÃO.")
            confirmar = input("(S/N): ").strip().upper()


        if confirmar != "S":
            print("Voto cancelado.")
            return
        candidato_id = candidato[0]


    else:
        print("Número inválido. Voto será NULO.")
        confirmar = input("Confirmar voto nulo? SIM (S) ou NÃO(N): ").upper().strip()

        while confirmar not in ["S", "N"]:
            print("Digite S para SIM ou N para NÃO.")
            confirmar = input("(S/N): ").strip().upper()

        if confirmar != "S":
            print("Voto cancelado.")
            return
        candidato_id = None  
    
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
    conexao.cursor.execute(sql_voto, (candidato_id, data_hora, protocolo))

    
    sql_update = "UPDATE eleitores SET ja_votou = TRUE WHERE id = %s"
    conexao.cursor.execute(sql_update, (eleitor[0],))

    conexao.conexao.commit()

    print("\nVOTO REGISTRADO COM SUCESSO")
    print(f"Protocolo de votação: {protocolo}")
    registrar_log("Voto realizado.")





def registrar_log(mensagem):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    arquivo = open("auditoria.txt", "a", encoding="utf-8")
    arquivo.write("[" + data_hora + "] " + mensagem + "\n")
    arquivo.close()


def exibir_logs():
    arquivo = open("auditoria.txt", "r", encoding="utf-8")
    conteudo = arquivo.read()

    print("\n=== LOGS DE AUDITORIA ===")
    print(conteudo)

    arquivo.close()






def editar_candidato():

    print("\n=== EDITAR CANDIDATO ===")

    numero = input("Digite o número do candidato: ").strip()

    while not numero.isdigit():
        print("Digite apenas números.")
        numero = input("Digite o número do candidato: ").strip()

    numero_int = int(numero)

    sql = "SELECT id, nome, numero, partido FROM candidatos WHERE numero = %s"
    conexao.cursor.execute(sql, (numero_int,))
    candidato = conexao.cursor.fetchone()

    if not candidato:
        print("Candidato não encontrado.")
        return

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

    numero_existe = True

    while numero_existe:
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
            numero_existe = False

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

    print("\n=== EDITAR ELEITOR ===")

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

    print(f"\nEleitor encontrado: {eleitor[1]}")

    nome = input("Digite o novo nome: ").strip()

    while nome == "":
        print("Nome inválido.")
        nome = input("Digite o novo nome: ").strip()

    titulo = input("Digite o novo título: ").strip()
    titulo = "".join(t for t in titulo if t.isdigit())

    while not validar_titulo(titulo):
        print("Título inválido.")
        titulo = input("Digite o novo título: ").strip()
        titulo = "".join(t for t in titulo if t.isdigit())

    titulo_existe = True

    while titulo_existe:
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
            titulo_existe = False

    mesario = input("Deseja ser mesário? (S/N): ").strip().upper()

    while mesario not in ["S", "N"]:
        print("Digite S ou N.")
        mesario = input("(S/N): ").strip().upper()

    valor_mesario = True if mesario == "S" else False

    confirm = input("Deseja salvar? (S/N): ").strip().upper()

    while confirm not in ["S", "N"]:
        print("Digite S ou N.")
        confirm = input("(S/N): ").strip().upper()

    if confirm != "S":
        print("Edição cancelada.")
        return

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
    print("\n=== TORNAR ELEITOR MESÁRIO ===")

    cpf = input("Digite o CPF do eleitor: ").strip()
    cpf = cpf.replace('.', '')
    cpf = cpf.replace('-', '')

    while not cpf.isdigit():
        print("CPF inválido. Digite apenas números")
        cpf = input("Digite o CPF do eleitor: ").strip()
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')

    cpf_cripto = criptografar(cpf)
    sql = "SELECT id, nome_completo, is_mesario FROM eleitores WHERE cpf = %s"
    conexao.cursor.execute(sql, (cpf_cripto,))
    eleitor = conexao.cursor.fetchone()

    if not eleitor:
        print("Eleitor não encontrado.")
        registrar_log("Tentativa de tornar mesário um eleitor não existente.")
        return
    
    if eleitor[2] == 1:
        print(f"{eleitor[1]} já é mesário.")
        return
    
    confirmacao = input(f"Deseja tornar {eleitor[1]} um mesário? Sim (S) ou Não (N)").strip().upper()

    while confirmacao not in ["S", "N"]:
        print("Digite S ou N.")
        confirmacao = input("(S/N): ").strip().upper()

    if confirmacao != "S":
        print("Operação cancelada.")
        return
    
    sql_update = "UPDATE eleitores SET is_mesario = TRUE WHERE id = %s"
    conexao.cursor.execute(sql_update, (eleitor[0],))
    conexao.conexao.commit()

    print(f"{eleitor[1]} agora é mesário!")

    registrar_log("Eleitor promovido a mesário.")


def boletim_urna():
    print("\n=== BOLETIM DE URNA ===")

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

    for c in resultados:
        print(f"{c[0]} ({c[1]}) - {c[2]} | {c[3]} voto(s)")

        if c[3] > maior_votos:
            maior_votos = c[3]
            vencedores = [c]

        elif c[3] == maior_votos:
            vencedores.append(c)
        
    print("\n=== RESULTADO FINAL ===")

    if len(vencedores) == 1:
        v = vencedores[0]
        print(f"VENCEDOR: {v[0]} ({v[1]}) - {v[2]}")
        print(f"Total de votos: {v[3]}")

    else:
        print("EMPATE ENTRE:")
        for v in vencedores:
            print(f"{v[0]} ({v[1]}) - {v[2]} | {v[3]} votos")


        

def estatisticas_comparecimento():
    print("\n=== ESTATÍSTICAS DE COMPARECIMENTO ===")

    sql_total = "SELECT COUNT(*) FROM eleitores"
    conexao.cursor.execute(sql_total)
    total = conexao.cursor.fetchone()[0]

    sql_votaram = "SELECT COUNT(*) FROM eleitores WHERE ja_votou = 1"
    conexao.cursor.execute(sql_votaram)
    votaram = conexao.cursor.fetchone()[0]

    if total == 0:
        print("Nenhum eleitor cadastrado.")
        return
    
    percentual = (votaram / total) * 100
    print(f"Total de eleitores: {total}")
    print(f"Eleitores que votaram: {votaram}")
    print(f"Comparecimento: {percentual:.2f}%")

def votos_por_partido():

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

    if not resultados:
        print("Nenhum dado disponível.")
        return

    for r in resultados:
        partido = r[0]
        votos = r[1]
        print(f"Partido: {partido} -> {votos} votos") 
    

def validar_integridade():

    
    sql_votos = "SELECT COUNT(*) FROM voto"
    conexao.cursor.execute(sql_votos)
    total_votos = conexao.cursor.fetchone()[0]

    
    sql_eleitores = "SELECT COUNT(*) FROM eleitores WHERE ja_votou = TRUE"
    conexao.cursor.execute(sql_eleitores)
    total_eleitores = conexao.cursor.fetchone()[0]

    print("\n=== VALIDAÇÃO DE INTEGRIDADE ===")

    print(f"Total de votos registrados: {total_votos}")
    print(f"Total de eleitores que votaram: {total_eleitores}")

    
    if total_votos == total_eleitores:
        print("\nINTEGRIDADE CONFIRMADA")
        print("Não há inconsistências no sistema.")
    else:
        print("\nERRO DE INTEGRIDADE")
        print("Há divergência entre votos e eleitores.")





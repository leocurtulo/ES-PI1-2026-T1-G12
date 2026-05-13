def validar_titulo(titulo):

    titulo = str(titulo)

    # Verificação básica
    if len(titulo) != 12 or not titulo.isdigit():
        return False

    # Divisão das partes do titulo de eleitor
    numero_sequencial = titulo[:8]
    uf = titulo[8:10]
    dv_informado = titulo[10:]


#Cálculo do primeiro digito validador
    pesos_dv1 = [2, 3, 4, 5, 6, 7, 8, 9]
    soma_dv1 = 0

    for i in range(8):
        soma_dv1 += int(numero_sequencial[i]) * pesos_dv1[i]

    resto1 = soma_dv1 % 11

    if resto1 == 10:
        dv1 = 0
    elif resto1 == 0 and uf in ["01", "02"]:  # SP ou MG
        dv1 = 1
    else:
        dv1 = resto1


#Cálculo do segundo titulo validador
    pesos_dv2 = [7, 8, 9]
    soma_dv2 = 0

    soma_dv2 += int(uf[0]) * pesos_dv2[0]
    soma_dv2 += int(uf[1]) * pesos_dv2[1]
    soma_dv2 += dv1 * pesos_dv2[2]

    resto2 = soma_dv2 % 11

    if resto2 == 10:
        dv2 = 0
    elif resto2 == 0 and uf in ["01", "02"]:  # SP ou MG
        dv2 = 1
    else:
        dv2 = resto2


#Resultado da validação:
    dv_calculado = str(dv1) + str(dv2)

    return dv_calculado == dv_informado








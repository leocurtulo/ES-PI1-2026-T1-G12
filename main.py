import menu
import funcoes_PI



opc = -1

while (opc != 0):
    opc = menu.menu_principal()

    match opc:

        # ===== GERENCIAMENTO =====
        case 1:
            sub = -1

            while (sub != 0):
                sub = menu.menu_gerenciamento()

                match sub:

                    # ELEITORES
                    case 1:
                        op = -1
                        while (op != 0):
                            op = menu.menu_eleitores()

                            match op:
                                case 1:
                                    funcoes_PI.cadastro_eleitores()
                                case 2:
                                    funcoes_PI.listar_eleitores()
                                case 3:
                                    funcoes_PI.buscar_eleitor()
                                case 4:
                                    print("Editar eleitor")
                                case 5:
                                    funcoes_PI.remover_eleitores()
                                case 6:
                                    print("Tornar eleitor mesário")
                                case 7:
                                    funcoes_PI.listar_mesarios()
                                case 0:
                                    print("Voltando...")
                                case _:
                                    print("Opção inválida.")

                    # CANDIDATOS
                    case 2:
                        op = -1
                        while (op != 0):
                            op = menu.menu_candidatos()

                            match op:
                                case 1:
                                    funcoes_PI.cadastrar_candidato()
                                case 2:
                                    print("Listar candidatos")
                                case 3:
                                    funcoes_PI.buscar_candidatos()
                                case 4:
                                    print("Editar candidato")
                                case 5:
                                    print("Remover candidato")
                                case 0:
                                    print("Voltando...")
                                case _:
                                    print("Opção inválida.")

                    case 0:
                        print("Voltando...")

                    case _:
                        print("Opção inválida.")

        # ===== VOTAÇÃO =====
        case 2:
            sub = -1

            while (sub != 0):
                sub = menu.menu_votacao()

                match sub:

                    # ABERTURA
                    case 1:
                        op = -1
                        while (op != 0):
                            op = menu.menu_abertura()

                            match op:
                                case 1:
                                    print("Votar")
                                case 2:
                                    print("Encerrar votação")
                                case 0:
                                    print("Voltando...")
                                case _:
                                    print("Opção inválida.")

                    # AUDITORIA
                    case 2:
                        op = -1
                        while (op != 0):
                            op = menu.menu_auditoria()

                            match op:
                                case 1:
                                    print("Logs")
                                case 2:
                                    print("Protocolos")
                                case 0:
                                    print("Voltando...")
                                case _:
                                    print("Opção inválida.")

                    # RESULTADOS
                    case 3:
                        op = -1
                        while (op != 0):
                            op = menu.menu_resultados()

                            match op:
                                case 1:
                                    print("Boletim")
                                case 2:
                                    print("Estatísticas")
                                case 3:
                                    print("Partido")
                                case 4:
                                    print("Integridade")
                                case 0:
                                    print("Voltando...")
                                case _:
                                    print("Opção inválida.")

                    case 0:
                        print("Voltando...")

                    case _:
                        print("Opção inválida.")

        # ===== SAIR =====
        case 0:
            print("Encerrando sistema...")

        case _:
            print("Opção inválida.")


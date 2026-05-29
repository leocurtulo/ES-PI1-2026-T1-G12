import menu
import funcoes_PI
import os
votacao_aberta = 0
votacao_existente = 0

def limpar_principal():
    os.system("cls" if os.name == "nt" else clear)


opc = -1

while (opc != 0):
    limpar_principal()
    opc = menu.menu_principal()

    match opc:

        # ===== GERENCIAMENTO =====
        case 1:
            sub = -1

            while (sub != 0):
                limpar_principal()
                sub = menu.menu_gerenciamento()

                match sub:

                    # ELEITORES
                    case 1:
                        op = -1
                        while (op != 0):
                            limpar_principal()
                            op = menu.menu_eleitores()

                            match op:
                                case 1:
                                    funcoes_PI.cadastro_eleitores()
                                    input("\nPressione ENTER para continuar...")
                                case 2:
                                    funcoes_PI.listar_eleitores()
                                    input("\nPressione ENTER para continuar...")
                                case 3:
                                    funcoes_PI.buscar_eleitor()
                                    input("\nPressione ENTER para continuar...")
                                case 4:
                                    funcoes_PI.editar_eleitor()
                                    input("\nPressione ENTER para continuar...")
                                case 5:
                                    funcoes_PI.remover_eleitores()
                                    input("\nPressione ENTER para continuar...")
                                case 6:
                                    funcoes_PI.tornar_mesario()
                                    input("\nPressione ENTER para continuar...")
                                case 7:
                                    funcoes_PI.listar_mesarios()
                                    input("\nPressione ENTER para continuar...")
                                case 0:
                                    print("Voltando...")
                                case _:
                                    print("Opção inválida.")
                                    input("Pressione ENTER para continuar...")

                    # CANDIDATOS
                    case 2:
                        op = -1
                        while (op != 0):
                            limpar_principal()
                            op = menu.menu_candidatos()

                            match op:
                                case 1:
                                    funcoes_PI.cadastrar_candidato()
                                    input("\nPressione ENTER para continuar...")
                                case 2:
                                    funcoes_PI.listar_candidatos()
                                    input("\nPressione ENTER para continuar...")
                                case 3:
                                    funcoes_PI.buscar_candidatos()
                                    input("\nPressione ENTER para continuar...")
                                case 4:
                                    funcoes_PI.editar_candidato()
                                    input("\nPressione ENTER para continuar...")
                                case 5:
                                    funcoes_PI.remover_candidato()
                                    input("\nPressione ENTER para continuar...")
                                case 0:
                                    print("Voltando...")
                                case _:
                                    print("Opção inválida.")
                                    input("Pressione ENTER para continuar...")

                    case 0:
                        print("Voltando...")

                    case _:
                        print("Opção inválida.")
                        input("Pressione ENTER para continuar...")

        # ===== VOTAÇÃO =====
        case 2:
            sub = -1

            while (sub != 0):
                limpar_principal()
                
                sub = menu.menu_votacao_inicial ()

                match sub:

                    
                    case 1:
                        if votacao_aberta == 0:
                            abriu = funcoes_PI.abrir_votacao()
                            if abriu == 1:
                                votacao_aberta = 1

                        else:
                            print("A votação já está aberta.")
                            
                        input("\nPressione ENTER para continuar...")
                        
                    case 2:
                        if votacao_existente == 1:
                            op = -1
                            while op !=0:
                                limpar_principal()
                                op = menu.menu_resultados()

                                match op:
                                    case 1:
                                        funcoes_PI.boletim_urna()
                                    case 2:
                                        funcoes_PI.estatisticas_comparecimento()
                                    case 3:
                                        funcoes_PI.votos_por_partido()
                                    case 4:
                                        funcoes_PI.validar_integridade()
                                    case 0:
                                        print("Voltando...")
                                    case _:
                                        print("Opção inválida.")
                                input("\nPressione ENTER para continuar...")
                        else:
                            print("Ainda não estão liberados os resultados.")

                            input("\nPressione ENTER para continuar...")
                    

                    case 3:
                        if votacao_existente == 1:
                            op = -1
                            while op !=0:
                                limpar_principal()
                                op = menu.menu_auditoria()

                                match op:
                                    case 1:
                                        funcoes_PI.exibir_logs()
                                    case 2:
                                        funcoes_PI.exibir_protocolos()
                                    case 0:
                                        print("Voltando...")
                                    case _:
                                        print("Opção inválida.")
                                input("\nPressione ENTER para continuar...")
                        else:
                            print("Ainda não há dados para auditoria.")

                            input("Pressione ENTER para continuar...")

                    case 4:
                        if votacao_aberta == 1:
                            op = -1
                            while op != 0:

                                limpar_principal()
                                op = menu.menu_urna()

                                match op:
                                    case 1:
                                        if votacao_aberta ==1:
                                            funcoes_PI.votar()
                                        else:
                                            print("A votação está fechada.")
                                        input("\nPressione ENTER para continuar...")
                                        

                                    case 2:
                                        encerrou = funcoes_PI.encerrar_votacao()
                                        
                                        if encerrou == 1:
                                            votacao_aberta = 0
                                            votacao_existente = 1
                                            op = 0
                                        
                                        input("\nPressione ENTER para continuar...")

                                    case 0:
                                        print("Voltando...")

                                    case _:
                                        print("Opção inválida.")
                                        input("Pressione ENTER para continuar...")

                        else:
                            print("A votação não está aberta.")
                            input("\nPressione ENTER para continuar...")

                    case 0:
                        print("Voltando...")

                    case _:
                        print("Opção inválida.")
                        input("Pressione ENTER para continuar...")


           

        # ===== SAIR =====
        case 0:
            print("Encerrando sistema...")

        case _:
            print("Opção inválida.")
            input("Pressione ENTER para continuar...")


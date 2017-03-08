#!/usr/bin/env python
__author__ = 'Cristiano Vagos, João Pedro Fonseca'
__email__ = 'cristianovagos@ua.pt, jpedrofonseca@ua.pt'
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Cristiano Vagos"

"""
Introdução à Inteligência Artificial @ DETI-UA 2016/17
Trabalho Prático de Grupo: Blackjack

Cristiano Vagos (65169), João Pedro Fonseca (73779)

------------------------------------------------------------------------------------------------

print_studentPlayer.py - Programa de teste de execução do agente StudentPlayer

Ferramenta criada para visualização e interpretação dos dados ao longo da execução do agente.
Permite:
    - Ver tabela de acções (tabela Q / a melhor estratégia a executar pelo agente)
    - Ver valores máximos da tabela Q (recompensa média para cada estado da tabela Q)
    - Consultar valor da tabela (ver os valores para um dado estado da tabela Q)
    - Consultar valor da primeira/próximas jogadas (ver o nº de ocorrências para um dado estado da tabela Q)
    - Ver dicionario da primeira jogada / próximas jogadas
    - Ver tabela Q / dicionario
    - Número total de jogos feitos pelo ficheiro
    - Ver estado da aprendizagem (Primeira Jogada e Próximas Jogadas)
    - Alterar valor de surrender (apenas para visualização neste ficheiro)

------------------------------------------------------------------------------------------------

Packages não-nativos necessários à execução: termcolor

"""

import pickle
from termcolor import colored, cprint

file = open("studentPlayer.data", "rb")
file.seek(0)
tmpList = pickle.load(file)
dat = tmpList[0]
datFirst = tmpList[1]
avg = tmpList[2]
avgFirst = tmpList[3]
total = tmpList[4]
file.close()

surrenderFlag = -0.65
learnFactor = 150

print(chr(27) + "[2J")
while(True):
    print('-------------------------------------------------------------------------------')
    print("                 Ferramenta de Teste para o Agente Blackjack")
    print('-------------------------------------------------------------------------------')
    print("\nSeleccionar a opção:")
    print("     1 - Ver tabela Q / ver estratégia           (1ª Jogada)")
    print("     2 - Ver tabela Q / ver estratégia           (Próximas Jogadas)")
    print("     3 - Ver valores máximos da tabela Q         (1ª Jogada)")
    print("     4 - Ver valores máximos da tabela Q         (Próximas Jogadas)")
    print("     5 - Consultar valor da tabela Q             (1ª Jogada)")
    print("     6 - Consultar valor da tabela Q             (Próximas Jogadas)")
    print("     7 - Consultar valor de contagem             (1ª Jogada)")
    print("     8 - Consultar valor de contagem             (Próximas Jogadas)")
    print("     9 - Ver dicionario da primeira jogada       (raw data)")
    print("    10 - Ver dicionario das próximas jogadas     (raw data)")
    print("    11 - Ver tabela Q / dicionario (raw data)    (1ª Jogada)")
    print("    12 - Ver tabela Q / dicionario (raw data)    (Próximas Jogadas)")
    print("    13 - Número de jogos feitos pelo ficheiro")
    print("    14 - Ver estado da aprendizagem              (1ª Jogada)")
    print("    15 - Ver estado da aprendizagem              (Próximas Jogadas)")
    print("    16 - Alterar valor mínimo de Surrender       (valor atual:", surrenderFlag, ")")
    print("     0 - Sair")
    print('-------------------------------------------------------------------------------')
    option = int(input("Opção -> "),10)
    print('-------------------------------------------------------------------------------')
    print("\n")

    if option == 1:
        print('----------------------------------------------------------------------')
        print('                       Estratégia (1ª Jogada)')
        print('----------------------------------------------------------------------')
        for useable in [False, True]:
            if useable:
                print('--------------------------------------------------')
                print('                     Soft Hand')
                print('--------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            else:
                print('--------------------------------------------------')
                print('                     Hard Hand')
                print('--------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            print('  A    2    3    4    5    6    7    8    9    T')
            print('--------------------------------------------------')
            for value in range(mintmp+1, maxtmp+1):
                for card in range(1, 11):
                    hit = datFirst[((card, value, useable), 'h')]
                    stand = datFirst[((card, value, useable), 's')]
                    dd = datFirst[((card, value, useable), 'd')]

                    if hit <= surrenderFlag and stand <= surrenderFlag and dd <= surrenderFlag:
                        cprint(' Sur ', "cyan", end="")
                        continue

                    if hit <= surrenderFlag and stand <= surrenderFlag:
                        cprint(' Sur ', "cyan", end="")
                        continue

                    tmp = max(hit, stand, dd)
                    if tmp == 0.0:
                        print('     ', end="")
                    elif tmp == hit:
                        cprint('  H  ', 'red', end="")
                    elif tmp == stand:
                        cprint('  S  ', 'yellow', end="")
                    elif tmp == dd:
                        cprint('  D  ', 'blue', end="")
                print('| %d' % value)
            print(' ')
    elif option == 2:
        print('----------------------------------------------------------------------')
        print('                    Estratégia (Próximas Jogadas)')
        print('----------------------------------------------------------------------')
        for useable in [False, True]:
            if useable:
                print('--------------------------------------------------')
                print('                     Soft Hand')
                print('--------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            else:
                print('--------------------------------------------------')
                print('                     Hard Hand')
                print('--------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            print('  A    2    3    4    5    6    7    8    9    T')
            print('--------------------------------------------------')
            for value in range(mintmp+1, maxtmp+1):
                for card in range(1, 11):
                    hit = dat[((card, value, useable), 'h')]
                    stand = dat[((card, value, useable), 's')]

                    if hit <= surrenderFlag and stand <= surrenderFlag:
                        cprint(' Sur ', "cyan", end="")
                        continue

                    tmp = max(hit, stand)
                    if tmp == 0.0:
                        print('     ', end="")
                    elif tmp == hit:
                        cprint('  H  ', 'red', end="")
                    elif tmp == stand:
                        cprint('  S  ', 'yellow', end="")
                print('| %d' % value)
            print(' ')
    elif option == 3:
        print('----------------------------------------------------------------------')
        print('           Valores máximos da Tabela Q (Primeira Jogada)')
        print('----------------------------------------------------------------------')
        for useable in [False, True]:
            if useable:
                print('----------------------------------------------------------------------')
                print('                               Soft Hand')
                print('----------------------------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            else:
                print('----------------------------------------------------------------------')
                print('                               Hard Hand')
                print('----------------------------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            print('    A      2      3      4      5      6      7      8      9      T')
            print('----------------------------------------------------------------------')
            for value in range(mintmp+1, maxtmp+1):
                for card in range(1, 11):
                    hit = datFirst[((card, value, useable), 'h')]
                    stand = datFirst[((card, value, useable), 's')]
                    dd = datFirst[((card, value, useable), 'd')]

                    if hit <= surrenderFlag and stand <= surrenderFlag and dd <= surrenderFlag:
                        cprint('  Surr ', "cyan", end="")
                        continue

                    val = max(hit,stand,dd)
                    if val < 0:
                        cprint(" %5.2f " % round((val),2), "red", end="")
                    elif val == 0:
                        print(" %5.2f " % round((val), 2), end="")
                    else:
                        cprint(" %5.2f " % round((val), 2), "green", end="")
                print('| %d' % value)
            print(' ')
        print("Legenda:")
        cprint("    Maior probabilidade de ganhar", "green")
        cprint("    Maior probabilidade de perder", "red")
        cprint("    Surr", "cyan", end="")
        print(" - Surrender\n")

    elif option == 4:
        print('----------------------------------------------------------------------')
        print('           Valores máximos da Tabela Q (Próximas Jogadas)')
        print('----------------------------------------------------------------------')
        for useable in [False, True]:
            if useable:
                print('----------------------------------------------------------------------')
                print('                               Soft Hand')
                print('----------------------------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            else:
                print('----------------------------------------------------------------------')
                print('                               Hard Hand')
                print('----------------------------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            print('    A      2      3      4      5      6      7      8      9      T')
            print('----------------------------------------------------------------------')
            for value in range(mintmp+1, maxtmp+1):
                for card in range(1, 11):
                    hit = dat[((card, value, useable), 'h')]
                    stand = dat[((card, value, useable), 's')]

                    if hit <= surrenderFlag and stand <= surrenderFlag:
                        cprint('  Surr ', "cyan", end="")
                        continue

                    val = max(hit,stand)
                    if val < 0:
                        cprint(" %5.2f " % round((val),2), "red", end="")
                    elif val == 0:
                        print(" %5.2f " % round((val), 2), end="")
                    else:
                        cprint(" %5.2f " % round((val), 2), "green", end="")
                print('| %d' % value)
            print(' ')
        print("Legenda:")
        cprint("    Maior probabilidade de ganhar", "green")
        cprint("    Maior probabilidade de perder", "red")
        cprint("    Surr", "cyan", end="")
        print(" - Surrender\n")

    elif option == 5:
        print('-------------------------------------------------------------------------------')
        print('               Consultar Valores da Tabela Q (Primeira Jogada)')
        print('-------------------------------------------------------------------------------')
        dealer = int(input("Valor do dealer: "),10)
        player = int(input("Valor do player: "),10)

        print("\nHard Hand")
        print("     Stand : ", datFirst[((dealer, player, False), 's')] if datFirst[((dealer, player, False), 's')] != 0.0 else "(na)")
        print("     Hit   : ", datFirst[((dealer, player, False), 'h')] if datFirst[((dealer, player, False), 'h')] != 0.0 else "(na)")
        print("     D-Down: ", datFirst[((dealer, player, False), 'd')] if datFirst[((dealer, player, False), 'd')] != 0.0 else "(na)")

        val = max(datFirst[((dealer, player, False), 's')], datFirst[((dealer, player, False), 'h')],
                  datFirst[((dealer, player, False), 'd')])
        if val <= surrenderFlag:
            cprint("     -> O Agente faz surrender!", "cyan")

        print("\nSoft Hand")
        print("     Stand : ", datFirst[((dealer, player, True), 's')] if datFirst[((dealer, player, True), 's')] != 0.0 else "(na)")
        print("     Hit   : ", datFirst[((dealer, player, True), 'h')] if datFirst[((dealer, player, True), 'h')] != 0.0 else "(na)")
        print("     D-Down: ", datFirst[((dealer, player, True), 'd')] if datFirst[((dealer, player, True), 'd')] != 0.0 else "(na)")

        val = max(datFirst[((dealer, player, True), 's')], datFirst[((dealer, player, True), 'h')],
                  datFirst[((dealer, player, True), 'd')])
        if val <= surrenderFlag:
            cprint("     -> O Agente faz surrender!", "cyan")

    elif option == 6:
        print('-------------------------------------------------------------------------------')
        print('              Consultar Valores da Tabela Q (Próximas Jogadas)')
        print('-------------------------------------------------------------------------------')
        dealer = int(input("Valor do dealer: "),10)
        player = int(input("Valor do player: "),10)

        print("\nHard Hand")
        print("     Stand : ", dat[((dealer, player, False), 's')] if dat[((dealer, player, False), 's')] != 0.0 else "(na)")
        print("     Hit   : ", dat[((dealer, player, False), 'h')] if dat[((dealer, player, False), 'h')] != 0.0 else "(na)")

        val = max(dat[((dealer, player, False), 's')], dat[((dealer, player, False), 'h')])
        if val <= surrenderFlag:
            cprint("     -> O Agente faz surrender!", "red")

        print("\nSoft Hand")
        print("     Stand : ", dat[((dealer, player, True), 's')] if dat[((dealer, player, True), 's')] != 0.0 else "(na)")
        print("     Hit   : ", dat[((dealer, player, True), 'h')] if dat[((dealer, player, True), 'h')] != 0.0 else "(na)")

        val = max(dat[((dealer, player, True), 's')], dat[((dealer, player, True), 'h')])
        if val <= surrenderFlag:
            cprint("     -> O Agente faz surrender!", "red")

    elif option == 7:
        print('-------------------------------------------------------------------------------')
        print('                 Consultar Valor (Primeira Jogada)')
        print('-------------------------------------------------------------------------------')
        dealer = int(input("Valor do dealer: "), 10)
        player = int(input("Valor do player: "), 10)

        print("\nHard Hand")
        print("     Stand : ", avgFirst[((dealer, player, False), 's')] if avgFirst[((dealer, player, False), 's')] != 0 else "(na)")
        print("     Hit   : ", avgFirst[((dealer, player, False), 'h')] if avgFirst[((dealer, player, False), 'h')] != 0 else "(na)")
        print("     D-Down: ", avgFirst[((dealer, player, False), 'd')] if avgFirst[((dealer, player, False), 'd')] != 0 else "(na)")

        print("\nSoft Hand")
        print("     Stand : ", avgFirst[((dealer, player, True), 's')] if avgFirst[((dealer, player, True), 's')] != 0 else "(na)")
        print("     Hit   : ", avgFirst[((dealer, player, True), 'h')] if avgFirst[((dealer, player, True), 'h')] != 0 else "(na)")
        print("     D-Down: ", avgFirst[((dealer, player, True), 'd')] if avgFirst[((dealer, player, True), 'd')] != 0 else "(na)")



    elif option == 8:
        print('-------------------------------------------------------------------------------')
        print('                 Consultar Valor (Próximas Jogadas)')
        print('-------------------------------------------------------------------------------')
        dealer = int(input("Valor do dealer: "), 10)
        player = int(input("Valor do player: "), 10)

        print("\nHard Hand\n")
        print("     Stand : ", avg[((dealer, player, False), 's')] if avg[((dealer, player, False), 's')] != 0 else "(na)")
        print("     Hit   : ", avg[((dealer, player, False), 'h')] if avg[((dealer, player, False), 'h')] != 0 else "(na)")

        print("\nSoft Hand\n")
        print("     Stand : ", avg[((dealer, player, True), 's')] if avg[((dealer, player, True), 's')] != 0 else "(na)")
        print("     Hit   : ", avg[((dealer, player, True), 'h')] if avg[((dealer, player, True), 'h')] != 0 else "(na)")

    elif option == 9:
        print('-------------------------------------------------------------------------------')
        print('                           Contagem Primeira Jogada')
        print('-------------------------------------------------------------------------------\n')
        print("\n", sorted(avgFirst.items()), "\n\n")

    elif option == 10:
        print('-------------------------------------------------------------------------------')
        print('                          Contagem Próximas Jogadas')
        print('-------------------------------------------------------------------------------\n')
        print("\n", sorted(avg.items()), "\n\n")

    elif option == 11:
        print('-------------------------------------------------------------------------------')
        print('                           Tabela Q Primeira Jogada')
        print('-------------------------------------------------------------------------------\n')
        print("\n", sorted(datFirst.items()), "\n\n")

    elif option == 12:
        print('-------------------------------------------------------------------------------')
        print('                          Tabela Q Próximas Jogadas')
        print('-------------------------------------------------------------------------------\n')
        print("\n", sorted(dat.items()), "\n\n")

    elif option == 13:
        print('-------------------------------------------------------------------------------')
        print('   Número total de jogos feitos pelo ficheiro: ', total)
        print('-------------------------------------------------------------------------------\n')

    elif option == 14:
        print('-------------------------------------------------------------------------------')
        print('                 Estado da Aprendizagem (Primeira Jogada)')
        print('-------------------------------------------------------------------------------')
        for useable in [False, True]:
            if useable:
                print('-------------------------------------------------------------------------------')
                print('                                  Soft Hand')
                print('-------------------------------------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            else:
                print('-------------------------------------------------------------------------------')
                print('                                  Hard Hand')
                print('-------------------------------------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            print('\n    A       2       3       4       5       6       7       8       9       T')
            print('-------------------------------------------------------------------------------')
            for value in range(mintmp+1, maxtmp+1):
                for card in range(1, 11):
                    hit = avgFirst[((card, value, useable), 'h')]
                    stand = avgFirst[((card, value, useable), 's')]
                    dd = avgFirst[((card, value, useable), 'd')]
                    hit_c = datFirst[((card, value, useable), 'h')]
                    stand_c = datFirst[((card, value, useable), 's')]
                    dd_c = datFirst[((card, value, useable), 'd')]

                    if hit == 0 and stand == 0 and dd == 0:
                        print('  (na)  ', end="")
                        continue

                    if hit >= learnFactor and stand >= learnFactor and dd >= learnFactor:
                        cprint('  True  ', 'green', end="")
                    else:
                        print('        ', end="")
                print('| %d' % value)
            print(' ')

    elif option == 15:
        print('-------------------------------------------------------------------------------')
        print('                 Estado da Aprendizagem (Próximas Jogadas)')
        print('-------------------------------------------------------------------------------')
        for useable in [False, True]:
            if useable:
                print('-------------------------------------------------------------------------------')
                print('                                  Soft Hand')
                print('-------------------------------------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            else:
                print('-------------------------------------------------------------------------------')
                print('                                  Hard Hand')
                print('-------------------------------------------------------------------------------')
                maxtmp = 20
                mintmp = 3
            print('\n    A       2       3       4       5       6       7       8       9       T')
            print('-------------------------------------------------------------------------------')
            for value in range(mintmp+1, maxtmp+1):
                for card in range(1, 11):
                    hit = avg[((card, value, useable), 'h')]
                    stand = avg[((card, value, useable), 's')]
                    hit_c = dat[((card, value, useable), 'h')]
                    stand_c = dat[((card, value, useable), 's')]

                    if hit == 0 and stand == 0:
                        print('  (na)  ', end="")
                        continue

                    if hit >= learnFactor and stand >= learnFactor:
                        cprint('  True  ', 'green', end="")
                    else:
                        print('        ', end="")
                print('| %d' % value)
            print(' ')
    elif option == 16:
        print('-------------------------------------------------------------------------------')
        print('                         Alterar Valor Surrender')
        print('-------------------------------------------------------------------------------')
        print('Valor de Surrender atual: ', surrenderFlag)
        surrenderFlag = float(input("Valor do surrender: "))

    elif option == 0:
        break
    else:
        print("\nOpção inválida!")

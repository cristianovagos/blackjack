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

Agente que joga sozinho Blackjack, com o código fornecido pelos professores.
Optámos por escolher a estratégia de AI Reinforcement Learning, que faz com
que o agente aprenda sozinho a tomar decisões conforme os jogos que vai fazendo
e os resultados obtidos dos mesmos.
(Retirado do livro "Reinforcement Learning: An Introduction")
(link: https://webdocs.cs.ualberta.ca/~sutton/book/bookdraft2016sep.pdf)

Algumas ideias aqui implementadas são baseadas em código já existente, onde são feitos
dois métodos de Reinforcement Learning (Monte Carlo ES e Q-Learning):
(código: https://inst.eecs.berkeley.edu/~cs188/sp08/projects/blackjack/blackjack.py)

A nossa estratégia passa por jogar de forma completamente aleatória até um número limite
de jogadas para cada estado possível. Então, os dados são guardados em 2 dicionários que
guardam todos os estados possíveis e a probabilidade de acerto, que é aumentada/diminuida
conforme a recompensa de cada jogo (1 em caso de vitória, 0 para empate, -1 para derrota).
Todas as acções são escolhidas pelo agente, de forma completamente autónoma tendo em base
os jogos que já efetuou até ao momento.

Depois do número limite de jogadas para cada tipo de jogada (Hit, Stand ou Double-Down)
o agente joga a melhor opção determinada pelo histórico de jogos que fez até ao momento.
A melhor acção provém do dicionário respetivo (primeira / próximas jogadas), e é escolhida
a acção que tem a maior média de recompensa (quanto mais próximo de 1, melhor, e quanto mais
próximo de -1 pior).
Por isso o rácio de vitórias irá aumentar ao longo do tempo em que a tabela é preenchida.

Guardamos os dados (Tabelas Q + Contagens de Ocorrências) num ficheiro que é habitualmente
lido e gravado com os dados que vai obtendo no decorrer dos jogos. Conforme o estado do jogo atual
(mão do dealer, mão do jogador, se o jogador tem "hard" ou "soft hand"), o agente escolhe
então uma opção de entre as disponíveis (Hit / Stand / Double-Down / Surrender).

O sistema de apostas usado no nosso agente é o "Up and Pull Betting System".
(Retirado de: http://www.countingedge.com/blackjack-money-management/)
Após os testes confirma-se que é uma boa estratégia de apostas para um bom ganho e menor risco.

------------------------------------------------------------------------------------------------

Packages não-nativos necessários à execução: numpy

"""

import os
import os.path

import card
import numpy as np
import pickle
import random
from player import Player
from collections import defaultdict

class StudentPlayer(Player):
    def __init__(self, name="Zeljko Ranogajec", money=0):
        super(StudentPlayer, self).__init__(name, money)
        self.name = name
        self.money = money

        """
        Opção para visualizar no terminal tudo o que se passa
        no agente. Estados atuais, valores, e decisões.
        """
        self.verbose = False

        """
        Inicialização das estruturas de dados

        - states    : todos os estados possíveis
        - qFirst    : tabela Q da primeira jogada (devido ao Double-Down)
        - q         : tabela Q das próximas jogadas
        - countFirst: contagem da primeira jogada (devido ao Double-Down)
        - count     : contagem das restantes jogadas (só guarda Hit/Stand)
        """
        self.states = initStates()
        self.qFirst = initActions(self.states)
        self.q = initActions(self.states)
        self.countFirst = initCount(self.qFirst)
        self.count = initCount(self.q)

        """
        Inicialização das variáveis auxiliares

        - winStreak    : contagem do nº de vitórias sucessivas
        - firstPlay    : verificação se é a primeira joga
        - learnFactor  : nº de jogos necessários para aprender (p/ cada jogada)da
        - surrenderFlag: "probabilidade" limite para fazer Surrender
        - results      : dicionario que guarda os estados decorridos no jogo (próximas jogadas)
        - firstResults : dicionario que guarda os estados decorridos no jogo (primeira jogada)
        """
        self.winStreak = 0
        self.firstPlay = True
        self.learnFactor = 150
        self.surrenderFlag = -0.65
        self.results = defaultdict(int)
        self.firstResults = defaultdict(int)

        """
        Inicialização das variáveis de contagem

        Usadas para efeitos de logging, pois é criado um ficheiro
        para ver os resultados atuais e totais dos jogos
        """
        self.games = 0
        self.currentGames = 0
        self.fileGames = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.twins = 0
        self.tlosses = 0
        self.tdraws = 0

        """
        Verificação do ficheiro que guarda os dados dos jogos
        efetuados pelo agente
        """
        # Verificar se o ficheiro existe
        if not os.path.isfile("studentPlayer.data"):
            # O ficheiro não existe
            print("Creating file... (press ENTER)")
            input()
            # Cria o ficheiro
            self.createFile()
        # Verificar se o ficheiro está vazio
        elif os.stat("studentPlayer.data").st_size == 0:
            print("File empty. Writing something... (press ENTER)")
            input()
            # Escreve o dicionario no ficheiro só para o ficheiro ter alguma coisa
            self.writeFile()
        else:
            print("File found. Reading... (press ENTER)")
            input()
            # Vamos ler o ficheiro e escrever o seu conteudo no dicionario
            self.readFile()

    def play(self, dealer, players):
        if self.verbose:
            self.debug_state(dealer, players)

        # Obter valores da minha mão
        playerHand, playerValue = self.getPlayerValue(players)

        # Se for primeira jogada vamos ler valor da mão do dealer
        if self.firstPlay:
            self.dealerValue = self.getDealerValue(dealer)

        playerAce = self.getUseableAce(playerHand)

        state = (self.dealerValue, playerValue, playerAce)

        if self.learning(state, self.firstPlay):
        #if self.learningEpsilon():
            action = self.getRandomAction(self.firstPlay)
        else:
            action = self.getBestAction(state, self.firstPlay)

        sa = (state, action)

        if self.firstPlay:
            self.firstPlay = False
            self.countFirst[sa] += 1
            self.firstResults[sa] = 0
        else:
            self.count[sa] += 1
            self.results[sa] = 0

        # Joga com a ação escolhida
        return action

    # Retirado dos ficheiros fornecidos
    def debug_state(self, dealer, players):
        print("--------------------------------------------")
        print("{:10s}: {!s:32s} = {}".format("Dealer", ['🎴 '] + dealer.hand, card.value(dealer.hand)))
        for p in players:
            print("{:10s}: {!s:32s} = {}".format(p.player.name, p.hand, card.value(p.hand)))

    def bet(self, dealer, players):
        return self.bets[self.winStreak]

    def want_to_play(self, rules):
        self.min_bet = rules.min_bet
        self.max_bet = rules.max_bet
        self.bets = list(range(1, self.max_bet + 1))
        self.bets[0] = 2
        return True

    def payback(self, prize):
        # Jogo já acabou, vamos recolher o prémio
        super(StudentPlayer, self).payback(prize)
        self.money += prize

        # Saber se perdemos ou ganhamos
        draw = (prize == 0)
        win = (prize > 0)

        # Qual a nossa recompensa?
        # 1 - Ganhamos
        # 0 - Empatamos
        # -1 - Perdemos
        if win:
            if self.verbose:
                print("Ganhámos! :)")
            if self.winStreak+1 < len(self.bets):
                self.winStreak += 1

            reward = 1
            self.wins += 1
            self.twins += 1
        elif draw:
            if self.verbose:
                print("Empate :/")
            reward = 0
            self.draws += 1
            self.tdraws += 1
            self.winStreak = 0
        else:
            if self.verbose:
                print("Perdemos :(")
            reward = -1
            self.losses += 1
            self.tlosses += 1
            self.winStreak = 0

        # Atualizar os resultados do jogo de acordo com a nossa recompensa
        # (em caso de Double-Down a recompensa duplica pois foi feito o dobro da aposta)
        for key in self.firstResults:
            if key[1] == 'd':
                self.firstResults[key] = reward * 2
            else:
                self.firstResults[key] = reward

        for key in self.results:
            if key[1] == 'u':
                break
            self.results[key] = reward

        if len(self.firstResults) > 0:
            self.qFirst = updateTable(self.qFirst, self.countFirst, self.firstResults)

        if len(self.results) > 0:
            self.q = updateTable(self.q, self.count, self.results)

        # Prepara para o próximo jogo
        self.results = defaultdict(int)
        self.firstResults = defaultdict(int)
        self.firstPlay = True
        self.games += 1
        self.currentGames += 1
        self.fileGames += 1

        # Escrevemos a tabela no ficheiro a cada 10000 jogos
        if self.games % 10000 == 0:
            self.writeFile()
            self.writeLogFile()

    """
    --------------------------------------------------------------------------------------------------------
    FUNÇÕES AUXILIARES

    - getDealerValue  (obter o valor do dealer)
    - getPlayerValue  (obter o valor do jogador)
    - getUseableAce   (saber se o jogador tem soft/hard hand)
    - learning        (saber se o jogador está em aprendizagem)
    - getBestAction   (obter a melhor acção)
    - getRandomAction (obter uma acção aleatória dependendo se é a primeira jogada ou não)
    - writeLogFile    (escrever um ficheiro de log para acompanhar os resultados parciais e totais)
    - createFile      (criação do ficheiro com os dados do agente)
    - readFile        (leitura do ficheiro com os dados do agente)
    - writeFile       (escrita do ficheiro com os dados do agente)
    --------------------------------------------------------------------------------------------------------
    """

    # Obter valor do dealer
    def getDealerValue(self, dealer):
        dealerHand = card.value(dealer.hand)
        if len([c for c in dealer.hand if c.is_ace()]) > 0:
            dealerHand = 1
        return dealerHand

    # Obter valor da minha mão
    def getPlayerValue(self, players):
        for p in players:
            if p.player.name == self.name:
                return p.hand, card.value(p.hand)

    # Saber se tenho soft ou hard hand
    def getUseableAce(self, hand):
        numberAces = len([c for c in hand if c.is_ace()])
        if numberAces == 0:
            return False
        elif numberAces == 2 and len(hand) == 2 and (card.value(hand) == 12 or card.value(hand) == 2):
            return True
        handNoAce = card.value([c for c in hand if not c.is_ace()])
        return True if numberAces + handNoAce == card.value(hand) else False

    def learning(self, state, first):
        if first:
            stand = self.countFirst[(state, 's')]
            hit = self.countFirst[(state, 'h')]
            dd = self.countFirst[(state, 'd')]
            if (stand <= self.learnFactor or hit <= self.learnFactor or dd <= self.learnFactor):
                # True
                # -> epsilon greedy strategy: vamos deixá-lo explorar outras opções em 1% das vezes
                return False if random.random() < 0.01 else True
            return False
        stand = self.count[(state, 's')]
        hit = self.count[(state, 'h')]
        if (stand <= self.learnFactor or hit <= self.learnFactor):
            #True
            # -> epsilon greedy strategy: vamos deixá-lo explorar outras opções em 1% das vezes
            return False if random.random() < 0.01 else True
        return False

    def getBestAction(self, state, first):
        if first:
            hit = self.qFirst[(state, 'h')]
            stand = self.qFirst[(state, 's')]
            dd = self.qFirst[(state, 'd')]
            tmp = np.argmax(np.array([hit, stand, dd]))
            if tmp == 0:
                return 'h'
            elif tmp == 1:
                return 's'
            return 'd'
        hit = self.q[(state, 'h')]
        stand = self.q[(state, 's')]
        tmp = np.argmax(np.array([hit, stand]))
        aux = max(hit, stand)
        if aux <= self.surrenderFlag:
            return 'u'
        if tmp == 0:
            return 'h'
        return 's'

    def getRandomAction(self, first):
        if first:
            r = random.randint(0, 2)
            if r == 0:
                return 'h'
            elif r == 1:
                return 's'
            return 'd'
        return 'h' if random.random() < 0.5 else 's'

    def writeLogFile(self):
        # Escreve o dicionario no ficheiro
        file = open("studentPlayer-log.txt", "w")
        file.write("-------------------------------------------\n")
        file.write("Played {} games, won {}, draw {}, loss {}\n".format(self.currentGames, self.wins, self.draws, self.losses))
        file.write("Win Rate: {}%\n".format(self.wins/self.currentGames * 100))
        file.write("Total {} games, won {}, draw {}, loss {}\n".format(self.games, self.twins, self.tdraws, self.tlosses))
        file.write("Total Win Rate: {}%\n".format(self.twins / self.games * 100))
        self.losses = 0
        self.wins = 0
        self.draws = 0
        self.currentGames = 0
        file.close()

    def createFile(self):
        # Cria o ficheiro e fecha-o
        file = open("studentPlayer.data", "w+")
        file.close()

    def readFile(self):
        # Abrimos o dicionario em read-only mode e em binary mode
        file = open("studentPlayer.data", "rb")
        file.seek(0)
        tmpList = pickle.load(file)
        self.q = tmpList[0]
        self.qFirst = tmpList[1]
        self.count = tmpList[2]
        self.countFirst = tmpList[3]
        self.fileGames = tmpList[4]
        file.close()

    def writeFile(self):
        # Escreve o dicionario no ficheiro
        file = open("studentPlayer.data", "wb")
        file.seek(0)
        file.truncate()
        file.seek(0)
        tmpList = [self.q, self.qFirst, self.count, self.countFirst, self.fileGames]
        pickle.dump(tmpList, file)
        file.close()

"""
--------------------------------------------------------------------------------------------------------
FUNÇÕES AUXILIARES (extra-classe)

- initStates    : devolve uma lista com os estados possíveis no jogo
- initActions   : devolve um dicionário com os estados/acções possíveis no jogo
- initCount     : devolve um dicionário para a contagem de ocorrências dos estados/acções
- updateTable   : atualiza a tabela Q dada com os dados da contagem e resultados obtidos num jogo
--------------------------------------------------------------------------------------------------------
"""

def initStates():
    states = []
    for dealer in range(1, 11):
        for player in range(4, 21):
            states.append((dealer, player, False))
            states.append((dealer, player, True))
    return states

def initActions(states):
    q = defaultdict(float)
    for state in states:
        q[(state, 's')] = 0.0
        q[(state, 'h')] = 0.0
        q[(state, 'd')] = 0.0
    return q

def initCount(actions):
    count = defaultdict(int)
    for action in actions:
        count[action] = 0
    return count

def updateTable(table, count, results):
    for key in results:
        table[key] = table[key] + (1 / count[key]) * (results[key] - table[key])
    return table

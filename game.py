#encoding: utf8
__author__ = 'Diogo Gomes'
__email__ = 'dgomes@ua.pt'
__license__ = "GPL"
__version__ = "0.1"

import copy
import card
from shoe import Shoe
from dealer import Dealer
from player import Player

BET_MULTIPLIER = 2

class Game(object):
    class Rules():
        def __init__(self, shoe_size=4, min_bet=1, max_bet=10):
            self.shoe_size = shoe_size
            self.min_bet = min_bet
            self.max_bet = max_bet
            self.bet_multiplier = BET_MULTIPLIER
        def __str__(self):
            return "RULES\tMin bet: {}, Max bet: {}, Shoe size: {}, Bet multiplier: {}".format(self.min_bet, self.max_bet, self.shoe_size, self.bet_multiplier)
    class PlayerState():
        def __init__(self, p):
            self.player = p
            self.bet = 0
            self.hand = []
            self.bust = False
            self.done = False
            self.watch = False
        def copy(self):
            return copy.deepcopy(self)
        def __str__(self):
            if isinstance(self.player, Dealer):
                return "{}".format(self.hand)
            return "{} ({}€)".format(self.hand, self.bet)
        def __repr__(self):
            return "{}".format(self.player.name)
        def hide_card(self):
            h = self.copy()
            h.hand = h.hand[1:]
            return h
        def want_to_play(self, rules):
            return self.player.want_to_play(rules)
        def take_bet(self, state, rules):
            bet = 0
            while (bet!=self.bet and self.bet!=0) or not (rules.min_bet <= bet <= rules.max_bet) :      #bets can't be 0 and double down means double down
                bet = self.player.bet(state[0].hide_card(), state[1:])
            self.bet += bet

    def __init__(self, players, shoe_size=4, debug=False, verbose=True, min_bet=1, max_bet=10, shoe=None):
        if verbose:
    #       print(chr(27) + "[2J")
            print("-"*80)
        self.verbose = verbose
        self.debug = debug
        self.rules = self.Rules(shoe_size=shoe_size, min_bet=min_bet, max_bet=max_bet)
        self.shoe = Shoe(shoe_size)
        if shoe != None:
            self.shoe = shoe
        self.shoe.shuffle()
        self.state = [self.PlayerState(Dealer())] + [self.PlayerState(p) for p in players]

        self.done = False

    def str_players_hands(self):
        o = ""
        for p in self.state[1:]:
            o+="{!s:^45}".format(p)
        return o

    def str_players_names(self):
        o = ""
        for p in self.state[1:]:
            o+="{!s:^35}".format(p.player)
        return o

    """
    def __str__(self):
        return (\
        "{:^30}\n"\
        "╔"+"═══════════════════════════════"*(len(self.state)-1)+"╗\n"\
        "{!s:^45}\n"\
        "                         \n"\
        "                         \n"\
        "                         \n"\
        "                         \n"\
        "                         \n"\
        "{!s}\n"\
        "╚"+"═══════════════════════════════"*(len(self.state)-1)+"╝\n"\
        "{}\n"\
        ).format(self.state[0].player.name, self.state[0].hand if self.done else (["**"]+self.state[0].hide_card().hand if len(self.state[0].hand) else []), self.str_players_hands(), self.str_players_names())
    """

    def deal(self, num):
        return self.shoe.deal_cards(1)

    def take_bets(self):
        if self.debug:
            print(self)
        for p in self.state[1:]:
            if p.want_to_play(self.rules):
                p.take_bet(self.state, self.rules)
            else:
                p.watch = True

    def loop(self):

        #deal initial cards
        self.state[0].hand += self.shoe.deal_cards(2)
        for p in self.state[1:]:
            if not p.watch:
                p.hand += self.shoe.deal_cards(2)

        turn = 0
        if card.blackjack(self.state[0].hand):  #if the dealer has blackjack there is no point in playing...
            self.done = True
            return [p for p in self.state[1:] if card.blackjack(p.hand)]

        #lets play
        while not self.done:
            turn += 1
            hits = 0
            for p in self.state[::-1]:
                if p.watch or p.bust or p.done or card.value(p.hand) == 21:  #skip players watching, bust players, players who have double down and players who already have blackjack!
                    continue

                if self.debug:
                    print("TURN {}: {}".format(turn, p.player.name))
                    print(self)
                action = ""
                while action not in ["h", "s", "d", "u"]:
                    if isinstance(p.player, Dealer):
                        action = p.player.play(self.state[0], self.state[1:])
                    else:
                        action = p.player.play(self.state[0].hide_card(), self.state[1:])
                    if action == "d" and turn != 1:
                        print("YOU CAN'T DOUBLE DOWN!!! double down is only available on the 1st turn")
                        action = ""

                if action == "u":
                    p.watch = True
                    continue

                if action == "d":
                    p.take_bet(self.state,self.rules)
                    p.done = True

                if action in ["h", "d"]:
                    p.hand+=self.deal(1)
                    hits +=1

                if card.value(p.hand) >= 21:
                    if card.value(p.hand) > 21:
                        p.bust = True
                    else:
                        p.done = True   #already has blackjack
                    if isinstance(p.player, Dealer):
                        self.done = True #game is over we already have a blackjack
            if hits == 0:
                self.done = True

        self.done = True

        return [p for p in self.state if
            not isinstance(p.player, Dealer) and    #Dealer is not really a winner
            not card.blackjack(self.state[0].hand) and  #If dealer gets blackjack no one wins
            not p.watch and  #players watching can't win :)
            not p.bust and  #bust players can't win :)
            (card.value(p.hand) >= card.value(self.state[0].hand) or self.state[0].bust)    #winners have more points then the dealer or the dealer has gone bust
            ]

    def show_table(self):
        for p in self.state[1:]:
            p.player.show(self.state)

    def payback(self, winners):
        for p in self.state[1:]:
            if p.watch:
                #check if player surrendered
                if p.bet > 0:
                    p.player.payback(-p.bet//2) #this means the player lost half his bet
                #skip watchers
                continue
            if p in winners and card.value(self.state[0].hand) == card.value(p.hand):
                p.player.payback(0)  #bet is returned
            elif p in winners:
                p.player.payback(-p.bet + p.bet*BET_MULTIPLIER)
            else:
                p.player.payback(-p.bet) #this means the player lost

    def run(self):
        self.take_bets()
        winners = self.loop()
        self.show_table()
        self.payback(winners)
        if self.verbose:
            print(self)
            print("🏆    Winners: "+str(winners))


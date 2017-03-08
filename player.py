#encoding: utf8
__author__ = 'Diogo Gomes'
__email__ = 'dgomes@ua.pt'
__license__ = "GPL"
__version__ = "0.1"
import card

class Player(object):
    def __init__(self, name="Player", money=0):
        self.name = name
        self.pocket = money #dont mess with pocket!
        self.table = 0

    def __str__(self):
        return "{} ({}€)".format(self.name, self.pocket-self.table)

    def __repr__(self):
        return self.__str__()

# MIGHT want to re-implement the next methods
    def show(self, players): #will receive a list containing all the players in the table and respective hands. this method is called before payback and represents the end state
        #example: print "SHOW:", {p.player.name: p.hand for p in players}
        pass

    def want_to_play(self, rules):     #if you have to much money and jut want to watch, return False
                                        # rules contains a Game.Rules object with information on the game rules (min_bet, max_bet, shoe_size, etc)
        print(rules)
        return True

    def payback(self, prize):
        """ receives bet + premium
            of 0 if both player and dealer have black jack
            or -bet if player lost
        """
        self.table = 0
        self.pocket += prize

    def debug_state(self, dealer, players):
        print("{:10s}: {!s:32s} = {}".format("Dealer", ['🎴 '] + dealer.hand, card.value(dealer.hand)))
        for p in players:
            print("{:10s}: {!s:32s} = {}".format(p.player.name, p.hand, card.value(p.hand)))

# MANDATORY to re-implement all the next methods
    def play(self, dealer, players):
        """ Calculates decision to take
            Must be either "h", "d", "s" or "u" - Hit, Double down, Stand, S(u)rrender
            Hit -> player gets an extra card
            Double Down -> player can bet extra money (up to 100% of the initial bet) and a LAST extra card
            Stand -> player does not wish to make any move in the current turn
            Surrender -> player receives back half of his bet
        """
        self.debug_state(dealer, players)
        return input("(h)it (d)ouble (s)tand or s(u)rrender ")

    def bet(self, dealer, players):
        """ Calculates how much to bet
            dealer - state
            players - list of players state

            returns:
            bet (int value)
        """
        self.debug_state(dealer, players)
        try:
            bet = int(input("bet: "))
        except Exception as e:
            bet = 1
        self.table = bet
        return bet

#encoding: utf8
__author__ = 'Diogo Gomes'
__email__ = 'dgomes@ua.pt'
__license__ = "GPL"
__version__ = "0.1"
import card
from player import Player

class Dealer(Player):
    def __init__(self):
        self.hand = []
        self.name = "Dealer"
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()

    def play(self, dealer, players):
        if card.value(dealer.hand) < 17:
            return "h"
        return "s"

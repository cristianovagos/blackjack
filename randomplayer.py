#encoding: utf8
__author__ = 'Diogo Gomes'
__email__ = 'dgomes@ua.pt'
__license__ = "GPL"
__version__ = "0.1"
import card
import random
from player import Player

class RandomPlayer(Player):
    def __init__(self, name="RandomPlayer", money=0):
        super(RandomPlayer, self).__init__(name, money)

    def play(self, dealer, players):
        """ Calculates decision to take
            Must be either "h" or "s"

            dealer - state
            players - list of players state
        """
        cmd = ["h", "s"]
        return cmd[random.randint(0,1)]

    def bet(self, dealer, players):
        """ Calculates how much to bet (int)

            dealer - state
            players - list of players state
        """
        return 1

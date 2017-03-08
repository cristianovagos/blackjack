#encoding: utf8
__author__ = 'Diogo Gomes'
__email__ = 'dgomes@ua.pt'
__license__ = "GPL"
__version__ = "0.1"


import random

class Card(object):
    suit_names = ["♠️", "♣️", "♦️", "♥️"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=0, rank=1):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """Returns a human-readable string representation."""
        return '{}{} '.format(Card.rank_names[self.rank], Card.suit_names[self.suit])

    def __repr__(self):
        return self.__str__()

    def value(self):
        return self.rank if self.rank < 10 else 10

    def is_ace(self):
        if self.rank == 1:
            return True
        return False
    def is_ten(self):
        if self.rank >= 10:
            return True
        return False

def value(hand):    
    v = sum([c.value() for c in hand]) 
    if len([c for c in hand if c.is_ace()]) > 0 and v <= 11: #if there is an Ace and we don't bust by take the Ace as an eleven
        return v+10 
    return v

def blackjack(hand):
    if len(hand) == 2 and hand[0].is_ace() and hand[1].is_ten():
        return True
    if len(hand) == 2 and hand[1].is_ace() and hand[0].is_ten():
        return True
    return False
    
if __name__ == '__main__':
    shoe = Shoe()
    shoe.shuffle()

    print(shoe.deal_cards(2))


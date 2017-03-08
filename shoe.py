#encoding: utf8
__author__ = 'Diogo Gomes'
__email__ = 'dgomes@ua.pt'
__license__ = "GPL"
__version__ = "0.1"

from card import Card
import random

class Shoe(object):
    #Represents one or more decks of cards use to
    #take cards for players and dealer

    def __init__(self, number_decks=1):
        self.cards = []
        for i in range(number_decks):
            self.cards += [Card(suit, rank) for suit in range(4) for rank in range(1,14)]

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def pop_card(self, i=-1):
        """Removes and returns a card from the deck.

        i: index of the card to pop; by default, pops the last card.
        """
        return self.cards.pop(i)

    def shuffle(self):
        """Shuffles the cards in this deck."""
        random.shuffle(self.cards)

    def sort(self):
        """Sorts the cards in ascending order."""
        self.cards.sort()

    def deal_cards(self, num):
        """Moves the given number of cards from the deck

        num: integer number of cards to move
        """
        deal = []
        for i in range(num):
            deal.append(self.pop_card())
        return deal

if __name__ == '__main__':
    shoe = Shoe()
    shoe.shuffle()

    print(shoe.deal_cards(2))


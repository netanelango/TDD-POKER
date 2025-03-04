import random

SUITS = ['coeur', 'carreau', 'trèfle', 'pique']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R', 'A']

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num):
        if num > len(self.cards):
            raise ValueError("Pas assez de cartes dans le paquet")
        dealt_cards = self.cards[:num]
        self.cards = self.cards[num:]
        return dealt_cards

if __name__ == '__main__':
    deck = Deck()
    print("Jeu initial :", deck.cards)
    deck.shuffle()
    print("Jeu mélangé :", deck.cards)
    hand = deck.deal(5)
    print("Main distribuée :", hand)

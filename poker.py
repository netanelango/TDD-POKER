import random

SUITS = ['coeur', 'carreau', 'trèfle', 'pique']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R', 'A']
RANK_VALUES = {rank: i for i, rank in enumerate(RANKS, start=2)}

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

        from collections import Counter


class PokerHand:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError("Une main de poker doit comporter 5 cartes")
        self.cards = cards
        self.values = sorted([RANK_VALUES[card.rank] for card in cards])
        self.suits = [card.suit for card in cards]
        self.rank_counts = Counter(card.rank for card in cards)
    
    def is_flush(self):
        """Vérifie si toutes les cartes sont de la même couleur (flush)."""
        return len(set(self.suits)) == 1
    
    def is_straight(self):
        """Vérifie si les cartes forment une suite (straight)."""
        values = sorted(self.values)
        if values == list(range(min(values), min(values) + 5)):
            return True
        if set(self.values) == {RANK_VALUES['A'], RANK_VALUES['2'], RANK_VALUES['3'], RANK_VALUES['4'], RANK_VALUES['5']}:
            return True
        return False

    def classify(self):
        """
        Évalue et retourne la combinaison de la main sous forme de tuple 
        (nom_de_la_combinaison, niveau).
        """
        is_flush = self.is_flush()
        is_straight = self.is_straight()
        counts = self.rank_counts.most_common()

        if is_flush and set(card.rank for card in self.cards) == {'A', 'R', 'D', 'V', '10'}:
            return ("Quinte Flush Royale", 10)
        if is_flush and is_straight:
            return ("Quinte Flush", 9)
        if counts[0][1] == 4:
            return ("Carré", 8)
        if counts[0][1] == 3 and counts[1][1] == 2:
            return ("Full", 7)
        if is_flush:
            return ("Couleur", 6)
        if is_straight:
            return ("Quinte", 5)
        if counts[0][1] == 3:
            return ("Brelan", 4)
        if len([rank for rank, count in counts if count == 2]) == 2:
            return ("Deux Paires", 3)
        if counts[0][1] == 2:
            return ("Paire", 2)
        return ("Carte Haute", 1)
    
    def __repr__(self):
        return " ".join(str(card) for card in self.cards)


if __name__ == '__main__':
    deck = Deck()
    print("Jeu initial :", deck.cards)
    deck.shuffle()
    print("Jeu mélangé :", deck.cards)
    hand = deck.deal(5)
    print("Main distribuée :", hand)

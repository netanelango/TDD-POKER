import random
import unittest
from collections import Counter

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
        dealt = self.cards[:num]
        self.cards = self.cards[num:]
        return dealt

class PokerHand:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError("Une main de poker doit comporter 5 cartes")
        self.cards = cards
        self.values = sorted([RANK_VALUES[card.rank] for card in cards])
        self.suits = [card.suit for card in cards]
        self.rank_counts = Counter(card.rank for card in cards)
    
    def is_flush(self):
        return len(set(self.suits)) == 1

    def is_straight(self):
        values = sorted(self.values)
        if values == list(range(min(values), min(values) + 5)):
            return True
        if set(values) == {RANK_VALUES['A'], RANK_VALUES['2'], RANK_VALUES['3'], RANK_VALUES['4'], RANK_VALUES['5']}:
            return True
        return False

    def classify(self):
        """
        Retourne un tuple (nom_de_la_combinaison, niveau) selon l'ordre défini.
        Le niveau permet un classement numérique (plus haut = main forte).
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

def play_poker():
    deck = Deck()
    deck.shuffle()
    hand_cards = deck.deal(5)
    hand = PokerHand(hand_cards)
    print("Main :", hand)
    classification, level = hand.classify()
    print("Classification :", classification)
    return hand, classification, level

if __name__ == "__main__":
    play_poker()

class TestPokerHand(unittest.TestCase):
    def test_royal_flush(self):
        cards = [Card('A', 'coeur'), Card('R', 'coeur'), Card('D', 'coeur'),
                 Card('V', 'coeur'), Card('10', 'coeur')]
        hand = PokerHand(cards)
        self.assertEqual(hand.classify()[0], "Quinte Flush Royale")
    
    def test_straight_flush(self):
        cards = [Card('9', 'pique'), Card('8', 'pique'), Card('7', 'pique'),
                 Card('6', 'pique'), Card('5', 'pique')]
        hand = PokerHand(cards)
        self.assertEqual(hand.classify()[0], "Quinte Flush")
    
    def test_four_of_a_kind(self):
        cards = [Card('7', 'coeur'), Card('7', 'carreau'), Card('7', 'pique'),
                 Card('7', 'trèfle'), Card('9', 'coeur')]
        hand = PokerHand(cards)
        self.assertEqual(hand.classify()[0], "Carré")
    
    def test_full_house(self):
        cards = [Card('10', 'coeur'), Card('10', 'carreau'), Card('10', 'pique'),
                 Card('4', 'trèfle'), Card('4', 'coeur')]
        hand = PokerHand(cards)
        self.assertEqual(hand.classify()[0], "Full")
    
    def test_flush(self):
        cards = [Card('A', 'trèfle'), Card('10', 'trèfle'), Card('7', 'trèfle'),
                 Card('6', 'trèfle'), Card('2', 'trèfle')]
        hand = PokerHand(cards)
        self.assertEqual(hand.classify()[0], "Couleur")
    
    def test_straight(self):
        cards = [Card('9', 'coeur'), Card('8', 'trèfle'), Card('7', 'pique'),
                 Card('6', 'carreau'), Card('5', 'coeur')]
        hand = PokerHand(cards)
        self.assertEqual(hand.classify()[0], "Quinte")
    
    def test_three_of_a_kind(self):
        cards = [Card('8', 'coeur'), Card('8', 'carreau'), Card('8', 'pique'),
                 Card('R', 'trèfle'), Card('3', 'carreau')]
        hand = PokerHand(cards)
        self.assertEqual(hand.classify()[0], "Brelan")
    
    def test_two_pair(self):
        cards = [Card('V', 'coeur'), Card('V', 'trèfle'), Card('4', 'pique'),
                 Card('4', 'coeur'), Card('A', 'carreau')]
        hand = PokerHand(cards)
        self.assertEqual(hand.classify()[0], "Deux Paires")
    
    def test_one_pair(self):
        cards = [Card('10', 'coeur'), Card('10', 'trèfle'), Card('R', 'pique'),
                 Card('4', 'coeur'), Card('3', 'carreau')]
        hand = PokerHand(cards)
        self.assertEqual(hand.classify()[0], "Paire")
    
    def test_high_card(self):
        cards = [Card('2', 'coeur'), Card('5', 'carreau'), Card('7', 'trèfle'),
                 Card('9', 'trèfle'), Card('V', 'coeur')]
        hand = PokerHand(cards)
        self.assertEqual(hand.classify()[0], "Carte Haute")

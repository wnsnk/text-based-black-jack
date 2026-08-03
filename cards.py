import random


class Card():
    def __init__(self, symbol, value, suit):
        self.symbol = symbol
        self.value = value
        self.suit = suit


placeholder = Card('?', '?', '?')


def create_deck():
    suits = ['♣', '♦', '♥', '♠']
    deck = []

    for suit in suits:
        for num in range(2, 11):
            deck.append(Card(num, num, suit))
        deck.append(Card('J', 10, suit))
        deck.append(Card('Q', 10, suit))
        deck.append(Card('K', 10, suit))
        deck.append(Card('A', 11, suit))
        # TODO: Fix Ace
    return deck


def shuffle_cards(deck):
    random_number = random.randint(100, 100000)
    for shuffle in range(random_number):
        random.shuffle(deck)
    return deck

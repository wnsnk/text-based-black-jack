import time
from cards import placeholder


class Dealer():
    def __init__(self, deck):
        self.cards = []
        self.secret_card = None
        self.deck = deck

    def deal_card(self, player):
        player.cards.append(self.deck[0])
        self.deck.pop(0)

    def deal_secret_card(self):
        self.secret_card = self.deck[0]
        self.deck.pop(0)
        self.cards.append(placeholder)

    def deal_starting_cards(self, players: list):
        for player in players:
            self.deal_card(player)
            self.print_player_cards(player)

        self.deal_card(self)
        self.print_dealer_cards()

        print('\n' * 10)

        for player in players:
            self.deal_card(player)
            self.print_player_cards(player)

        self.deal_secret_card()
        self.print_dealer_cards()
        print('-------------------------------------')

    def print_player_cards(self, player):
        print(f'Player {player.number} cards:')
        for card in player.cards:
            print(card.symbol, card.suit)

    def print_dealer_cards(self):
        print('Dealer cards:')
        for card in self.cards:
            print(card.symbol, card.suit)
            time.sleep(2)

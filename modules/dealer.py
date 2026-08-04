import time
from modules.cards import placeholder
from .cards import create_deck, shuffle_cards

dotted_line = '-------------------------------------'


class Dealer():
    def __init__(self, deck):
        self.cards = []
        self.secret_card = None
        self.deck = deck
        self.end_game = False
        self.score = 0
        self.bust = False

    def take_bets(self, players):
        for player in players:
            player.bet_money()

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

            if player.cards[0].value + player.cards[1].value == 21:
                print(f'Player {player.number} has Black Jack!')
                player.score = 21
                player.has_blackjack = True

        self.deal_secret_card()
        self.print_dealer_cards()
        if self.cards[0].value + self.secret_card.value == 21:
            print('Dealer has Black Jack!')
            self.show_secret_card()
            print('End of game.')
            self.end_game = True
        print(dotted_line)

    def print_player_cards(self, player):
        print(f'Player {player.number} cards:')
        for card in player.cards:
            print(card.symbol, card.suit)
        time.sleep(1)

    def print_dealer_cards(self):
        print('Dealer cards:')
        for card in self.cards:
            print(card.symbol, card.suit)
        time.sleep(1)

    def start_game(self, players):
        for player in players:
            if player.has_blackjack:
                print(f'Player {player.number} already has black jack.')
                time.sleep(1)
                print()
                continue
            player.turn(dealer=self)
            time.sleep(1)
            print()

    def show_secret_card(self):
        self.cards.pop(1)
        self.cards.append(self.secret_card)
        self.print_dealer_cards()

    def calc_value(self):
        value_list = []
        for card in self.cards:
            value_list.append(card.value)
        return sum(value_list)

    def turn(self):
        self.show_secret_card()
        self.score = self.calc_value()
        while self.score < 17:
            self.deal_card(self)
            self.print_dealer_cards()
            self.score = self.calc_value()
            print(f'Total Value: {self.score}')

        if self.score > 21:
            print('Dealer bust')
            self.bust = True

    def compare_scores(self, players):
        for player in players:
            if player.bust:
                continue
            elif player.has_blackjack:
                player.bet = player.bet * 2.5
                player.money += player.bet
                print(
                    f'Player {player.number} had Black Jack! Money: ${player.money}')
            elif self.bust:
                player.bet = player.bet * 2
                player.money += player.bet
                print(f'Player {player.number} won! Money: ${player.money}')
            elif player.score > self.score:
                player.bet = player.bet * 2
                player.money += player.bet
                print(f'Player {player.number} won! Money: ${player.money}')
            elif player.score == self.score:
                player.money += player.bet
                print(
                    f'Player {player.number} tied! Money: ${player.money}')
            else:
                print(
                    f'Player {player.number} Lost! Money: ${player.money}')

    def reset_game(self, players):
        for player in players:
            player.bet = 0
            player.cards = []
            player.score = 0
            player.has_blackjack = False
            player.bust = False

        self.cards = []
        self.secret_card = None
        self.score = 0
        self.bust = False
        self.end_game = False
        deck = create_deck()
        shuffle_cards(deck)
        self.deck = deck

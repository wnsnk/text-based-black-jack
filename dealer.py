import time
from cards import placeholder


class Dealer():
    def __init__(self, deck):
        self.cards = []
        self.secret_card = None
        self.deck = deck
        self.end_game = False

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
                player.bet * 2.5
                player.money += player.bet
                print(
                    f'${player.bet} added to Player {player.number}\'s money (${player.money})')

        self.deal_secret_card()
        self.print_dealer_cards()
        if self.cards[0].value + self.secret_card.value == 21:
            print('Dealer has Black Jack!')
            self.cards.pop(1)
            self.cards.append(self.secret_card)
            self.print_dealer_cards()
            print('End of game.')
            self.end_game = True
        print('-------------------------------------')

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

    # TODO: Add ending

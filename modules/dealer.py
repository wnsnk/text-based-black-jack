import time
from modules.cards import placeholder
from .cards import create_deck, shuffle_cards, Card
from .player import Player

dotted_line = '-------------------------------------'


class Dealer():
    def __init__(self, deck):
        self.cards: list[Card]
        self.cards = []
        self.secret_card: Card
        self.secret_card = None
        self.deck = deck
        self.end_game = False
        self.score = 0
        self.bust = False

    def take_bets(self, players):
        '''Ask Players to place a bet'''
        for player in players:
            player: Player
            player.bet_money()

    def deal_card(self, player):
        '''Deal 1 card to Player'''
        player.cards.append(self.deck[0])
        self.deck.pop(0)

    def deal_secret_card(self):
        '''Deal upside down card to self'''
        self.secret_card = self.deck[0]
        self.deck.pop(0)
        self.cards.append(placeholder)

    def deal_starting_cards(self, players: list[Player]):
        '''Deal the Starting cards to Players and self'''
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

    def print_player_cards(self, player: Player):
        '''Prints player cards'''
        print(f'Player {player.number} cards:')
        for card in player.cards:
            print(card.symbol, card.suit)
        time.sleep(1)

    def print_dealer_cards(self):
        '''Prints Dealer Cards'''
        print('Dealer cards:')
        for card in self.cards:
            card: Card
            print(card.symbol, card.suit)
        time.sleep(1)

    def start_game(self, players: list[Player]):
        '''starts the game after all players and dealer get their starting cards'''
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
        '''Removes the secret card from self.cards, appends the actual secret card to self.cards and then prints the dealer cards.'''
        self.cards.pop(1)
        self.cards.append(self.secret_card)
        self.print_dealer_cards()

    def calc_value(self) -> int:
        '''Calculate the value of Dealer Hand'''
        value_list = []
        for card in self.cards:
            card: Card
            value_list.append(card.value)
        return sum(value_list)

    def turn(self):
        '''Start dealer turn. '''
        self.show_secret_card()
        self.score = self.calc_value()
        while self.score < 17:
            self.deal_card(self)
            self.print_dealer_cards()
            self.score = self.calc_value()
            if self.score > 21:
                self.calc_ace_value()
            print(f'Total Value: {self.score}')

        if self.score > 21:
            print('Dealer bust')
            self.bust = True

    def calc_ace_value(self):
        '''Calculates if an Ace should count as 11 or as 1'''
        if self.score > 21:
            for card in self.cards:
                card: Card
                if card.symbol == 'A' and card.value == 11:
                    card.value = 1
                    self.score = self.calc_value()
                    print('score:', self.score)
                    if self.score > 21:
                        continue
                    else:
                        break

    def compare_scores(self, players: list[Player]):
        '''Compares the scores of all Players Against the score of the Dealer and handles wins or losses'''
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
        '''Resets all variables of player except Player.money, resets all variables of self.'''
        for player in players:
            player: Player
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

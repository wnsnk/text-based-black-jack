import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .dealer import Dealer
    from ..q_learning import QLearningBot
from .cards import Card
from ._print import dotted_line
import random


class Player():
    def __init__(self, number):
        self.number = number
        self.cards: list[Card]
        self.cards = []
        self.money = 1000
        self.bet = 0
        self.score = 0
        self.has_blackjack = False
        self.bust = False
        self.total_wins = 0
        self.total_losses = 0
        self.total_ties = 0

    def bet_money(self):
        '''Ask user how much money to bet'''
        print(dotted_line)
        if self.money < 1:
            print('YOU LOST ALL YOUR MONEY, GAME OVER!')
            self.bust = True
            # TODO: Stop player from continuing
            return
        legal_bet = False
        while not legal_bet:
            print(f'Player {self.number}: You have ${self.money}')
            try:
                self.bet = int(input('How much would you like to bet?\n'))
            except ValueError:
                print('You can only bet money!')
                # time.sleep(2)
                self.bet_money()
            if self.bet > self.money:
                print('Not enough money!')
            elif self.bet <= 0:
                print('Can\'t bet zero or lower!')
            else:
                legal_bet = True
            self.money -= self.bet

    def print_info(self, total_value):
        '''print info about value, money and current bet to terminal'''
        print(f'Total Value: {total_value}')
        print(f'Money ${self.money}')
        print(f'Current bet: ${self.bet}')

    def calc_value(self) -> int:
        '''Calculate the value of player hand'''
        value_list = []
        for card in self.cards:
            card: Card
            value_list.append(card.value)
        return sum(value_list)

    def turn(self, dealer: Dealer):
        '''Starts the turn of the player'''
        count = 0
        self.options = ['stand', 'hit']
        if self.money >= self.bet:
            self.options.append('double down')
        # if self.cards[0].value == self.cards[1].value:
        #     self.options.append('split')

        end_of_turn = False

        while not end_of_turn:
            count += 1
            self.print_player_cards()
            self.score = self.calc_value()
            if self.score > 21:
                self.calc_ace_value()
            self.print_info(self.score)

            if self.score == 21:
                print('You have 21! End of turn')
                end_of_turn = True
                return
            elif self.score > 21:
                print('Bust!')
                self.bust = True
                end_of_turn = True
                return

            legal_move = False
            while not legal_move:
                print('What would you like to do:')
                print(self.options)
                self.choice = input().lower()
                if self.choice not in self.options:
                    print('Not a legal move!')
                else:
                    legal_move = True
            if self.choice == 'stand':
                end_of_turn = True
            elif self.choice == 'hit':
                dealer.deal_card(self)
            elif self.choice == 'double down':
                self.money -= self.bet
                self.bet = self.bet * 2
                print('Doubled Down!')
                dealer.deal_card(self)
                self.print_player_cards()
                self.score = self.calc_value()
                self.print_info(self.score)
                end_of_turn = True
            elif self.choice == 'split':
                self.options.remove('split')
                # TODO
            try:
                self.options.remove('double down')
            except ValueError:
                pass

    def print_player_cards(self):
        '''Print all cards from self to console'''
        print(f'Player {self.number} cards:')
        for card in self.cards:
            print(card.symbol, card.suit)
        # time.sleep(1)

    def hit(self, dealer: Dealer):
        '''Get extra card from dealer'''
        dealer.deal_card(self)

    def calc_ace_value(self):
        '''Calculates if an Ace should be 11 or 1'''
        if self.score > 21:
            for card in self.cards:
                if card.symbol == 'A' and card.value == 11:
                    card.value = 1
                    self.score = self.calc_value()
                    print('score:', self.score)
                    if self.score > 21:
                        continue
                    else:
                        break


class AIPlayer(Player):
    def __init__(self, number, AI: QLearningBot):
        super().__init__(number)
        self.AI = AI
        self.state = None
        self.action = None

    def bet_money(self):
        betting_choices = [10, 25, 50, 100, 250]
        for bet in betting_choices:
            if bet > self.money:
                betting_choices.remove(bet)
        # first choose random bet? maybe later train ai to also bet?
        self.bet = random.choice(betting_choices)
        print(f'Player {self.number} (AI) bets ${self.bet}')

    def turn(self, dealer: Dealer):
        count = 0
        self.options = ['stand', 'hit']
        if self.money >= self.bet:
            self.options.append('double down')
            self.can_double_down = True
        else:
            self.can_double_down = False

        end_of_turn = False

        while not end_of_turn:
            count += 1
            self.print_player_cards()
            self.score = self.calc_value()
            if self.score > 21:
                self.calc_ace_value()
            self.print_info(self.score)

            if self.score == 21:
                print('You have 21! End of turn')
                end_of_turn = True
                return
            elif self.score > 21:
                print('Bust!')
                self.bust = True
                end_of_turn = True
                return
            if count > 1:
                print('2nd round')
                self.AI.get_reward(state=self.state, action=self.action, next_state=self.AI.calc_state(
                    self.score, dealer.calc_value()), reward=0.5, done=False)
            legal_move = False
            while not legal_move:
                print('What would you like to do:')
                print(self.options)
                self.state = self.AI.calc_state(
                    self_value=self.calc_value(), dealer_value=dealer.calc_value())
                self.action = self.AI.choose_action(
                    self.state, can_double_down=self.can_double_down)

                # if self.choice not in self.options:
                #     print('Not a legal move!')
                # else:
                legal_move = True
            if self.action == 0:
                end_of_turn = True
            elif self.action == 1:
                dealer.deal_card(self)
            elif self.action == 2:
                self.money -= self.bet
                self.bet = self.bet * 2
                print('Doubled Down!')
                dealer.deal_card(self)
                self.print_player_cards()
                self.score = self.calc_value()
                self.print_info(self.score)
                end_of_turn = True
            elif self.choice == 'split':
                self.options.remove('split')
                # TODO
            try:
                self.options.remove('double down')
                self.can_double_down = False
            except ValueError:
                pass

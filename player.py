import time


class Player():
    def __init__(self, number):
        self.number = number
        self.cards = []
        self.money = 10000
        self.bet = 0
        self.score = 0
        self.has_blackjack = False

    def bet_money(self):
        print('\n' * 20)
        legal_bet = False
        while not legal_bet:
            print(f'Player {self.number}: You have ${self.money}')
            try:
                self.bet = int(input('How much would you like to bet?\n'))
            except ValueError:
                print('You can only bet money!')
                time.sleep(2)
                self.bet_money()
            if self.bet > self.money:
                print('Not enough money!')
            elif self.bet <= 0:
                print('Can\'t bet zero or lower!')
            else:
                legal_bet = True
            self.money -= self.bet

    def turn(self, dealer):
        count = 0
        self.options = ['stand', 'hit']
        if self.money > self.bet:
            self.options.append('double down')
        if self.cards[0].value == self.cards[1].value:
            self.options.append('split')

        end_of_turn = False

        while not end_of_turn:
            count += 1
            self.print_player_cards()
            total_value = 0
            for card in self.cards:
                total_value += card.value
            print(f'Total Value: {total_value}')
            print(f'Money ${self.money}')
            print(f'Current bet: {self.bet}')
            # if count == 1 and total_value == 21:
            #     print('BLACK JACK!!!')
            #     self.bet * 2.5
            #     self.money += self.bet
            #     print(f'Money ${self.money}')
            #     end_of_turn = True
            if total_value == 21:
                print('You have 21! End of turn')
                self.score = total_value
                end_of_turn = True
                return
            elif total_value > 21:
                print('Bust!')
                self.score = 0
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
            elif self.choice == 'double down' or self.choice == 'dd':
                self.money -= self.bet
                self.bet * 2
                print('Doubled Down!')
                dealer.deal_card(self)
            elif self.choice == 'split':
                self.options.remove('split')
                # TODO
            try:
                self.options.remove('double down')
            except ValueError:
                pass

    def print_player_cards(self):
        print(f'Player {self.number} cards:')
        for card in self.cards:
            print(card.symbol, card.suit)
        time.sleep(1)

    def hit(self, dealer):
        dealer.deal_card(self)

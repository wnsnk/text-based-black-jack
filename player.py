import time


class Player():
    def __init__(self, number):
        self.number = number
        self.cards = []
        self.money = 10000
        self.bet = 0

    def turn(self):
        self.print_player_cards()
        self.options = ['stand', 'hit']
        if self.money > self.bet:
            self.options.append('double down')
        if self.cards[0].value == self.cards[1].value:
            self.options.append('split')
        print('What would you like to do:')
        self.choice = input(self.options)

    def print_player_cards(self):
        print(f'Player {self.number} cards:')
        for card in self.cards:
            print(card.symbol, card.suit)
        time.sleep(1)

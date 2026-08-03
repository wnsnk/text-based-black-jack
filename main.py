from cards import create_deck, shuffle_cards
from dealer import Dealer
from player import Player
import random

deck = create_deck()
shuffle_cards(deck)

dealer = Dealer(deck)

PLAYERS = 3
player_list = []
for num in range(PLAYERS):
    player = Player(num + 1)
    player_list.append(player)

# dealer.take_bets(player_list)
dealer.deal_starting_cards(player_list)
dealer.start_game(player_list)

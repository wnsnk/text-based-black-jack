from modules.cards import create_deck, shuffle_cards
from modules.dealer import Dealer
from modules.player import Player, AIPlayer
import random

deck = create_deck()
shuffle_cards(deck)

dealer = Dealer(deck)

PLAYERS = 1
AI_PLAYERS = 1
player_list = []
for num in range(PLAYERS):
    player = Player(num + 1)
    player_list.append(player)

for num in range(AI_PLAYERS):
    player = AIPlayer(len(player_list) + 1, AI=None)
    player_list.append(player)


def reset():
    dealer.reset_game(player_list)
    dealer.take_bets(player_list)
    dealer.deal_starting_cards(player_list)
    if not dealer.end_game:
        dealer.start_game(player_list)
    dealer.turn()
    dealer.compare_scores(player_list)


while True:
    reset()

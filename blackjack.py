from modules.cards import create_deck, shuffle_cards
from modules.dealer import Dealer
from modules.player import Player, AIPlayer
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from q_learning import QLearningBot


class BlackJack():
    def __init__(self, num_players: int, num_ai_players: int, AI: QLearningBot):

        self.deck = create_deck()
        shuffle_cards(self.deck)
        self.dealer = Dealer(self.deck)

        self.PLAYERS = num_players
        self.AI_PLAYERS = num_ai_players
        self.player_list = []
        self.ai_player: AIPlayer
        for num in range(self.PLAYERS):
            player = Player(num + 1)
            self.player_list.append(player)

        for num in range(self.AI_PLAYERS):
            player = AIPlayer(len(self.player_list) + 1, AI=AI)
            self.ai_player = player
            self.player_list.append(player)

    def reset(self):
        self.dealer.reset_game(self.player_list)
        self.dealer.take_bets(self.player_list)
        self.dealer.deal_starting_cards(self.player_list)
        if not self.dealer.end_game:
            self.dealer.start_game(self.player_list)
        self.dealer.turn()
        self.dealer.compare_scores(self.player_list)

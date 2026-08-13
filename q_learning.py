import numpy
import sys
import random
from blackjack import BlackJack
from modules.player import Player

numpy.set_printoptions(threshold=sys.maxsize)
# 1 state for betting money. With 5 choices
# bet_money_state = 1
#  18 possible player values (4 (2 * 2) - 21)
possible_player_values = 18
#  20 possibe dealer values (2 - 21)
possible_dealer_values = 20
# 5 possible betting types
# num_type_of_bets = 5
number_of_states = (possible_player_values *
                    possible_dealer_values)  # * num_type_of_bets  # + bet_money_state


# When betting there are 5 options
# bet_options = 5
bet_options = 0
# When playing sometimes 3 (stand, hit , double)
# Double is sometimes not possible
playing_options = 3
number_of_actions = bet_options + playing_options


class QLearningBot():
    def __init__(self):

        self.learning_rate = 0.9  # alpha
        self.discount_factor = 0.95  # gamma
        self.exploration_rate = 1.0  # epsilon
        self.epsilon_decay = 0.9995
        self.min_epsilon = 0.01
        self.num_of_episodes = 100000
        self.max_steps = 9

        self.q_table = numpy.zeros((number_of_states, number_of_actions))

    def calc_state(self, self_value: int, dealer_value: int):
        print(self_value)
        print(type(self_value))
        return (self_value - 4) * possible_dealer_values + (dealer_value - 2)

    def choose_action(self, state, can_double_down):

        print(f'state: {state}')
        if random.uniform(0, 1) < self.exploration_rate:
            # return random action
            if can_double_down:
                return random.randint(0, 2)
            else:
                return random.randint(0, 1)
        else:
            # return best action
            return numpy.argmax(self.q_table[state, :])

    def get_reward(self, state: int, action: int, next_state: int, reward: int, done: bool):
        old_value = self.q_table[state, action]

        if done:
            target = reward
            next_max = 0.0
        else:
            next_max = numpy.max(self.q_table[next_state, :])
            target = reward + self.discount_factor * next_max

        self.q_table[state, action] = (1 - self.learning_rate) * old_value + \
            self.learning_rate * target

        self.exploration_rate = max(
            self.min_epsilon, self.exploration_rate * self.epsilon_decay)

    def train(self):
        self.env = BlackJack(0, 1, self)
        print(self.q_table)
        print_counter = 0
        for episode in range(self.num_of_episodes):
            print_counter += 1
            print('EPISODE: ', episode)
            # if print_counter == 100:
            #     print(self.q_table)
            #     print_counter = 0
            # state, _ = reset()
            state = self.env.reset()
            done = False
            # for step in range(self.max_steps):
            # action = self.choose_action(state)

            # env.step(action)
        print(self.q_table)
        numpy.save('q_table_1.csv', self.q_table)
        numpy.save('q_table_1.npy', self.q_table)


ai = QLearningBot()
ai.train()

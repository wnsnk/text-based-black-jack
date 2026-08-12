import numpy
import random
# from main import reset
from modules.player import Player

# 1 state for betting money. With 5 choices
bet_money_state = 1
#  18 possible player values (4 (2 * 2) - 21)
possible_player_values = 18
#  20 possibe dealer values (2 - 21)
possible_dealer_values = 20
# 5 possible betting types
num_type_of_bets = 5
number_of_states = (possible_player_values *
                    possible_dealer_values) * num_type_of_bets + bet_money_state
print(number_of_states)

# When betting there are 5 options
# When playing sometimes 3 (stand, hit , double)
# Double is sometimes not possible
number_of_actions = 8


class QLearningBot():
    def __init__(self):

        self.learning_rate = 0.8  # alpha
        self.discount_factor = 0.95  # gamma
        self.exploration_rate = 1.0  # epsilon
        self.epsilon_decay = 0.9995
        self.min_epsilon = 0.01
        self.num_of_episodes = 10000
        self.max_steps = 9

        self.q_table = numpy.zeros((number_of_states, number_of_actions))

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            # return random action
            pass
        else:
            # return best action
            return numpy.argmax(self.q_table[state, :])

    def train(self):
        for episode in range(self.num_of_episodes):
            # state, _ = reset()
            done = False
            for step in range(self.max_steps):
                action = self.choose_action(state)

                # env.step(action)
                next_state, reward, done, truncated, info = 0
                old_value = self.q_table[state, action]
                next_max = numpy.max(self.q_table[next_state, :])
                self.q_table[state, action] = (1 - self.learning_rate) * old_value + \
                    self.learning_rate * \
                    (reward + self.discount_factor * next_max)

                state = next_state

                if done or truncated:
                    break

            exploration_rate = max(
                self.min_epsilon, exploration_rate * self.epsilon_decay)

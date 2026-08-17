import numpy
import sys
import random
from blackjack import BlackJack
from modules.player import Player

#  18 possible player values (4 (2 * 2) - 21)
possible_player_values = 18
#  20 possibe dealer values (2 - 21)
possible_dealer_values = 20

number_of_states = (possible_player_values *
                    possible_dealer_values)


# When playing there are max 3 actions (stand, hit , double)
# Double is not always possible
number_of_actions = 3


class QLearningBot():
    def __init__(self):

        self.learning_rate = 0.9  # alpha
        self.discount_factor = 0.95  # gamma
        self.exploration_rate = 1.0  # epsilon
        self.epsilon_decay = 0.9995
        self.min_epsilon = 0.01
        self.num_of_episodes = int(
            input('HOW MANY EPISODES DO YOU WANT TO TRAIN?'))
        self.max_steps = 9

        self.q_table = numpy.zeros((number_of_states, number_of_actions))
        self.q_table = numpy.load('q_table_50000_training_BACKUP_4999.npy')
        print(self.q_table)

    def calc_state(self, self_value: int, dealer_value: int):
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
        backup_counter = 0
        for episode in range(5000, self.num_of_episodes):
            backup_counter += 1
            print(f'EPISODE: {episode}/{self.num_of_episodes}')
            if backup_counter == 5000:
                self.save_q_table(
                    f'q_table_{self.num_of_episodes}_training_BACKUP_{episode}')
                print(self.q_table)
                backup_counter = 0

            self.env.reset()

        print(self.q_table)
        self.save_q_table(
            name=f'q_table_{self.num_of_episodes}_training', episode=episode)
        print(f'TRAINING FINISHED. TOTAL EPISODES: {episode}')

    def save_q_table(self, name):
        numpy.savetxt(
            f'{name}.csv', self.q_table, delimiter=',')
        numpy.save(
            f'{name}', self.q_table)


ai = QLearningBot()
ai.train()

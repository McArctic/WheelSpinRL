import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
from wheelGame import WheelGameAI, payouts
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:


    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(2, 256, 5)  # Example adjustment
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)



    def get_state(self, game):

        state = np.array([game.balance, game.last_outcome], dtype=float)
        print('state',state)
        return state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        balance = state[0]

        final_move = [0.00,0.00,0.00,0.00,0.00]

        # Exploration v explotaion
        self.epsilon = 180 - self.n_games
        if random.randint(0,200) < self.epsilon:
            # Exploration: Randomly distribute the balance across the actions,
            # ensuring the sum does not exceed the balance.
            # This is a simple way to do it, more sophisticated distributions are possible.
            remaining_balance = balance
            for i in range(len(final_move)-1):
                final_move[i] = round(random.uniform(0, remaining_balance), 2)
                remaining_balance -= final_move[i]
            final_move[-1] = round(remaining_balance, 2)

        else:
            # Exploitation: Use model to allocate balance proportionally to the predicted values.
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
    
            # Normalize the model's predictions to sum to 1, then scale by the balance.
            normalized_prediction = torch.softmax(prediction, dim=0)
            final_move = [balance * val.item() for val in normalized_prediction]

            # Correct any small negative values that may have arisen from rounding
            final_move = [max(0, round(val, 2)) for val in final_move]
    
            # Ensure the sum of final_move does not exceed the balance due to rounding
            while sum(final_move) > balance:
                # Find the index of the maximum value in final_move
                max_index = final_move.index(max(final_move))
                # Decrease the maximum value by the smallest amount to correct the sum
                final_move[max_index] -= 0.01  # Adjust by a cent or the smallest unit of your balance
                final_move[max_index] = round(final_move[max_index], 2)  # Re-round after adjustment
    
        print('final move:', final_move)
        return final_move



def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = WheelGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        balance, last_outcome, rewards, done = game.placeBets(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, rewards, state_new, done)

        # remember
        agent.remember(state_old, final_move, rewards, state_new, done)

        
        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if balance > record:
                record = balance
                agent.model.save()

            print('Game', agent.n_games, 'Score', balance, 'Record:', record)

            plot_scores.append(balance)
            total_score += balance
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)




if __name__ == '__main__':
    train()
import torch
import random
import numpy as np
from collections import deque
from game import SnakeGame, Heading, Point
from trainer import QNet, QTrainer
from constants import MAX_MEMORY, BATCH_SIZE, LR
from plots import plot

"""
Agent is the trainer that utilizes the QNet and QTrainer class to implement a trainer
on the snake game. 
"""
class Agent:

  """
  __init__(self) initializes the Agent object by setting its parameters to default
  paramters, and intializing the QNet model and QTrainer trainer.
  """
  def __init__(self):
    self.n_games = 0
    self.epsilon = 0
    self.gamma = 0.9
    self.memory = deque(maxlen = MAX_MEMORY)
    self.model = QNet(11, 256, 3)
    self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)

  """
  get_state(self, game) returns the current game state which contains encoded
  information about the positioning of the snake, its heading, and the position
  of the food on the game screen.
  """
  def get_state(self, game):
    position = game.snake[0]
    left = Point(position.x - 20, position.y)
    right = Point(position.x + 20, position.y)
    up = Point(position.x, position.y - 20)
    down = Point(position.x, position.y + 20)

    dir_left = game.heading == Heading.LEFT
    dir_right = game.heading == Heading.RIGHT
    dir_up = game.heading == Heading.UP
    dir_down = game.heading == Heading.DOWN

    state = [(dir_left and game.check_collision(left)) or
             (dir_right and game.check_collision(right)) or
             (dir_up and game.check_collision(up)) or
             (dir_down and game.check_collision(down)),

             (dir_left and game.check_collision(up)) or
             (dir_right and game.check_collision(down)) or
             (dir_up and game.check_collision(right)) or
             (dir_down and game.check_collision(left)),

             (dir_left and game.check_collision(down)) or
             (dir_right and game.check_collision(up)) or
             (dir_up and game.check_collision(left)) or
             (dir_down and game.check_collision(right)),

             dir_left,
             dir_right,
             dir_up,
             dir_down,

             game.food.x < game.position.x,
             game.food.x > game.position.x,
             game.food.y < game.position.y,
             game.food.y > game.position.y]
    return np.array(state, dtype = int)
  
  """
  remember(self, state, action, reward, next_state, end) adds the state paramters
  obtained as arguments to the model memory of the agent.
  """
  def remember(self, state, action, reward, next_state, end):
    self.memory.append((state, action, reward, next_state, end))

  """
  train_long_memory(self) trains the trainer on the state paramters obtained from
  the long memory states.
  """
  def train_long_memory(self):
    if len(self.memory) > BATCH_SIZE:
      sample = random.sample(self.memory, BATCH_SIZE)
    else:
      sample = self.memory

    states, actions, rewards, next_states, ends = zip(*sample)
    self.trainer.train(states, actions, rewards, next_states, ends)
  
  """"
  train_short_memory(self, state, action, reward, next_state, end) trains the model
  trainer on the arguments.
  """
  def train_short_memort(self, state, action, reward, next_state, end):
    self.trainer.train(state, action, reward, next_state, end)

  """
  get_action(self, state) returns the optimal move as determined by the agent after
  applying the QTrainer and the QNet on the current game state.
  """
  def get_action(self, state):
    self.epsilon = 80 - self.n_games
    final_move = [0, 0, 0]
    if random.randint(0, 200) < self.epsilon:
      move = random.randint(0, 2)
      final_move[move] = 1
    else:
      init_state = torch.tensor(state, dtype = torch.float)
      pred = self.model(init_state)
      move = torch.argmax(pred).item()
      final_move[move] = 1

    return final_move

"""
train() initializes the game, trainer, and agent to initiate the Q-learning process.
After termination of each game, the function generates a plot by calling the function
plot() which generates a data point on the plot corresponding to the program's
performance in the current iteration.
"""
def train():
  scores = []
  mean_scores = []
  total_score = 0
  record = 0
  agent = Agent()
  game = SnakeGame()
  while True:
    old_state = agent.get_state(game)
    final_move = agent.get_action(old_state)
    reward, end, score = game.play_step(final_move)
    new_state = agent.get_state(game)
    agent.train_short_memort(old_state, final_move, reward, new_state, end)
    agent.remember(old_state, final_move, reward, new_state, end)

    if end:
      game.reset()
      agent.n_games += 1
      agent.train_long_memory()
      if score > record:
        record = score
        agent.model.save()

      print('Game', agent.n_games, 'Score', score, 'Record:', record)

      scores.append(score)
      total_score += score
      mean_score = total_score / agent.n_games
      mean_scores.append(mean_score)
      plot(scores, mean_scores)
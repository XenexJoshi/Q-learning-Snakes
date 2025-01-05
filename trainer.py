import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

"""
QNet represents the neural network used by the QLearner to determine the most effective
action for the current game state.
"""
class QNet(nn.Module):

  def __init__(self, input_size, hidden_size, output_size):
    """
    __init__(self, input_size, hidden_size, optput_size) initializes a neural network
    with input layer, hidden layer, and output layer. The input layer has input_size
    nodes, the hidden layer has hidden_size nodes, and the output layer has output_size
    nodes.
    """
    super().__init__()
    self.linear1 = nn.Linear(input_size, hidden_size)
    self.linear2 = nn.Linear(hidden_size, output_size)

  def forward(self, x):
    """
    forward(self, x) is the forward pass function for the neural network that combines
    the input layer to the hidden layer, and hidden layer to the output function using
    a linear neural network.
    """
    x = F.relu(self.linear1(x))
    x = self.linear2(x)
    return x
  
  def save(self, file_name = 'model.pth'):
    """
    save(self, filepath) saves the model data for the current version of the learned
    neural network in the argument file_name. If file_name does not exist yet, the
    function creates a file with the filepath, and then saves the current learned
    data.
    """
    model_file_path = './model'
    if not os.path.exists(model_file_path):
      os.makedirs(model_file_path)

    filename = os.path.join(model_file_path, file_name)
    torch.save(self.state_dict(), filename)


"""
QTrainer is the trainer that uses the QNet neural network, and implements the Bellman
equation to select the optimal action for the current game state, to train the
program to choose optimal moves to maximize game score.
"""
class QTrainer:

  def __init__(self, model, lr, gamma):
    """
    __init__(self, model, lr, gamma) initializes the QTrainer with the arguments as
    parameters for the trainer. The trainer uses Adam optimizer, and mean-squared loss
    as the optimization criterion.
    """
    self.model = model
    self.lr = lr
    self.gamma = gamma
    self.optimizer = optim.Adam(model.parameters(), lr = self.lr)
    self.criterion = nn.MSELoss()

  def train(self, state, action, reward, next_state, end):
    """
    train(self, state, action, reward, next_state, end) uses the Bellman equation
    to compute the optimal next_state given the current state state, and action 
    action, with the reward reward until the game states reaches end state.
    """
    state = torch.tensor(state, dtype = torch.float)
    next_state = torch.tensor(next_state, dtype = torch.float)
    action = torch.tensor(action, dtype = torch.long)
    reward = torch.tensor(reward, dtype = torch.float)

    if (len(state.shape) == 1):
      state = torch.unsqueeze(state, 0)
      next_state = torch.unsqueeze(next_state, 0)
      action = torch.unsqueeze(action, 0)
      reward = torch.unsqueeze(reward, 0)
      end = (end, )
    pred = self.model(state)

    target = pred.clone()
    for i in range(len(end)):
      Q_new = reward[i]
      if not end[i]:
        Q_new = reward[i] + self.gamma * torch.max(self.model(next_state[i]))
      target[i][torch.argmax(action[i]).item()] = Q_new

    self.optimizer.zero_grad()
    loss = self.criterion(target, pred)
    loss.backward()
    self.optimizer.step()
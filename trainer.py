import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class QNet(nn.Module):
  def __init__(self, input_size, hidden_size, output_size):
    super().__init__()
    self.linear1 = nn.Linear(input_size, hidden_size)
    self.linear2 = nn.Linear(hidden_size, output_size)

  def forward(self, x):
    x = F.relu(self.linear1(x))
    x = self.linear2(x)
    return x
  
  def save(self, file_name = 'model.pth'):
    model_file_path = './model'
    if not os.path.exists(model_file_path):
      os.makedirs(model_file_path)

    filename = os.path.join(model_file_path, file_name)
    torch.save(self.state_dict(), filename)

class QTrainer:
  def __init__(self, model, lr, gamma):
    self.model = model
    self.lr = lr
    self.gamma = gamma
    self.optimizer = optim.Adam(model.parameters(), lr = self.lr)
    self.criterion = nn.MSELoss()

  def train(self, state, action, reward, next_state, end):
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
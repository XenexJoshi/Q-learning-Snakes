import matplotlib.pyplot as plt
from IPython import display

# Initialzing matplotlib window
plt.ion()

def plot(scores, mean_val):
  """
  plot(scores, mean_val) plots the scores and mean_val on the y-axis with the game
  id(number of game) on the x-axis to depict the progression of the Q-learner with
  number of games played.
  """
  display.clear_output(wait = True)
  display.display(plt.gcf())
  plt.clf()
  plt.title("Q-learning training")
  plt.xlabel("Number of Games")
  plt.ylabel("Score")
  plt.plot(scores)
  plt.plot(mean_val)
  plt.ylim(ymin = 0)
  plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
  plt.text(len(mean_val) - 1, mean_val[-1], str(mean_val[-1]))
  plt.show(block = False)
  plt.pause(0.1)

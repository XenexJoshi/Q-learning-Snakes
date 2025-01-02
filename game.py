import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

# Initializing pygame window
pygame.init()
game_font = pygame.font.SysFont('arial', 25) #update

class Heading(Enum):
  RIGHT = 1
  LEFT = 2
  UP = 3
  DOWN = 4

Point = namedtuple('Point', 'x, y')

# update colors for game
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

# update dims
SQR_SIZE = 20 
INNER_BODY = 12 
SPEED = 80 #update based on gameplay

class SnakeGame:
  def _update_screen(self):
    self.display.fill(BLACK)
    for point in self.snake:
      pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x, point.y, 
                                                        SQR_SIZE, SQR_SIZE)) 
      pygame.draw.rect(self.display, BLUE2, pygame.Rect(point.x + 4, point.y + 4, 
                                                       INNER_BODY, INNER_BODY))  #update offset
  
    pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, 
                                                    SQR_SIZE, SQR_SIZE))
    text = game_font.render("Score: " + str(self.score), True, WHITE)
    self.display.blit(text, [0, 0])
    pygame.display.flip()


  def __init__(self, width = 640, height = 480): #set dimensions
    self.width = width
    self.height = height
    self.display = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption('Classic Snake')
    self.clock = pygame.time.Clock()
    self.reset()

  # change var name
  def reset(self): #game state
    self.heading = Heading.RIGHT
    self.position = Point(self.width / 2, self.height / 2)
    self.snake = [self.position, Point(self.head.x - SQR_SIZE, self.head.y), 
                  Point(self.head.x - (2 * SQR_SIZE), self.head.y)]
    self.score = 0
    self.food = None
    self._position_food()
    self.frame_iteration = 0

  def _position_food(self):
    x = random.randint(0, (self.width - SQR_SIZE)) * SQR_SIZE
    y = random.randint(0, (self.height - SQR_SIZE)) * SQR_SIZE
    self.food = Point(x, y)
    if self.food in self.snake:
      self._position_food()

  def check_collision(self, pos = None):
    if pos is None:
      pos = self.position
    if (pos.x > (self.width - SQR_SIZE) or (pos.x < 0)) or (pos.y > (self.height - SQR_SIZE) or (pos.y < 0)):
      return True # snake hits boundary
    if pos in self.snake[1:]:
      return True # snake hits itseld
    return False

  def play_step(self, action):
    self.frame_iteraion += 1
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    self._move(action)
    self.snake.insert(0, self.head)
    reward = 0
    game_end = False
    if self.check_collision() or self.frame_iteration > 100 * len(self.snake):
      game_end = True
      reward -= 10
    if self.head == self.head:
      self.score += 1
      reward = 10
      self._position_food()
    else:
      self.snake.pop()
    self._update_ui()
    self.clock.tick(SPEED)
    return reward, game_end, self.score

  # figure out how it works, and update it
  def _move(self, action):
    clockwise = [Heading.RIGHT, Heading.DOWN, Heading.LEFT, Heading.UP]
    index = clockwise.index(self.heading)
    if np.array_equal(action, [1, 0, 0]):
      update_heading = clockwise[index]
    elif np.array_equal(action, [0, 1, 0]):
      update_heading = clockwise[((index + 1) % 4)]
    else:
      update_heading = clockwise[((index - 1) % 4)]
    self.heading = update_heading

    x = self.position.x
    y = self.position.y
    if self.heading == Heading.LEFT:
      x -= SQR_SIZE
    elif self.heading == Heading.RIGHT:
      x += SQR_SIZE
    elif self.heading == Heading.UP:
      y -= SQR_SIZE
    elif self.heading == Heading.DOWN:
      y += SQR_SIZE

    self.position = Point(x, y)


import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
from constants import *

# Initializing pygame window
pygame.init()

# Setting the game screen font to display scores
game_font = pygame.font.SysFont('arial', 24)

"""
Heading represents the direction of the snake's current motion represented as an
enum for the four cardinal directions.
"""
class Heading(Enum):
  RIGHT = 1
  LEFT = 2
  UP = 3
  DOWN = 4


"""
Point represents a tuple that represents the position on the game screen. Point.x
represents the x-direction(horizontal) position of an object on the game board, and
Point.y represents the y-direction(vertical) position of an object on the game 
board.
"""
Point = namedtuple('Point', 'x, y')


"""
SnakeGame represents the playable game window, including the score tracker, snake
object and the food object. This object implements all the functionalities associated
with the base snake game including food placements, and the motion of the snake
on the gameboard along with rendering the game.
"""
class SnakeGame:

  """
  __init__(self, width, height) initializes the game screen based on the arguments
  width and height, and clears the game screen to initiate the game.
  """
  def __init__(self, width = 640, height = 480): 
    self.width = width
    self.height = height
    self.display = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption('Classic Snake')
    self.clock = pygame.time.Clock()
    self.reset()

  """
  reset(self) updates the game state to a new game by resetting the snake and food
  positions to the default positions on the game board. The game also clears all 
  the previous gamestates including scores and actions.
  """
  def reset(self):
    self.heading = Heading.RIGHT
    self.position = Point(self.width / 2, self.height / 2)
    self.snake = [self.position, Point(self.position.x - BLOCK, self.position.y), 
                  Point(self.position.x - (2 * BLOCK), self.position.y)]
    self.score = 0
    self.food = None
    self._position_food()
    self.frame_iteration = 0

  """ 
  _update_screen(self) updates the position of the game screen based on the current
  game state. This function draws the snake object on the screen, along with the
  food and the game score based on the current game state.
  """
  def _update_screen(self):
    self.display.fill(BLACK)
    for point in self.snake:
      pygame.draw.rect(self.display, GREEN_PRIM, 
                       pygame.Rect(point.x, point.y, 
                       BLOCK, BLOCK), border_radius = BORDER_RADIUS) 
      pygame.draw.rect(self.display, GREEN_SEC, 
                       pygame.Rect(point.x + 4, point.y + 4, 
                       INNER_BODY, INNER_BODY), border_radius = BORDER_RADIUS)  
  
    pygame.draw.circle(self.display, RED, (self.food.x, self.food.y), 
                                                    BLOCK // 2)
    text = game_font.render("Score: " + str(self.score), True, WHITE)
    self.display.blit(text, [0, 0])
    pygame.display.flip()

  """
  _position_food(self) randomly selects a valid position within the game screen 
  and sets the food at the selected location. A valid position lies within the
  game screen, and does not lie on a position already occupied by the snake object.
  """
  def _position_food(self):
    x = random.randint(0, (self.width - (2 * BLOCK)) // BLOCK) * BLOCK
    y = random.randint(0, (self.height - (2 * BLOCK)) // BLOCK) * BLOCK
    self.food = Point(x, y)
    if self.food in self.snake:
      self._position_food()

  """
  check_collision(self, pos) determines whether the current snake position represents
  a collision. A collision is defined as a game state where the head of the snake
  contacts any of the game boundaries, or and other segment of the snake's body.
  """
  def check_collision(self, pos = None):
    if pos is None:
      pos = self.position
    if (pos.x > (self.width - BLOCK) or (pos.x < 0)) or (pos.y > (self.height - BLOCK) or (pos.y < 0)):
      return True 
    if pos in self.snake[1:]:
      return True 
    return False

  """
  play_step(self, action) updates the current game state based on the past game
  state, and the argument action. This function deals with any snake heading changes
  along with any food position related event that needs to be dealt with. Additionally,
  this function also allocates rewards(both positive and negative) for the consequences
  of action.
  """
  def play_step(self, action):
    self.frame_iteration += 1
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    self._move(action)
    self.snake.insert(0, self.position)
    reward = 0
    game_end = False
    if self.check_collision() or self.frame_iteration > 100 * len(self.snake):
      game_end = True
      reward -= 10
    if self.position == self.food:
      self.score += 1
      reward = 10
      self._position_food()
    else:
      self.snake.pop()
    self._update_screen()
    self.clock.tick(SPEED)
    return reward, game_end, self.score

  """
  _move(self, action) updates the current position of the snake object based on 
  the argument action.
  """
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
      x -= BLOCK
    elif self.heading == Heading.RIGHT:
      x += BLOCK
    elif self.heading == Heading.UP:
      y -= BLOCK
    elif self.heading == Heading.DOWN:
      y += BLOCK

    self.position = Point(x, y)
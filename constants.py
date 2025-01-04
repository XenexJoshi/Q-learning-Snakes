# RGB representation of color used for rendering
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN_PRIM = (0, 255, 0)
GREEN_SEC = (120, 255, 0)
BLACK = (0, 0, 0)

# Dimension of a game block
BLOCK = 20 
# Dimension of inner snake body
INNER_BODY = 12 
# Curvature of snake's body segment
BORDER_RADIUS = 10 

# Frame rate of snake's movement 
SPEED = 80 

# Max-memory for the Q-learner agent
MAX_MEMORY = 100000
# Batch-size for the Q-learner agent
BATCH_SIZE = 1000
# Learning rate for the Q-learner agent
LR = 0.001
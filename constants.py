import itertools

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)
PURPLE = (180, 70, 200)
BROWN = (139, 69, 19)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
GHOST_WHITE = (240, 240, 255, 180)

from enum import Enum

class IngredientType(Enum):
    LETTUCE = 0
    TOMATO = 1
    BREAD = 2
    MEAT = 3
    CHEESE = 4
    WATER = 5
    SALT = 6
    
class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    WIN = 3

# Recipes for dishes
RECIPES = {
    "salad": {IngredientType.LETTUCE, IngredientType.TOMATO},
    "burger": {IngredientType.BREAD, IngredientType.MEAT, IngredientType.CHEESE},
    "soup": {IngredientType.TOMATO, IngredientType.WATER, IngredientType.SALT},
}

# Alternating cycle for footsteps
play_footstep = itertools.cycle([False, True])
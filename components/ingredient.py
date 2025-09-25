from enum import Enum
import math

import pygame
from constants import *


class IngredientType(Enum):
    VEGETABLE = 0
    MEAT = 1
    SPICE = 2

# Ingredient class
class Ingredient:
    def __init__(self, x, y, ingredient_type):
        self.x = x
        self.y = y
        self.type = ingredient_type
        self.radius = 15
        self.collected = False
        self.visible = False
        
        # Set color based on type
        if ingredient_type == IngredientType.VEGETABLE:
            self.color = GREEN
        elif ingredient_type == IngredientType.MEAT:
            self.color = RED
        else:  # SPICE
            self.color = YELLOW
            
    def draw(self, screen, player_x, player_y, vision_radius):
        if not self.collected:
            # Check if ingredient is within player's vision
            dist_to_player = math.sqrt((self.x - player_x)**2 + (self.y - player_y)**2)
            self.visible = dist_to_player <= vision_radius
            
            if self.visible:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
                pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)

import math
import pygame
from enum import Enum
from constants import *


class IngredientType(Enum):
    VEGETABLE = 0
    MEAT = 1
    SPICE = 2


class Ingredient:
    def __init__(self, x, y, ingredient_type):
        self.x = x
        self.y = y
        self.type = ingredient_type
        self.radius = 15
        self.collected = False
        self.visible = False

        # Load the correct PNG image based on type
        if ingredient_type == IngredientType.VEGETABLE:
            self.image = pygame.image.load("sprites/vegetable/tile000.png").convert_alpha()
        elif ingredient_type == IngredientType.MEAT:
            self.image = pygame.image.load("sprites/vegetable/tile001.png").convert_alpha()
        else:  # SPICE
            self.image = pygame.image.load("sprites/vegetable/tile002.png").convert_alpha()

        # Scale image to match the "radius"
        self.image = pygame.transform.scale(self.image, (self.radius * 4, self.radius * 4))

    def draw(self, screen, player_x, player_y, vision_radius):
        if not self.collected:
            # Check if ingredient is within player's vision
            dist_to_player = math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2)
            self.visible = dist_to_player <= vision_radius

            if self.visible:
                rect = self.image.get_rect(center=(int(self.x), int(self.y)))
                screen.blit(self.image, rect)

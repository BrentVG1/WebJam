import math
import pygame
from enum import Enum
from constants import *


class IngredientType(Enum):
    LETTUCE = 0
    CHEESE = 1
    TOMATO = 2
    PATTY = 3
    BUN = 4


class Ingredient:
    def __init__(self, x, y, ingredient_type, processed_by=None):
        self.x = x
        self.y = y
        self.type = ingredient_type
        self.radius = 15
        self.collected = False
        self.visible = False
        self.processed = False
        self.processed_by = processed_by

        # Load the correct PNG image based on type
        # if ingredient_type == IngredientType.VEGETABLE:
        #     self.image = pygame.image.load("sprites/vegetable/tile000.png").convert_alpha()
        # elif ingredient_type == IngredientType.MEAT:
        #     self.image = pygame.image.load("sprites/vegetable/tile001.png").convert_alpha()
        # else:  # SPICE
        if ingredient_type == IngredientType.LETTUCE:
            self.image = pygame.image.load("sprites/KropSla.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
            self.processed_image = pygame.image.load("sprites/GesnedenSla.png").convert_alpha()
            self.processed_image = pygame.transform.scale(self.image, (self.radius, self.radius))
        elif ingredient_type == IngredientType.CHEESE:
            self.image = pygame.image.load("sprites/CheddarKaas.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
        elif ingredient_type == IngredientType.TOMATO:
            self.image = pygame.image.load("sprites/Tomaat.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
            self.processed_image = pygame.image.load("sprites/GesnedenTomaten-1.png").convert_alpha()
            self.processed_image = pygame.transform.scale(self.image, (self.radius, self.radius))
        elif ingredient_type == IngredientType.PATTY:
            self.image = pygame.image.load("sprites/Patty.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
            self.processed_image = pygame.image.load("sprites/gebakkenPatty.png").convert_alpha()
            self.processed_image = pygame.transform.scale(self.image, (self.radius, self.radius))
        elif ingredient_type == IngredientType.BUN:
            self.image = pygame.image.load("sprites/Buns.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.radius, self.radius))
        else:
            raise ValueError(f"Unknown ingredient type: {ingredient_type}")

        # Scale image to match the "radius"
        self.image = pygame.transform.scale(self.image, (self.radius * 4, self.radius * 4))

    def draw(self, screen, player_x, player_y, vision_radius, debug=False):
        if not self.collected:
            if debug:
                self.visible = True
            else:
                # Check if ingredient is within player's vision
                dist_to_player = math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2)
                self.visible = dist_to_player <= vision_radius

            if self.visible:
                rect = self.image.get_rect(center=(int(self.x), int(self.y)))
                screen.blit(self.image, rect)


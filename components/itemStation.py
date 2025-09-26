import math
import pygame
from components.collisionObject import CollisionObject
from constants import *


class ItemStation(CollisionObject):
    def __init__(self, x, y, width, height, ingredient):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.progress = 0
        self.active = False
        self.ingredients = []
        self.visible = False
        self.ingredient = ingredient
        super().__init__(x, y, width, height)
        
    def draw(self, screen, player_x, player_y, vision_radius):
       
        
        # Draw station background
        color = GREEN
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, LIGHT_GRAY, (self.x, self.y, self.width, self.height), 2)
        
        # Draw station label
        font = pygame.font.SysFont(None, 30)
        text = font.render(self.ingredient.type.name.capitalize(), True, WHITE)
        screen.blit(text, (self.x + 10, self.y + 10))
        
        # Draw progress if active
        if self.active and self.progress > 0:
            pygame.draw.rect(screen, GREEN, (self.x, self.y + self.height - 10, self.width * (self.progress / 100), 10))
        
        self.ingredient.draw(screen, player_x, player_y, vision_radius)

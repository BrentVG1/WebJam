import math
import pygame
from components.collisionObject import CollisionObject
from constants import *


class CookingStation(CollisionObject):
    def __init__(self, x, y, width, height, station_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = station_type  # "chopping", "cooking", "serving"
        self.progress = 0
        self.active = False
        self.visible = False
        self.texture = None
        if self.type == "chopping":
            self.texture = pygame.image.load("sprites/Snijplank.png").convert_alpha()
            self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        elif self.type == "cooking":
            self.texture = pygame.image.load("sprites/grillpraat.png").convert_alpha()
            self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
            
        elif self.type == "serving":
            self.texture = pygame.image.load("sprites/Toog.png").convert_alpha()
            self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
            
        # elif self.type == "baking":
        #     self.texture = pygame.image.load("sprites/baking_station.png").convert_alpha()
        super().__init__(x, y, width, height)
        
    def draw(self, screen):
        
        if self.texture:
            screen.blit(self.texture, (self.x, self.y))
            
        else:
       
        
            # Draw station background
            color = BROWN if self.type == "chopping" else (100, 100, 100) if self.type == "cooking" else PURPLE
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, LIGHT_GRAY, (self.x, self.y, self.width, self.height), 2)
            
            # Draw station label
            font = pygame.font.SysFont(None, 30)
            text = font.render(self.type.capitalize(), True, WHITE)
            screen.blit(text, (self.x + 10, self.y + 10))
        
        # Draw progress if active
        if self.active and self.progress > 0:
            pygame.draw.rect(screen, GREEN, (self.x, self.y + self.height - 10, self.width * (self.progress / 100), 10))

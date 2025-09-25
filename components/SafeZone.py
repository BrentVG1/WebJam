
import pygame
from constants import *


class SafeZone:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        
    def in_zone(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
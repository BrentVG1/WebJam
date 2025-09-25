
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
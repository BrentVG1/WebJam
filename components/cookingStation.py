import math
import pygame
from constants import *


class CookingStation:
    def __init__(self, x, y, width, height, station_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = station_type  # "chopping", "cooking", "serving"
        self.progress = 0
        self.active = False
        self.ingredients = []
        self.visible = False
        
    def draw(self, screen, player_x, player_y, vision_radius):
        # Check if station is within player's vision
        dist_to_player = math.sqrt((self.x + self.width/2 - player_x)**2 + 
                                 (self.y + self.height/2 - player_y)**2)
        self.visible = dist_to_player <= vision_radius + max(self.width, self.height)
        
        if self.visible:
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

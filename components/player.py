import random

import pygame

from components.footprint import Footprint

from constants import *



class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.radius = 20
        self.color = BLUE
        self.footprint_timer = 0
        self.footprint_interval = 10  # frames between footprints
        self.carrying = []  # List of carried ingredients
        
    def update(self, keys):
        # Movement
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            
        # Keep player on screen
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
        
        # Update footprint timer
        self.footprint_timer += 1
        
    def create_footprint(self):
        # Calculate brightness based on movement speed (simplified)
        brightness = 0.7 + random.uniform(0, 0.3)
        return Footprint(self.x, self.y, brightness)
        
    def draw(self, screen):
        # Draw player
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)
        
        # Draw carried ingredients
        for i, ingredient in enumerate(self.carrying):
            offset_x = (i - (len(self.carrying) - 1) / 2) * 10
            pygame.draw.circle(screen, ingredient.color, (int(self.x + offset_x), int(self.y - 25)), 8)

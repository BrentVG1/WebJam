

import pygame
import constants


class CollisionObject:
    def __init__(self, x, y, width, height, color=constants.RED):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.obj_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def collides_with(self, rect):
        return self.obj_rect.colliderect(rect)
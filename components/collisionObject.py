

import math
import pygame
import constants


class CollisionObject:
    def __init__(self, x, y, width, height, color=constants.GRAY):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.obj_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.img = None        
        
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def collides_with(self, rect):
        return self.obj_rect.colliderect(rect)
    
    def distance_to_rect(self, player_pos):
        px, py = player_pos
        
        # Clamp point to the rectangle bounds
        closest_x = max(self.obj_rect.left, min(px, self.obj_rect.right))
        closest_y = max(self.obj_rect.top, min(py, self.obj_rect.bottom))
        
        dx = px - closest_x
        dy = py - closest_y
        
        return math.hypot(dx, dy)
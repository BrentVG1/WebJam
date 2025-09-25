import math

import pygame


class Footprint:
    def __init__(self, x, y, brightness=1.0):
        self.x = x
        self.y = y
        self.brightness = brightness
        self.max_brightness = brightness
        self.fade_speed = 0.01  # How fast footprints fade
        self.radius = 10
        self.visible = True
        
    def update(self):
        self.brightness -= self.fade_speed
        return self.brightness > 0
        
    def draw(self, screen, player_x, player_y, vision_radius):
        # Check if footprint is within player's vision
        dist_to_player = math.sqrt((self.x - player_x)**2 + (self.y - player_y)**2)
        self.visible = dist_to_player <= vision_radius
        
        if self.brightness > 0 and self.visible:
            alpha = int(255 * self.brightness)
            color = (255, 255, 200, alpha)
            
            # Create a surface for the glowing effect
            glow_surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, color, (self.radius * 2, self.radius * 2), self.radius)
            
            # Draw the footprint
            screen.blit(glow_surface, (self.x - self.radius * 2, self.y - self.radius * 2), 
                       special_flags=pygame.BLEND_ALPHA_SDL2)

import pygame
import math

class FogOfWar:
    def __init__(self, screen_width, screen_height, vision_radius):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.vision_radius = vision_radius
        
    def draw(self, screen, player_x, player_y):
        # Create a black surface with a hole for the player's vision
        fog_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        fog_surface.fill((0, 0, 0, 255))  # Opaque black
        
        # Cut a hole for the vision area
        vision_surface = pygame.Surface((self.vision_radius * 2, self.vision_radius * 2), pygame.SRCALPHA)
        vision_surface.fill((0, 0, 0, 0))  # Transparent
        
        
        center = (self.vision_radius, self.vision_radius)
        for radius in range(self.vision_radius, 0, -1):
            if radius > self.vision_radius // 2:
                # fade from clear (0) at half radius to opaque (255) at edge
                fade_ratio = (radius - self.vision_radius // 2) / (self.vision_radius / 2)
                alpha = int(255 * fade_ratio)
            else:
                alpha = 0  # fully clear in the inner half
            color = (0, 0, 0, alpha)
            pygame.draw.circle(vision_surface, color, center, radius)

        
        # Apply the vision hole to the fog
        fog_surface.blit(vision_surface, 
                        (player_x - self.vision_radius, player_y - self.vision_radius),
                        special_flags=pygame.BLEND_RGBA_MIN)
        
        pygame.draw.circle(fog_surface, (0, 0, 0), (int(player_x), int(player_y)), self.vision_radius * 1.5, width=self.vision_radius // 2 + 1)
        
        # Draw the fog on top of everything
        screen.blit(fog_surface, (0, 0))
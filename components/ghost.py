from enum import Enum
import math
import random
import pygame

from constants import *


class GhostType(Enum):
    FOLLOWER = 0
    PATROLLER = 1


class Ghost:
    def __init__(self, x, y, ghost_type=GhostType.FOLLOWER, safe_zone_height=250):
        self.x = x
        self.y = y
        self.current_type = ghost_type   # Current type (can change dynamically)
        self.speed = random.uniform(0.5, 1.5)
        self.target_x = x
        self.target_y = y
        self.radius = 25
        self.detection_range = 200
        self.patrol_points = []
        self.current_patrol_index = 0
        self.visible = False
        self.safe_zone_height = safe_zone_height
        
        self.setup_patrol_points()
    
    def setup_patrol_points(self):
        # Create random patrol points around the kitchen (avoid safe zone)
        for _ in range(4):
            self.patrol_points.append((
                random.randint(100, SCREEN_WIDTH - 100),
                random.randint(100, SCREEN_HEIGHT - self.safe_zone_height - 100)
            ))
    
    def update(self, player, footprints, player_in_safe_zone):
        # Dynamic type switching: Followers become patrollers when player is in safe zone
        
        # Behavior based on current type
        if self.current_type == GhostType.PATROLLER or player_in_safe_zone:
            # Patrol behavior
            target = self.patrol_points[self.current_patrol_index]
            self.target_x, self.target_y = target
            
            # Check if reached patrol point
            if math.sqrt((self.x - target[0])**2 + (self.y - target[1])**2) < 20:
                self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
                
        elif self.current_type == GhostType.FOLLOWER:
            # Hunting/following behavior
            # Find the brightest footprint in range
            brightest_footprint = None
            max_brightness = 0
            
            for footprint in footprints:
                dist = math.sqrt((self.x - footprint.x)**2 + (self.y - footprint.y)**2)
                if dist < self.detection_range and footprint.brightness > max_brightness:
                    max_brightness = footprint.brightness
                    brightest_footprint = footprint
            
            if brightest_footprint:
                self.target_x = brightest_footprint.x
                self.target_y = brightest_footprint.y
            else:
                # If no footprints, follow player directly
                self.target_x = player.x
                self.target_y = player.y
        
        # Move towards target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = max(0.1, math.sqrt(dx*dx + dy*dy))
        
        # Calculate new position
        new_x = self.x + (dx / dist) * self.speed
        new_y = self.y + (dy / dist) * self.speed
        
        # Apply boundary constraints (ghosts can't enter safe zone)
        new_x = max(self.radius, min(SCREEN_WIDTH - self.radius, new_x))
        new_y = max(self.radius, min(SCREEN_HEIGHT - self.safe_zone_height - self.radius, new_y))
        
        # Update ghost position
        self.x = new_x
        self.y = new_y
        
    def draw(self, screen):
        # Determine color based on current type
        if self.current_type == GhostType.FOLLOWER:
            ghost_color = (255, 100, 100, 180)  # Red when following/hunting
        else:
            ghost_color = (200, 230, 255, 180)  # Normal color when patrolling
        
     
        # Create a surface for the ghost with alpha
        ghost_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(ghost_surface, ghost_color, (self.radius, self.radius), self.radius)
        
        # Draw wavy bottom for ghost effect
        points = []
        for i in range(5):
            angle = i * (math.pi / 2)
            x = self.radius + math.cos(angle) * self.radius * 0.8
            y = self.radius + math.sin(angle) * self.radius * 0.8
            points.append((x, y))
        
        pygame.draw.polygon(ghost_surface, ghost_color, points)
        
        # Draw eyes
        eye_radius = 5
        left_eye_pos = (self.radius - 7, self.radius - 5)
        right_eye_pos = (self.radius + 7, self.radius - 5)
        pygame.draw.circle(ghost_surface, (30, 30, 60), left_eye_pos, eye_radius)
        pygame.draw.circle(ghost_surface, (30, 30, 60), right_eye_pos, eye_radius)
        
        # Blit the ghost surface to the screen
        screen.blit(ghost_surface, (self.x - self.radius, self.y - self.radius))
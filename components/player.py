# components/player.py
import math
import pygame
from constants import *
import random
from components.footprint import Footprint

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.radius = 20
        self.color = BLUE
        self.footprint_timer = 0
        self.footprint_interval = 10
        self.carrying = None  # single carry slot

    # ---------- carry helpers ----------
    def has_item(self):
        return self.carrying is not None

    def pick_up(self, ingredient):
        """Pick up an ingredient if hands are free."""
        if not self.has_item():
            self.carrying = ingredient
            ingredient.collected = True
            return True
        return False

    def consume(self):
        """Use/serve the carried item (clear slot)."""
        self.carrying = None

    def drop(self):
        """Drop carried item at current position."""
        if self.has_item():
            item = self.carrying
            self.carrying = None
            item.collected = False
            item.x, item.y = self.x, self.y
            return item
        return None

    def create_footprint(self):
        """Create a Footprint at the player's current position with slight brightness variance."""
        brightness = 0.7 + random.uniform(0.0, 0.3)
        return Footprint(self.x, self.y, brightness)

    # ---------- NEW: moved from main ----------
    def try_auto_pickup_nearby(self, ingredients):
        """
        Auto-pick up a nearby ingredient if overlapping and hands are free.
        Returns the picked ingredient or None.
        """
        if self.has_item():
            return None

        for ing in ingredients:
            if not ing.collected:
                dist = math.hypot(ing.x - self.x, ing.y - self.y)
                if dist < ing.radius + self.radius:
                    if self.pick_up(ing):
                        return ing
        return None

    # ---------- existing methods ----------
    def update(self, keys, rects):
        # Store original position for collision recovery
        original_x, original_y = self.x, self.y
        
        # Movement
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Screen boundary check
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
        
        # Collision detection with rectangles
        player_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                                self.radius * 2, self.radius * 2)
        
        for rect in rects:
            if player_rect.colliderect(rect):
                self._resolve_collision(rect, original_x, original_y)
                break  # Only resolve one collision per frame
        
        self.footprint_timer += 1

    def _resolve_collision(self, obstacle_rect, original_x, original_y):
        """Resolve collision by moving player to the edge of the obstacle"""
        player_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                                self.radius * 2, self.radius * 2)
        
        # Calculate overlap on each side
        left_overlap = player_rect.right - obstacle_rect.left
        right_overlap = obstacle_rect.right - player_rect.left
        top_overlap = player_rect.bottom - obstacle_rect.top
        bottom_overlap = obstacle_rect.bottom - player_rect.top
        
        # Find the smallest overlap (the side we hit)
        min_overlap = min(left_overlap, right_overlap, top_overlap, bottom_overlap)
        
        # Move player to the edge based on which side we collided with
        if min_overlap == left_overlap:
            # Hit left side of obstacle
            self.x = obstacle_rect.left - self.radius
        elif min_overlap == right_overlap:
            # Hit right side of obstacle
            self.x = obstacle_rect.right + self.radius
        elif min_overlap == top_overlap:
            # Hit top side of obstacle
            self.y = obstacle_rect.top - self.radius
        elif min_overlap == bottom_overlap:
            # Hit bottom side of obstacle
            self.y = obstacle_rect.bottom + self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)

        if self.carrying:
            img = pygame.transform.scale(self.carrying.image, (64, 64))
            rect = img.get_rect(center=(int(self.x), int(self.y - 25)))
            screen.blit(img, rect)

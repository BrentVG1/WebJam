# components/player.py
import math
import pygame
import random
from constants import *
from components.footprint import Footprint
import os

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.radius = 20
        self.direction = "down"
        self.footprint_timer = 0
        self.footprint_interval = 10
        self.carrying = None

        # animatie helpers
        self.walk_cycle = 0
        self.walk_speed = 0.2

        # --- Load sprites ---
        self.sprites = {}
        self.sprites["down"] = pygame.image.load(os.path.join("sprites", "rat_chef.png")).convert_alpha()
        self.sprites["down"] = pygame.transform.scale(self.sprites["down"], (self.radius * 2.5, self.radius * 2.5))
        self.sprites["up"] = pygame.image.load(os.path.join("sprites", "rat_chef_back-1.png")).convert_alpha()
        self.sprites["left"] = pygame.image.load(os.path.join("sprites", "rat_chef_left.png")).convert_alpha()
        self.sprites["right"] = pygame.image.load(os.path.join("sprites", "rat_chef_right.png")).convert_alpha()
        self.sprites["up"] = pygame.transform.scale(self.sprites["up"], (self.radius * 2.5, self.radius * 2.5))
        self.sprites["left"] = pygame.transform.scale(self.sprites["left"], (self.radius * 2.5, self.radius * 2.5))
        self.sprites["right"] = pygame.transform.scale(self.sprites["right"], (self.radius * 2.5, self.radius * 2.5))
        
        # You can later add "left" and "right" if needed

    # ---------- carry helpers ----------
    def has_item(self):
        return self.carrying is not None

    def pick_up(self, ingredient):
        if not self.has_item():
            self.carrying = ingredient
            ingredient.collected = True
            return True
        return False

    def consume(self):
        self.carrying = None

    def drop(self):
        if self.has_item():
            item = self.carrying
            self.carrying = None
            item.collected = False
            item.x, item.y = self.x, self.y
            return item
        return None

    def create_footprint(self):
        brightness = 0.7 + random.uniform(0.0, 0.3)
        return Footprint(self.x, self.y, brightness)

    def try_auto_pickup_nearby(self, ingredients):
        if self.has_item():
            return None
        for ing in ingredients:
            if not ing.collected:
                dist = math.hypot(ing.x - self.x, ing.y - self.y)
                if dist < ing.radius + self.radius:
                    if self.pick_up(ing):
                        return ing
        return None

    # ---------- movement / collision ----------
        # ---------- movement / collision ----------
    def update(self, keys, rects, dt):
        original_x, original_y = self.x, self.y
        moved = False

        # base speed (pixels per second)
        move_speed = self.speed * dt  

        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.y -= move_speed
            self.direction = "up"
            moved = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += move_speed
            self.direction = "down"
            moved = True
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.x -= move_speed
            self.direction = "left"
            moved = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += move_speed
            self.direction = "right"
            moved = True
            
        if keys[pygame.K_LSHIFT]:
            self.speed = 2
        else:
            self.speed = 5

        # animatie cycle updaten
        if moved:
            self.walk_cycle += self.walk_speed * dt
        else:
            self.walk_cycle = 0

        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))

        player_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                  self.radius * 2, self.radius * 2)

        for rect in rects:
            if player_rect.colliderect(rect):
                self._resolve_collision(rect, original_x, original_y)
                break

        self.footprint_timer += dt


    def _resolve_collision(self, obstacle_rect, original_x, original_y):
        self.x, self.y = original_x, original_y

    # ---------- tekenen ----------
    def draw(self, screen):
        # Draw the sprite instead of shapes
        if self.direction in ["up", "down", "left", "right"]:
            sprite = self.sprites[self.direction]
        else:
            # fallback
            sprite = self.sprites["down"]

        # Scale sprite bigger (e.g., 2x)
        scale_factor = 2
        sprite_scaled = pygame.transform.scale(sprite, (sprite.get_width() * scale_factor, sprite.get_height() * scale_factor))

        offset_y = -25  # adjust this number as needed
        sprite_rect = sprite_scaled.get_rect(center=(int(self.x), int(self.y + offset_y)))
        screen.blit(sprite_scaled, sprite_rect)


        # Draw carried item spinning above head
        if self.carrying:
            if self.carrying.processed:
                img_s = self.carrying.processed_image
            else:
                img_s = self.carrying.image
            img = pygame.transform.scale(img_s, (40, 40))
            angle = (pygame.time.get_ticks() // 5) % 360
            img = pygame.transform.rotate(img, angle)
            rect = img.get_rect(center=(int(self.x), int(self.y + -25 - self.radius*2)))
            screen.blit(img, rect)

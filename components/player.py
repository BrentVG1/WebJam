# components/player.py
import math
import pygame
import random
from constants import *
from components.footprint import Footprint

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.radius = 20
        self.direction = "down"   # default kijkrichting
        self.color = BLUE
        self.footprint_timer = 0
        self.footprint_interval = 10
        self.carrying = None

        # animatie helpers
        self.walk_cycle = 0
        self.walk_speed = 0.2

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
    def update(self, keys, rects):
        original_x, original_y = self.x, self.y
        moved = False

        if keys[pygame.K_z] or keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = "up"
            moved = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = "down"
            moved = True
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = "left"
            moved = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = "right"
            moved = True

        # animatie cycle updaten
        if moved:
            self.walk_cycle += self.walk_speed
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

        self.footprint_timer += 1

    def _resolve_collision(self, obstacle_rect, original_x, original_y):
        self.x, self.y = original_x, original_y

    # ---------- tekenen ----------
    def draw(self, screen):
        # Schaduw
        shadow_rect = pygame.Rect(self.x - self.radius, self.y + self.radius - 5,
                                  self.radius * 2, 10)
        pygame.draw.ellipse(screen, (40, 40, 40), shadow_rect)

        # Regenboog aura
        for i in range(6):
            color = pygame.Color(0)
            color.hsva = ((pygame.time.get_ticks() // 10 + i*60) % 360, 90, 100, 100)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius + 10 - i*2, 2)

        # Lichaam
        body_color = self.color
        body_rect = pygame.Rect(self.x - self.radius//2, self.y - self.radius, self.radius, self.radius*2)
        pygame.draw.ellipse(screen, body_color, body_rect)

        # Groot hoofd
        head_radius = int(self.radius * 1.3)
        head_center = (int(self.x), int(self.y - self.radius))
        pygame.draw.circle(screen, (240, 220, 180), head_center, head_radius)

        # Ogen (kijken richting)
        eye_offset = 6
        if self.direction == "left":
            dx, dy = -eye_offset, 0
        elif self.direction == "right":
            dx, dy = eye_offset, 0
        elif self.direction == "up":
            dx, dy = 0, -eye_offset
        else:  # down
            dx, dy = 0, eye_offset

        pygame.draw.circle(screen, (255, 255, 255), (head_center[0] - 8, head_center[1] - 5), 8)
        pygame.draw.circle(screen, (255, 255, 255), (head_center[0] + 8, head_center[1] - 5), 8)
        pygame.draw.circle(screen, (0, 0, 0), (head_center[0] - 8 + dx//2, head_center[1] - 5 + dy//2), 4)
        pygame.draw.circle(screen, (0, 0, 0), (head_center[0] + 8 + dx//2, head_center[1] - 5 + dy//2), 4)

        # Mond (tong bij lopen)
        if abs(math.sin(self.walk_cycle)) > 0.5:
            pygame.draw.rect(screen, (255, 0, 0),
                             (head_center[0] - 5, head_center[1] + 10, 10, 8))  # tong
        else:
            pygame.draw.arc(screen, (0, 0, 0),
                            (head_center[0] - 10, head_center[1] + 5, 20, 10),
                            math.pi, 2*math.pi, 2)  # smile

        # Armen zwaaien
        offset = int(math.sin(self.walk_cycle * 2) * 12)
        pygame.draw.line(screen, body_color, (self.x - self.radius//2, self.y),
                         (self.x - self.radius - 10, self.y + offset), 6)
        pygame.draw.line(screen, body_color, (self.x + self.radius//2, self.y),
                         (self.x + self.radius + 10, self.y - offset), 6)

        # Benen overdreven
        pygame.draw.line(screen, body_color, (self.x - 5, self.y + self.radius//2),
                         (self.x - 15, self.y + self.radius*2 + offset), 8)
        pygame.draw.line(screen, body_color, (self.x + 5, self.y + self.radius//2),
                         (self.x + 15, self.y + self.radius*2 - offset), 8)

        # Item boven hoofd (draait)
        if self.carrying:
            img = pygame.transform.scale(self.carrying.image, (40, 40))
            angle = (pygame.time.get_ticks() // 5) % 360
            img = pygame.transform.rotate(img, angle)
            rect = img.get_rect(center=(int(self.x), int(self.y - self.radius*3)))
            screen.blit(img, rect)

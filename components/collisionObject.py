import math
import pygame
import constants
import os


class CollisionObject:
    def __init__(self, x, y, width, height, color=constants.GRAY, texture_path=None, tile=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.obj_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.img = None
        self.tile = tile  # choose between tiling or stretching

        if texture_path:
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                tex_path = os.path.join(base_dir, "..", "sprites", texture_path)  
                self.img = pygame.image.load(tex_path).convert()
                print(f"[CollisionObject] Loaded texture: {tex_path}")
            except Exception as e:
                print(f"[CollisionObject] Failed to load texture {texture_path}: {e}")
                self.img = None

    def draw(self, screen):
        if self.img:
            if self.tile:
                tex_w, tex_h = self.img.get_size()
                for y in range(self.y, self.y + self.height, tex_h):
                    for x in range(self.x, self.x + self.width, tex_w):
                        screen.blit(self.img, (x, y))
            else:
                stretched = pygame.transform.scale(self.img, (self.width, self.height))
                screen.blit(stretched, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collides_with(self, rect):
        return self.obj_rect.colliderect(rect)

    def distance_to_rect(self, player_pos):
        px, py = player_pos
        closest_x = max(self.obj_rect.left, min(px, self.obj_rect.right))
        closest_y = max(self.obj_rect.top, min(py, self.obj_rect.bottom))
        dx = px - closest_x
        dy = py - closest_y
        return math.hypot(dx, dy)

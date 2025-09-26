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
                x0, y0 = self.x, self.y
                x1, y1 = self.x + self.width, self.y + self.height

                for y in range(y0, y1, tex_h):
                    for x in range(x0, x1, tex_w):
                        w = min(tex_w, x1 - x)
                        h = min(tex_h, y1 - y)
                        if w > 0 and h > 0:
                            area = pygame.Rect(0, 0, w, h)
                            screen.blit(self.img, (x, y), area=area)
            else:
                stretched = pygame.transform.scale(self.img, (self.width, self.height))
                screen.blit(stretched, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # --- Border around the object ---
        border_color = (60, 40, 20)   # dark brown (you can change)
        border_thickness = 5          # pixels
        pygame.draw.rect(
            screen,
            border_color,
            (self.x, self.y, self.width, self.height),
            border_thickness
        )



    def collides_with(self, rect):
        return self.obj_rect.colliderect(rect)

    def distance_to_rect(self, player_pos):
        px, py = player_pos
        closest_x = max(self.obj_rect.left, min(px, self.obj_rect.right))
        closest_y = max(self.obj_rect.top, min(py, self.obj_rect.bottom))
        dx = px - closest_x
        dy = py - closest_y
        return math.hypot(dx, dy)

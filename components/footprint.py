import math
import pygame

class Footprint:
    foot_toggle = True  # Wisselt tussen links en rechts

    def __init__(self, x, y, player_dx=1, player_dy=0, scale=0.5, brightness=1.0):
        self.x = x
        self.y = y
        self.scale = scale
        self.brightness = brightness
        self.fade_speed = 0.01
        self.visible = True
        self.radius = 20  # voorkomt crash in main

        # Links of rechts voet
        self.is_left = Footprint.foot_toggle
        Footprint.foot_toggle = not Footprint.foot_toggle

        # Bereken rotatie op basis van beweging speler
        angle = math.degrees(math.atan2(-player_dy, player_dx))
        offset = -15 if self.is_left else 15
        self.rotation = angle + offset

        # Kleur van de voetafdruk (bruin)
        self.color = (139, 69, 19)

    def update(self):
        self.brightness -= self.fade_speed
        return self.brightness > 0

    def draw(self, screen, player_x, player_y, vision_radius):
        # Alleen tekenen als binnen zicht
        dist = math.hypot(self.x - player_x, self.y - player_y)
        self.visible = dist <= vision_radius
        if not self.visible or self.brightness <= 0:
            return

        alpha = int(255 * self.brightness)
        color = (*self.color, alpha)

        # Surface voor voetafdruk
        w = int(20 * self.scale)
        h = int(40 * self.scale)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)

        # Polygon teen + middenvoet
        points = [
            (w*0.3, h*0.2),
            (w*0.7, h*0.2),
            (w*0.8, h*0.6),
            (w*0.2, h*0.6)
        ]
        pygame.draw.polygon(surf, color, points)

        # Hiel
        pygame.draw.ellipse(surf, color, (w*0.2, h*0.55, w*0.6, h*0.35))

        # Rotatie gebaseerd op beweging speler
        surf = pygame.transform.rotate(surf, self.rotation)

        # Teken op scherm
        screen.blit(surf, (self.x - surf.get_width()//2, self.y - surf.get_height()//2))

from enum import Enum
import math
import random
import pygame
import os

from constants import *


class GhostType(Enum):
    FOLLOWER = 0
    PATROLLER = 1


class Ghost:
    def __init__(self, x, y, ghost_type=GhostType.FOLLOWER, safe_zone_height=250):
        self.x = x
        self.y = y
        self.current_type = ghost_type  # Current type (can change dynamically)
        self.speed = random.uniform(0.5, 1.5)
        self.target_x = x
        self.target_y = y
        self.radius = 25
        self.detection_range = 200
        self.patrol_points = []
        self.current_patrol_index = 0
        self.visible = False
        self.safe_zone_height = safe_zone_height
        self.dont_know_where_to_go = False

        self.setup_patrol_points()
        self.load_images()

    def setup_patrol_points(self):
        # Create random patrol points around the kitchen (avoid safe zone)
        for _ in range(4):
            self.patrol_points.append((
                random.randint(100, SCREEN_WIDTH - 100),
                random.randint(100, SCREEN_HEIGHT - self.safe_zone_height - 100)
            ))

    def load_images(self):
        # Laad alle spookafbeeldingen uit de folder images/ghosts/
        ghost_folder = os.path.join(os.path.dirname(__file__), "images", "ghosts")

        self.images = [
            pygame.image.load(os.path.join(ghost_folder, f)).convert_alpha()
            for f in os.listdir(ghost_folder)
            if f.endswith((".png", ".jpg"))
        ]
        # Kies een random afbeelding bij spawn
        self.set_random_image()

    def set_random_image(self):
        if self.images:
            self.image = random.choice(self.images)
            self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        else:
            self.image = None  # fallback als er geen afbeeldingen zijn

    def update(self, last_known_location, footprints, player_in_safe_zone):
        if self.dont_know_where_to_go and len(footprints) != 0:
            self.dont_know_where_to_go = False

        if self.current_type == GhostType.PATROLLER or player_in_safe_zone or self.dont_know_where_to_go or last_known_location is None:
            # Patrol behavior
            target = self.patrol_points[self.current_patrol_index]
            self.target_x, self.target_y = target
            if math.sqrt((self.x - target[0]) ** 2 + (self.y - target[1]) ** 2) < 20:
                self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
        elif self.current_type == GhostType.FOLLOWER:
            # Hunting/following behavior
            brightest_footprint = None
            max_brightness = 0
            for footprint in footprints:
                dist = math.sqrt((self.x - footprint.x) ** 2 + (self.y - footprint.y) ** 2)
                if dist < self.detection_range and footprint.brightness > max_brightness:
                    max_brightness = footprint.brightness
                    brightest_footprint = footprint
            if brightest_footprint:
                self.target_x = brightest_footprint.x
                self.target_y = brightest_footprint.y
            else:
                self.target_x = last_known_location[0]
                self.target_y = last_known_location[1]
                if abs(self.target_x - self.x) < 5 and abs(self.target_y - self.y) < 5:
                    self.dont_know_where_to_go = True

        # Move towards target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = max(0.1, math.sqrt(dx * dx + dy * dy))
        new_x = self.x + (dx / dist) * self.speed
        new_y = self.y + (dy / dist) * self.speed

        # Boundary constraints
        new_x = max(self.radius, min(SCREEN_WIDTH - self.radius, new_x))
        new_y = max(self.radius, min(SCREEN_HEIGHT - self.safe_zone_height - self.radius, new_y))
        self.x = new_x
        self.y = new_y

    def draw(self, screen):
        size = self.radius * 2
        ghost_surface = pygame.Surface((size, size), pygame.SRCALPHA)

        # --- Kies kleur op basis van spooktype ---
        if self.current_type == GhostType.FOLLOWER:
            body_color = (255, 80, 80, 220)  # roodachtig voor achtervolgers
        else:
            body_color = (240, 240, 240, 200)  # wit / lichtgrijs voor patrollers

        # --- Hoofd: nette ellipse ---
        head_width = self.radius * 2
        head_height = int(self.radius * 1.5)
        pygame.draw.ellipse(ghost_surface, body_color, (0, 0, head_width, head_height))

        # --- Lichaam met vloeiende golvende onderkant ---
        wave_count = 5
        wave_width = size / wave_count
        points = [(0, head_height)]
        for i in range(wave_count + 1):
            x = i * wave_width
            y = size - self.radius // 6 * (-1) ** i  # zachte golven
            points.append((x, y))
        points.append((size, head_height))
        pygame.draw.polygon(ghost_surface, body_color, points)

        # --- Twee nette ogen ---
        eye_radius = self.radius // 4
        eye_y = head_height // 2
        eye_x_offset = self.radius // 2
        # linker oog
        pygame.draw.circle(ghost_surface, (0, 0, 0), (eye_x_offset, eye_y), eye_radius)
        pygame.draw.circle(ghost_surface, (255, 255, 255), (eye_x_offset + eye_radius // 3, eye_y - eye_radius // 3),
                           eye_radius // 2)
        # rechter oog
        pygame.draw.circle(ghost_surface, (0, 0, 0), (size - eye_x_offset, eye_y), eye_radius)
        pygame.draw.circle(ghost_surface, (255, 255, 255),
                           (size - eye_x_offset - eye_radius // 3, eye_y - eye_radius // 3), eye_radius // 2)

        # --- Subtiele extra details (optioneel) ---
        for _ in range(random.randint(1, 2)):
            dot_x = random.randint(self.radius // 2, size - self.radius // 2)
            dot_y = random.randint(head_height, size)
            dot_radius = random.randint(2, 4)
            pygame.draw.circle(ghost_surface, (255, 150, 200), (dot_x, dot_y), dot_radius)

        # --- Blit naar scherm ---
        screen.blit(ghost_surface, (self.x - self.radius, self.y - self.radius))

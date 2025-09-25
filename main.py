import pygame
import random
import math
import sys
import constants  # <-- explicit import

<<<<<<< HEAD
=======
from components.cookingStation import CookingStation
from components.fogOfWar import FogOfWar
from components.ghost import Ghost, GhostType
from components.ingredient import Ingredient, IngredientType
from components.player import Player
from components.music import play_music
from constants import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants


# Game states
class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    WIN = 3

# Fog of War class

# Footprint class

# Ghost types

# Ghost class

# Ingredient types

# Cooking Station class

# Player class

# Game class
>>>>>>> 4d294088e577594db8e865d47c65e45804ecde5c
class HauntedKitchen:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Haunted Kitchen")
        self.clock = pygame.time.Clock()
        self.state = constants.GameState.MENU

        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 36)

        self.fog_surface = pygame.Surface(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA
        )
        self.vision_radius = 250

        self.reset_game()

    def reset_game(self):
        self.player = {
            "x": constants.SCREEN_WIDTH // 2,
            "y": constants.SCREEN_HEIGHT // 2,
            "speed": 5,
            "radius": 20,
            "carrying": [],
        }

        self.ghosts = []
        for _ in range(4):
            self.ghosts.append({
                "x": random.randint(100, constants.SCREEN_WIDTH - 100),
                "y": random.randint(100, constants.SCREEN_HEIGHT - 100),
                "radius": 20,
                "speed": 2,
            })

        self.ingredients = []
        for _ in range(8):
            ing_type = random.choice(list(constants.IngredientType))
            self.ingredients.append({
                "x": random.randint(100, constants.SCREEN_WIDTH - 100),
                "y": random.randint(100, constants.SCREEN_HEIGHT - 100),
                "radius": 15,
                "type": ing_type,
                "collected": False,
            })

        self.stations = [
            {"x": 200, "y": 200, "w": 150, "h": 100, "type": "chopping", "progress": 0},
            {"x": 400, "y": 200, "w": 150, "h": 100, "type": "cooking", "progress": 0},
            {"x": constants.SCREEN_WIDTH - 350, "y": 200, "w": 150, "h": 100, "type": "serving", "progress": 0},
        ]

        self.haunt_level = 0
        self.max_haunt_level = 100
        self.dishes_served = 0
        self.dishes_needed = 3
        self.ghost_projectiles = []
        self.wrong_combo_active = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == constants.GameState.PLAYING:
                        self.state = constants.GameState.MENU
                    else:
                        return False
                if event.key == pygame.K_RETURN:
                    if self.state == constants.GameState.MENU:
                        self.state = constants.GameState.PLAYING
                        self.reset_game()
                    elif self.state in [constants.GameState.GAME_OVER, constants.GameState.WIN]:
                        self.state = constants.GameState.MENU
        return True

    def update(self):
        if self.state != constants.GameState.PLAYING:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player["y"] -= self.player["speed"]
        if keys[pygame.K_s]:
            self.player["y"] += self.player["speed"]
        if keys[pygame.K_a]:
            self.player["x"] -= self.player["speed"]
        if keys[pygame.K_d]:
            self.player["x"] += self.player["speed"]

        # Ghosts follow player
        for ghost in self.ghosts:
            dx = self.player["x"] - ghost["x"]
            dy = self.player["y"] - ghost["y"]
            dist = math.hypot(dx, dy)
            if dist > 0:
                ghost["x"] += ghost["speed"] * dx / dist
                ghost["y"] += ghost["speed"] * dy / dist

            if dist < ghost["radius"] + self.player["radius"]:
                self.state = constants.GameState.GAME_OVER

        # Projectiles update
        for proj in self.ghost_projectiles:
            proj["x"] += proj["vx"]
            proj["y"] += proj["vy"]
            if math.hypot(
                proj["x"] - self.player["x"],
                proj["y"] - self.player["y"]
            ) < proj["radius"] + self.player["radius"]:
                self.state = constants.GameState.GAME_OVER

        self.ghost_projectiles = [
            p for p in self.ghost_projectiles
            if 0 < p["x"] < constants.SCREEN_WIDTH and 0 < p["y"] < constants.SCREEN_HEIGHT
        ]

        # Ingredient collection
        for ing in self.ingredients:
            if not ing["collected"]:
                if math.hypot(
                    ing["x"] - self.player["x"],
                    ing["y"] - self.player["y"]
                ) < ing["radius"] + self.player["radius"]:
                    ing["collected"] = True
                    self.player["carrying"].append(ing["type"])

        # Station interaction
        for station in self.stations:
            inside = (
                station["x"] < self.player["x"] < station["x"] + station["w"]
                and station["y"] < self.player["y"] < station["y"] + station["h"]
            )
            if inside and keys[pygame.K_SPACE]:
                station["progress"] += 1
                if station["type"] == "serving" and station["progress"] >= 100:
                    recipe_name = self.check_recipe(self.player["carrying"])
                    if recipe_name:
                        self.dishes_served += 1
                        self.player["carrying"] = []
                        self.wrong_combo_active = False
                        station["progress"] = 0
                        if self.dishes_served >= self.dishes_needed:
                            self.state = constants.GameState.WIN
                    else:
                        self.wrong_combo_active = True
                        station["progress"] = 0

        # Spawn ghost projectiles if wrong combo active
        if self.wrong_combo_active and random.random() < 0.02:
            ghost = random.choice(self.ghosts)
            dx = self.player["x"] - ghost["x"]
            dy = self.player["y"] - ghost["y"]
            dist = math.hypot(dx, dy)
            if dist > 0:
                vx = 5 * dx / dist
                vy = 5 * dy / dist
                self.ghost_projectiles.append(
                    {"x": ghost["x"], "y": ghost["y"], "vx": vx, "vy": vy, "radius": 5}
                )

        self.haunt_level += 0.05
        if self.haunt_level >= self.max_haunt_level:
            self.state = constants.GameState.GAME_OVER

    def check_recipe(self, ingredients):
        for recipe_name, combo in constants.RECIPES.items():
            if sorted(combo) == sorted(ingredients):
                return recipe_name
        return None

    def draw(self):
        self.screen.fill(constants.BLACK)
        if self.state == constants.GameState.MENU:
            self.draw_menu()
        elif self.state == constants.GameState.PLAYING:
            self.draw_game()
        elif self.state == constants.GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.state == constants.GameState.WIN:
            self.draw_game()
            self.draw_win()
        pygame.display.flip()

    def draw_menu(self):
        title = self.font_large.render("HAUNTED KITCHEN", True, constants.GREEN)
        self.screen.blit(title, (constants.SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        text = self.font_small.render("Press ENTER to start", True, constants.WHITE)
        self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, 400))

    def draw_game(self):
        # ingredients
        for ing in self.ingredients:
            if not ing["collected"]:
                pygame.draw.circle(self.screen, constants.YELLOW, (int(ing["x"]), int(ing["y"])), ing["radius"])

        # ghosts
        for ghost in self.ghosts:
            pygame.draw.circle(self.screen, constants.PURPLE, (int(ghost["x"]), int(ghost["y"])), ghost["radius"])

        # projectiles
        for proj in self.ghost_projectiles:
            pygame.draw.circle(self.screen, constants.RED, (int(proj["x"]), int(proj["y"])), proj["radius"])

        # player
        pygame.draw.circle(self.screen, constants.BLUE, (int(self.player["x"]), int(self.player["y"])), self.player["radius"])

        # UI
        dishes_text = self.font_small.render(
            f"Dishes: {self.dishes_served}/{self.dishes_needed}", True, constants.WHITE
        )
        self.screen.blit(dishes_text, (50, 30))

    def draw_game_over(self):
        overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        text = self.font_large.render("GAME OVER", True, constants.RED)
        self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, constants.SCREEN_HEIGHT // 2))

    def draw_win(self):
        overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        text = self.font_large.render("YOU SURVIVED!", True, constants.GREEN)
        self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, constants.SCREEN_HEIGHT // 2))

    def run(self):
        running = True
        play_music();
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(constants.FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    HauntedKitchen().run()

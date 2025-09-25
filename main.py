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
        self.vision_radius = 250
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Haunted Kitchen")
        self.clock = pygame.time.Clock()
        self.state = constants.GameState.MENU

        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 36)
        
        # Fog of war system
        self.fog_of_war = FogOfWar(SCREEN_WIDTH, SCREEN_HEIGHT, self.vision_radius)
        
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
        
        # Update player
        self.player.update(keys)
        
        # Update fog of war
        # self.fog_of_war.update(self.player.x, self.player.y, self.stations)
        
        # Create footprints at intervals
        if self.player.footprint_timer >= self.player.footprint_interval:
            self.footprints.append(self.player.create_footprint())
            self.player.footprint_timer = 0
            
        # Update footprints (and remove faded ones)
        self.footprints = [f for f in self.footprints if f.update()]
        
        # Update ghosts
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

        # Title
        title = self.font_large.render("HAUNTED KITCHEN", True, GREEN)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        
        # Instructions
        instructions = [
            "Cook and serve dishes before the kitchen becomes too haunted!",
            "Move with WASD or Arrow Keys",
            "Collect ingredients and take them to stations",
            "Use SPACE at stations to prepare food",
            "Avoid ghosts that follow your footprints",
            "You can only see things in your immediate vicinity",
            "",
            "Press ENTER to start",
            "Press ESC to quit",
            "Press F during game to toggle visibility (debug)"
        ]
        
        for i, line in enumerate(instructions):
            text = self.font_small.render(line, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 350 + i * 40))
            
    def is_in_vision(self, x, y, radius=0):
        """Check if an object is within the player's vision"""
        distance = math.sqrt((x - self.player.x)**2 + (y - self.player.y)**2)
        return distance <= self.vision_radius + radius
    
    def draw_game(self):
        # Clear screen with black (this will be our fog)
        self.screen.fill(BLACK)
        
        # 1. Draw visible portions of the kitchen background
        self._draw_visible_background()
        
        # 2. Only draw objects that are in vision
        self._draw_visible_objects()
        
        # 3. Apply fog of war (for gradient edges)
        self.fog_of_war.draw(self.screen, self.player.x, self.player.y)
        
        # 4. Draw UI (always visible)
        self.draw_ui()
    
    def _draw_visible_background(self):
        """Only draw the parts of the background that are visible"""
        # Draw main kitchen area (simplified - in real game you'd want to clip this)
        if self.is_in_vision(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, max(SCREEN_WIDTH, SCREEN_HEIGHT)):
            pygame.draw.rect(self.screen, DARK_GRAY, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
            pygame.draw.rect(self.screen, LIGHT_GRAY, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), 5)
            
            # Draw counter tops if they might be visible
            if self.is_in_vision(SCREEN_WIDTH//2, 150, SCREEN_WIDTH):
                pygame.draw.rect(self.screen, BROWN, (100, 150, SCREEN_WIDTH - 200, 80))
            if self.is_in_vision(SCREEN_WIDTH//2, SCREEN_HEIGHT - 230, SCREEN_WIDTH):
                pygame.draw.rect(self.screen, BROWN, (100, SCREEN_HEIGHT - 230, SCREEN_WIDTH - 200, 80))
    
    def _draw_visible_objects(self):
        """Only draw objects that are within the player's vision"""
        # Draw stations in vision
        for station in self.stations:
            if self.is_in_vision(station.x + station.width//2, station.y + station.height//2, 
                               max(station.width, station.height)):
                station.draw(self.screen)
        
        # Draw ingredients in vision
        for ingredient in self.ingredients:
            if not ingredient.collected and self.is_in_vision(ingredient.x, ingredient.y, ingredient.radius):
                ingredient.draw(self.screen, self.player.x, self.player.y, self.vision_radius)
        
        # Draw footprints in vision
        for footprint in self.footprints:
            if self.is_in_vision(footprint.x, footprint.y, footprint.radius):
                footprint.draw(self.screen, self.player.x, self.player.y, self.vision_radius)
        
        # Draw ghosts in vision
        for ghost in self.ghosts:
            if self.is_in_vision(ghost.x, ghost.y, ghost.radius):
                ghost.draw(self.screen)
        
        # Always draw player
        self.player.draw(self.screen)
        
    def draw_ui(self):
        # Haunt level meter
        meter_width = 300
        meter_height = 20
        meter_x = SCREEN_WIDTH - meter_width - 50
        meter_y = 30
        
        # Background
        pygame.draw.rect(self.screen, DARK_GRAY, (meter_x, meter_y, meter_width, meter_height))
        
        # Fill based on haunt level
        fill_width = int(meter_width * (self.haunt_level / self.max_haunt_level))
        pygame.draw.rect(self.screen, RED, (meter_x, meter_y, fill_width, meter_height))
        
        # Border
        pygame.draw.rect(self.screen, WHITE, (meter_x, meter_y, meter_width, meter_height), 2)
        
        # Label
        haunt_text = self.font_small.render("Haunt Level", True, WHITE)
        self.screen.blit(haunt_text, (meter_x, meter_y - 30))
        
        # Dishes served
        dishes_text = self.font_small.render(f"Dishes: {self.dishes_served}/{self.dishes_needed}", True, WHITE)
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

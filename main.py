import pygame
import random
import math
import sys
from enum import Enum

from components.cookingStation import CookingStation
from components.fogOfWar import FogOfWar
from components.ghost import Ghost, GhostType
from components.ingredient import Ingredient, IngredientType
from components.player import Player
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
class HauntedKitchen:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Haunted Kitchen")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 36)
        
        # Fog of war system
        self.fog_of_war = FogOfWar(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.vision_radius = 250
        
        self.reset_game()
        
    def reset_game(self):
        # Create player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Create footprints list
        self.footprints = []
        
        # Create ghosts
        self.ghosts = [
            Ghost(100, 100, GhostType.FOLLOWER),
            Ghost(SCREEN_WIDTH - 100, 100, GhostType.FOLLOWER),
            Ghost(100, SCREEN_HEIGHT - 100, GhostType.PATROLLER),
            Ghost(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, GhostType.PATROLLER)
        ]
        
        # Create ingredients
        self.ingredients = []
        for _ in range(8):
            ingredient_type = random.choice(list(IngredientType))
            self.ingredients.append(
                Ingredient(
                    random.randint(100, SCREEN_WIDTH - 100),
                    random.randint(100, SCREEN_HEIGHT - 100),
                    ingredient_type
                )
            )
        
        # Create cooking stations
        self.stations = [
            CookingStation(200, 200, 150, 100, "chopping"),
            CookingStation(400, 200, 150, 100, "cooking"),
            CookingStation(SCREEN_WIDTH - 350, 200, 150, 100, "serving")
        ]
        
        # Game variables
        self.haunt_level = 0
        self.max_haunt_level = 100
        self.dishes_served = 0
        self.dishes_needed = 3
        self.ghost_spawn_timer = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.MENU
                    else:
                        return False
                        
                if event.key == pygame.K_RETURN:
                    if self.state == GameState.MENU:
                        self.state = GameState.PLAYING
                        self.reset_game()
                    elif self.state in [GameState.GAME_OVER, GameState.WIN]:
                        self.state = GameState.MENU
                        
                # Debug key to toggle fog of war (for testing)
                if event.key == pygame.K_f and self.state == GameState.PLAYING:
                    self.vision_radius = 2000 if self.vision_radius == 250 else 250
                        
        return True
        
    def update(self):
        if self.state != GameState.PLAYING:
            return
            
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.update(keys)
        
        # Update fog of war
        self.fog_of_war.update(self.player.x, self.player.y, self.stations)
        
        # Create footprints at intervals
        if self.player.footprint_timer >= self.player.footprint_interval:
            self.footprints.append(self.player.create_footprint())
            self.player.footprint_timer = 0
            
        # Update footprints (and remove faded ones)
        self.footprints = [f for f in self.footprints if f.update()]
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.player, self.footprints)
            
            # Check for collision with player
            dist = math.sqrt((ghost.x - self.player.x)**2 + (ghost.y - self.player.y)**2)
            if dist < ghost.radius + self.player.radius:
                self.state = GameState.GAME_OVER
                
        # Check for ingredient collection
        for ingredient in self.ingredients:
            if not ingredient.collected:
                dist = math.sqrt((ingredient.x - self.player.x)**2 + (ingredient.y - self.player.y)**2)
                if dist < ingredient.radius + self.player.radius:
                    ingredient.collected = True
                    self.player.carrying.append(ingredient)
                    
        # Check for station interaction
        for station in self.stations:
            # Check if player is near station
            player_in_station = (
                self.player.x > station.x and self.player.x < station.x + station.width and
                self.player.y > station.y and self.player.y < station.y + station.height
            )
            
            if player_in_station and keys[pygame.K_SPACE]:
                station.active = True
                station.progress += 1
                
                # If station is serving and player has ingredients
                if station.type == "serving" and len(self.player.carrying) > 0:
                    if station.progress >= 100:
                        self.dishes_served += 1
                        self.player.carrying = []  # Clear carried ingredients
                        station.progress = 0
                        
                        # Check for win condition
                        if self.dishes_served >= self.dishes_needed:
                            self.state = GameState.WIN
            else:
                station.active = False
                station.progress = 0
                
        # Increase haunt level over time
        self.haunt_level += 0.05
        
        # Spawn new ghosts if haunt level is high
        self.ghost_spawn_timer += 1
        if self.ghost_spawn_timer > 300 and len(self.ghosts) < 8 and self.haunt_level > 30:
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                x, y = random.randint(0, SCREEN_WIDTH), -50
            elif side == "bottom":
                x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 50
            elif side == "left":
                x, y = -50, random.randint(0, SCREEN_HEIGHT)
            else:  # right
                x, y = SCREEN_WIDTH + 50, random.randint(0, SCREEN_HEIGHT)
                
            ghost_type = GhostType.FOLLOWER if random.random() > 0.3 else GhostType.PATROLLER
            self.ghosts.append(Ghost(x, y, ghost_type))
            self.ghost_spawn_timer = 0
            
        # Game over if haunt level reaches max
        if self.haunt_level >= self.max_haunt_level:
            self.state = GameState.GAME_OVER
            
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.state == GameState.WIN:
            self.draw_game()
            self.draw_win()
            
        pygame.display.flip()
        
    def draw_menu(self):
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
            
    def draw_game(self):
        # Draw kitchen background (simplified)
        pygame.draw.rect(self.screen, DARK_GRAY, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
        pygame.draw.rect(self.screen, LIGHT_GRAY, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), 5)
        
        # Draw counter tops
        pygame.draw.rect(self.screen, BROWN, (100, 150, SCREEN_WIDTH - 200, 80))
        pygame.draw.rect(self.screen, BROWN, (100, SCREEN_HEIGHT - 230, SCREEN_WIDTH - 200, 80))
        
        # Draw stations (always visible once discovered, but dim when not in current vision)
        for station in self.stations:
            station.draw(self.screen, self.player.x, self.player.y, self.vision_radius)
            
        # Draw ingredients
        for ingredient in self.ingredients:
            ingredient.draw(self.screen, self.player.x, self.player.y, self.vision_radius)
            
        # Draw footprints
        for footprint in self.footprints:
            footprint.draw(self.screen, self.player.x, self.player.y, self.vision_radius)
            
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen, self.player.x, self.player.y, self.vision_radius)
            
        # Draw player
        self.player.draw(self.screen)
        
        # Draw fog of war
        self.fog_of_war.draw(self.screen)
        
        # Draw UI (always visible)
        self.draw_ui()
        
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
        
        # Ghost count
        ghosts_text = self.font_small.render(f"Ghosts: {len(self.ghosts)}", True, WHITE)
        self.screen.blit(ghosts_text, (50, 70))
        
        # Vision radius indicator (debug)
        if self.vision_radius == 2000:  # Debug mode
            debug_text = self.font_small.render("DEBUG: Full Visibility", True, YELLOW)
            self.screen.blit(debug_text, (SCREEN_WIDTH // 2 - debug_text.get_width() // 2, 100))
        
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over = self.font_large.render("GAME OVER", True, RED)
        self.screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        # Instructions
        instructions = self.font_medium.render("Press ENTER to return to menu", True, WHITE)
        self.screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
    def draw_win(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Win text
        win_text = self.font_large.render("YOU SURVIVED!", True, GREEN)
        self.screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        # Instructions
        instructions = self.font_medium.render("Press ENTER to return to menu", True, WHITE)
        self.screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = HauntedKitchen()
    game.run()
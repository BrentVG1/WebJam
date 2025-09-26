import sys
import math
import random
import pygame

from components.collisionObject import CollisionObject
from components.itemStation import ItemStation
import constants  # use namespaced constants everywhere

from components.SafeZone import SafeZone
from components.cookingStation import CookingStation
from components.fogOfWar import FogOfWar
from components.ghost import Ghost, GhostType
from components.ingredient import Ingredient, IngredientType
from components.player import Player
from components.music import play_music
from components.start_menu import StartMenu
from components.footprint import Footprint
from components.soundEffects import play_soundeffect

# --- Pygame init ---
pygame.init()
pygame.mixer.init()

# --- Userevents ---
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)


class HauntedKitchen:
    def __init__(self):
        self.vision_radius = 300
        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Haunted Kitchen")
        self.clock = pygame.time.Clock()
        self.state = constants.GameState.MENU
        self.debug = True
        self.menu = StartMenu()
        self.player_in_zone = False
        self.last_known_location = None
        self.interaction_proximity = 25

        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 36)
        self.background_img = pygame.image.load("sprites/vloer-tegel-modified.png").convert()
        self.background_img = pygame.transform.scale(
        self.background_img, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        # --- Safezone wood texture ---
        self.wood_tile = pygame.image.load("sprites/wood_tile.png").convert()

        self.playscream = bool

        self.fog_of_war = FogOfWar(
            constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, self.vision_radius)

        self.reset_game()

    def reset_game(self):
        # Create player
        self.player = Player(100,
                             300)
        self.old_player_x = self.player.x
        self.old_player_y = self.player.y

        # Create footprints list
        self.footprints = []

        self.safe_zone = SafeZone(
            0, constants.SCREEN_HEIGHT - 250, constants.SCREEN_WIDTH, 250)

        # Create ghosts
        self.ghosts = [
            Ghost(100, 100, GhostType.FOLLOWER, self.safe_zone.height),
            Ghost(constants.SCREEN_WIDTH - 100, 100,
                  GhostType.FOLLOWER, self.safe_zone.height),
            Ghost(100, constants.SCREEN_HEIGHT - 100,
                  GhostType.PATROLLER, self.safe_zone.height),
            Ghost(constants.SCREEN_WIDTH - 100,
                  constants.SCREEN_HEIGHT - 100, GhostType.PATROLLER, self.safe_zone.height),
        ]


        # Create cooking stations
        self.stations = [
            CookingStation(constants.SCREEN_WIDTH - 400,
                           300, 100, 100, "chopping"),
            CookingStation(400, 250, 100, 100, "cooking"),
  
            CookingStation(400,
                           constants.SCREEN_HEIGHT - self.safe_zone.height, 120, 100, "serving"),
        ]

        self.item_stations = [
            ItemStation(0, 0, 100, 100, Ingredient(
                50, 50, IngredientType.LETTUCE, "chopping")),
            ItemStation(100, 0, 100, 100, Ingredient(
                150, 50, IngredientType.TOMATO, "chopping")),
            ItemStation(200, 0, 100, 100, Ingredient(
                250, 50, IngredientType.CHEESE)),
            ItemStation(constants.SCREEN_WIDTH - 100, 0, 100, 100,
                        Ingredient(constants.SCREEN_WIDTH - 50, 50, IngredientType.PATTY, "cooking")),
            ItemStation(500, 450, 100, 50, Ingredient(
                550, 475, IngredientType.BUN)),
        ]

        self.colliding_objects = [
            CollisionObject(300, 250, constants.SCREEN_WIDTH -
                            600, 250),  # central table
            CollisionObject(0, constants.SCREEN_HEIGHT -
                            self.safe_zone.height - 5, 100, 10),
            CollisionObject(200, constants.SCREEN_HEIGHT -
                            self.safe_zone.height - 5, constants.SCREEN_WIDTH - 400, 10),
            CollisionObject(constants.SCREEN_WIDTH - 100, constants.SCREEN_HEIGHT -
                            self.safe_zone.height - 5, 100, 10),
        ]

        # Game variables
        self.haunt_level = 0
        self.max_haunt_level = 100
        self.dishes_served = 0
        self.dishes_needed = 3
        self.ghost_spawn_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            # Menu state delegates to StartMenu
            if self.state == constants.GameState.MENU:
                action = self.menu.handle_event(event)
                if action == "start":
                    self.state = constants.GameState.PLAYING
                    self.reset_game()
                elif action == "quit":
                    return False
                continue  # don't process menu events below

            # --- Loads and plays a new track
            if event.type == MUSIC_END:
                play_music()

            # --- Playing / GameOver / Win states ---
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC from playing -> back to menu; from other states -> quit
                    if self.state == constants.GameState.PLAYING:
                        self.state = constants.GameState.MENU
                    else:
                        return False

                elif event.key == pygame.K_F12:
                    self.debug = not self.debug

                elif event.key == pygame.K_RETURN:
                    if self.state in [constants.GameState.GAME_OVER, constants.GameState.WIN]:
                        self.state = constants.GameState.MENU

                # Toggle fog radius (debug)
                if event.key == pygame.K_f and self.state == constants.GameState.PLAYING:
                    self.vision_radius = 2000 if self.vision_radius == 250 else 250
                    if hasattr(self.fog_of_war, "radius"):
                        self.fog_of_war.radius = self.vision_radius

        return True

    def update(self):
        if self.state != constants.GameState.PLAYING:
            return

        keys = pygame.key.get_pressed()

        # Update player
        self.player.update(keys, [obj.obj_rect for obj in self.colliding_objects] + [
                           obj.obj_rect for obj in self.stations] + [obj.obj_rect for obj in self.item_stations])

        # (Optional) Update fog of war if it needs an update step
        # If your FogOfWar has an update method that takes player pos, call it:
        if hasattr(self.fog_of_war, "update"):
            try:
                self.fog_of_war.update(
                    self.player.x, self.player.y, self.stations)
            except TypeError:
                # Some versions may only accept (x, y) or different args; ignore if not needed
                pass

        # Create footprints at intervals
        # Create footprints at intervals
        if not keys[pygame.K_LSHIFT] and (not self.player.x - self.old_player_x == 0 or not self.player.y - self.old_player_y == 0):
            if self.player.footprint_timer >= self.player.footprint_interval:
                dx = self.player.x - self.old_player_x
                dy = self.player.y - self.old_player_y
                if dx != 0 or dy != 0:
                    angle = math.degrees(math.atan2(-dy, dx))
                    self.footprints.append(
                        Footprint(self.player.x, self.player.y, angle))

                    # play footstep sound for every other footprint created
                    if next(constants.play_footstep):
                        play_soundeffect("step")

                self.player.footprint_timer = 0
                self.last_known_location = self.player.x, self.player.y

            # Update footprints (and remove faded ones)
        self.footprints = [f for f in self.footprints if f.update()]

        self.player_in_zone = self.safe_zone.in_zone(
            self.player.x, self.player.y)

        # Update ghosts
        for ghost in self.ghosts:
            # Some ghost.update signatures may differ; call safely
            try:
                ghost.update(self.last_known_location,
                             self.footprints, self.player_in_zone)
            except TypeError:
                ghost.update(self.last_known_location,
                             None, self.player_in_zone)

            # Check collision with player
            dist = math.hypot(ghost.x - self.player.x, ghost.y - self.player.y)

            if dist >= 0 and dist <= 300:
                play_soundeffect("ghost")

            if dist < ghost.radius + self.player.radius:
                self.state = constants.GameState.GAME_OVER

        # Station interaction
        closest_proximity_station = []
        if keys[pygame.K_SPACE]:
            for item_station in self.item_stations:
                distance = item_station.distance_to_rect((self.player.x, self.player.y))
                if distance < self.interaction_proximity:
                    closest_proximity_station.append([item_station, "item"])
                    
            for station in self.stations:
                distance = station.distance_to_rect((self.player.x, self.player.y))
                if distance < self.interaction_proximity:
                    closest_proximity_station.append([station, "station"])
            
            if not len(closest_proximity_station) == 0:
                closest_station = min(closest_proximity_station, key=lambda x: x[0].distance_to_rect((self.player.x, self.player.y)))
                if closest_station[1] == "item":
                    self.player.carrying = closest_station[0].ingredient                
                else:
                    # activate/progress
                    if hasattr(station, "active"):
                        station.active = True
                    if hasattr(station, "progress"):
                        station.progress += 1

                    # Serving station consumes carried item when complete
                    if station.type == "serving" and getattr(self.player, "has_item", lambda: False)():
                        if getattr(station, "progress", 0) >= 100:
                            self.dishes_served += 1
                            # consume carried item
                            if hasattr(self.player, "consume"):
                                self.player.consume()
                            else:
                                self.player.carrying = None
                            station.progress = 0

                            if self.dishes_served >= self.dishes_needed:
                                self.state = constants.GameState.WIN
            else:
                if hasattr(station, "active"):
                    station.active = False
                if hasattr(station, "progress"):
                    station.progress = 0

        # Increase haunt level over time
        # Increase/decrease haunt level afhankelijk van safe zone
        if self.player_in_zone:
            self.haunt_level -= 0.05  # daalt in safe zone
        else:
            self.haunt_level += 0.03  # stijgt buiten safe zone
        self.haunt_level = max(0, min(self.haunt_level, self.max_haunt_level))

        # Spawn new ghosts if haunt level is high
        self.ghost_spawn_timer += 1
        if self.ghost_spawn_timer > 300 and len(self.ghosts) < 8 and self.haunt_level > 30:
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                x, y = random.randint(0, constants.SCREEN_WIDTH), -50
            elif side == "bottom":
                x, y = random.randint(
                    0, constants.SCREEN_WIDTH), constants.SCREEN_HEIGHT + 50
            elif side == "left":
                x, y = -50, random.randint(0, constants.SCREEN_HEIGHT)
            else:  # right
                x, y = constants.SCREEN_WIDTH + \
                    50, random.randint(0, constants.SCREEN_HEIGHT)

            ghost_type = GhostType.FOLLOWER if random.random() > 0.3 else GhostType.PATROLLER
            self.ghosts.append(Ghost(x, y, ghost_type))
            self.ghost_spawn_timer = 0

        # Game over if haunt level reaches max
        if self.haunt_level >= self.max_haunt_level:
            self.state = constants.GameState.GAME_OVER

        self.old_player_x = self.player.x
        self.old_player_y = self.player.y

    # -------- drawing helpers --------
    def is_in_vision(self, x, y, radius=0):
        """Check if an object
            is within the player's vision"""
        distance = math.hypot(x - self.player.x, y - self.player.y)
        return distance <= self.vision_radius + radius

    def draw(self):
        if self.state == constants.GameState.MENU:
            self.menu.draw(self.screen)
        else:
            self.screen.fill(constants.BLACK)

            if self.state == constants.GameState.PLAYING:
                self.draw_game()

                # set bool to true so it plays when it's game over
                self.playscream = True
            elif self.state == constants.GameState.GAME_OVER:
                self.draw_game()
                self.draw_game_over()
                # play death soundeffect
                if self.playscream:
                    play_soundeffect("scream")
                self.playscream = False
            elif self.state == constants.GameState.WIN:
                self.draw_game()
                self.draw_win()

        pygame.display.flip()

    def draw_game(self):
        # Alles tekenen
        self.screen.fill(constants.BLACK)
        self._draw_visible_background()
        self._draw_safe_zone()
        self._draw_visible_objects()
        if not self.debug:
            self.fog_of_war.draw(self.screen, self.player.x, self.player.y)
        self.player.draw(self.screen)

        # UI altijd **laatste**
        self.draw_ui()

    def _draw_visible_background(self):
        self.screen.blit(self.background_img, (0, 0))


    def _draw_visible_objects(self):
        """Only draw objects that are within the player's vision"""
        for obj in self.colliding_objects:
            if self.is_in_vision(obj.x + obj.width // 2, obj.y + obj.height // 2,
                                 max(obj.width, obj.height)) or self.debug:
                obj.draw(self.screen)
        # Draw stations in vision
        for station in self.stations:
            # If your station.draw takes only (screen), call as below:
            if self.is_in_vision(station.x + station.width // 2, station.y + station.height // 2,
                                 max(station.width, station.height)) or self.debug:
                try:
                    station.draw(self.screen, self.player.x,
                                 self.player.y, self.vision_radius)
                except TypeError:
                    station.draw(self.screen)

        for item_station in self.item_stations:
            if self.is_in_vision(item_station.x + item_station.width // 2, item_station.y + item_station.height // 2,
                                 max(item_station.width, item_station.height)) or self.debug:
                try:
                    item_station.draw(self.screen, self.player.x,
                                      self.player.y, self.vision_radius)
                except TypeError:
                    item_station.draw(self.screen)

        for footprint in self.footprints:
            if self.is_in_vision(footprint.x, footprint.y, footprint.radius) or self.debug:
                try:
                    footprint.draw(self.screen, self.player.x,
                                   self.player.y, self.vision_radius)
                except TypeError:
                    footprint.draw(self.screen)

        for ghost in self.ghosts:
            if self.is_in_vision(ghost.x, ghost.y, ghost.radius) or self.debug:
                ghost.draw(self.screen)

        # Always draw player

    def _draw_safe_zone(self):
        sz = self.safe_zone

        # --- Draw wood texture background ---
        wood_scaled = pygame.transform.scale(self.wood_tile, (sz.width, sz.height))
        surface = wood_scaled.copy()

        t = pygame.time.get_ticks() * 0.002  # rustig tempo

        # --- Check danger ---
        danger = any(
            ghost.current_type == GhostType.FOLLOWER and
            math.hypot(ghost.x - self.player.x, ghost.y - self.player.y) < 150
            for ghost in self.ghosts
        )

        # --- Base colors ---
        if danger:
            base_colors = [(255, 80, 80), (255, 120, 120)]
            text_color = (255, 200, 200)
        else:
            base_colors = [(80, 180, 255), (120, 220, 255)]
            text_color = (255, 255, 255)

        # Make a transparent overlay for glow & effects
        overlay = pygame.Surface((sz.width, sz.height), pygame.SRCALPHA)

        # Glow
        pulse = 60 + 40 * math.sin(t)
        for i, col in enumerate(base_colors):
            alpha = int(pulse / (i + 1))
            glow_color = (*col, alpha)
            pygame.draw.rect(overlay, glow_color,
                            (-i * 5, -i * 5, sz.width + i * 10, sz.height + i * 10),
                            border_radius=25 + i * 5)

        # Waves
        wave_count = 8
        wave_height = 10
        top_points, bottom_points = [], []
        for i in range(wave_count + 1):
            x = i * (sz.width / wave_count)
            top_y = wave_height * math.sin(t + i * 0.5)
            bottom_y = sz.height - wave_height * math.sin(t + i * 0.5 + math.pi / 2)
            top_points.append((x, top_y))
            bottom_points.append((x, bottom_y))
        top_points = [(0, 0)] + top_points + [(sz.width, 0)]
        bottom_points = [(0, sz.height)] + bottom_points + [(sz.width, sz.height)]
        pygame.draw.polygon(overlay, (*base_colors[0], 120), top_points)
        pygame.draw.polygon(overlay, (*base_colors[1], 120), bottom_points)

        # Sparkles
        for _ in range(15):
            px = random.randint(0, sz.width)
            py = random.randint(0, sz.height)
            radius = random.randint(1, 3)
            alpha = random.randint(30, 100)
            pygame.draw.circle(overlay, (255, 255, 255, alpha), (px, py), radius)

        # Blit overlay on top of wood
        surface.blit(overlay, (0, 0))

        # SAFE ZONE text
        font = pygame.font.SysFont(None, 48)
        text = font.render("SAFE ZONE", True, text_color)
        text_rect = text.get_rect(center=(sz.width // 2, sz.height // 2))
        surface.blit(text, text_rect)

        # Finally blit to screen
        self.screen.blit(surface, (sz.x, sz.y))




    def draw_ui(self):
        # Maak een aparte surface voor de UI
        ui_surface = pygame.Surface(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)

        meter_width = 300
        meter_height = 20
        meter_x = constants.SCREEN_WIDTH - meter_width - 50
        meter_y = 30

        # Achtergrond meter
        pygame.draw.rect(ui_surface, constants.DARK_GRAY,
                         (meter_x, meter_y, meter_width, meter_height))

        # Dynamische kleur: groen → rood
        fear_ratio = self.haunt_level / self.max_haunt_level
        fill_width = int(meter_width * fear_ratio)
        # Rood neemt toe, groen af
        color = (int(255 * fear_ratio), int(255 * (1 - fear_ratio)), 0)
        pygame.draw.rect(ui_surface, color,
                         (meter_x, meter_y, fill_width, meter_height))

        # Border
        pygame.draw.rect(ui_surface, constants.WHITE,
                         (meter_x, meter_y, meter_width, meter_height), 2)

        # Label boven meter
        haunt_text = self.font_small.render(
            "Fear Meter", True, constants.WHITE)
        ui_surface.blit(
            haunt_text,
            (meter_x + meter_width - haunt_text.get_width(), meter_y - 30)
        )

        # Andere info linksboven
        dishes_text = self.font_small.render(
            f"Dishes: {self.dishes_served}/{self.dishes_needed}", True, constants.WHITE
        )
        ui_surface.blit(dishes_text, (50, 30))

        ghosts_text = self.font_small.render(
            f"Ghosts: {len(self.ghosts)}", True, constants.WHITE
        )
        ui_surface.blit(ghosts_text, (50, 70))

        if self.vision_radius == 2000:
            debug_text = self.font_small.render(
                "DEBUG: Full Visibility", True, constants.YELLOW
            )
            ui_surface.blit(
                debug_text,
                (constants.SCREEN_WIDTH // 2 - debug_text.get_width() // 2, 100),
            )

        # Blit de UI surface **bovenop alles**, inclusief fog
        self.screen.blit(ui_surface, (0, 0))

    def draw_game_over(self):
        overlay = pygame.Surface(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        text = self.font_large.render("GAME OVER", True, constants.RED)
        self.screen.blit(text, (constants.SCREEN_WIDTH // 2 -
                         text.get_width() // 2, constants.SCREEN_HEIGHT // 2))

    def draw_win(self):
        overlay = pygame.Surface(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        text = self.font_large.render("YOU SURVIVED!", True, constants.GREEN)
        self.screen.blit(text, (constants.SCREEN_WIDTH // 2 -
                         text.get_width() // 2, constants.SCREEN_HEIGHT // 2))

    def run(self):
        try:
            play_music()
        except Exception as e:
            print(f"Music error: {e}")

        running = True
        while running:
            running = self.handle_events()
            if not running:
                break

            self.update()
            self.draw()
            self.clock.tick(constants.FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    HauntedKitchen().run()

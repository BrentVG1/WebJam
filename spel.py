import pygame
import sys

# --- Init ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Footprint Demo")
clock = pygame.time.Clock()

# --- Kleuren ---
GREEN = (50, 200, 50)
SKIN = (255, 220, 177)
HAIR = (100, 50, 20)
SHIRT = (50, 100, 255)
PANTS = (30, 30, 120)
SHOE_MAIN = (40, 40, 40)   # donkergrijs
SHOE_SOLE = (200, 200, 200)  # lichtgrijs zool

# --- Speler ---
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
step_counter = 0
STEP_DELAY = 15
last_direction = (0, 1)

# --- Voetafdrukken lijst ---
footprints = []
FOOTPRINT_LIFETIME = 90  # frames (1.5 sec bij 60 FPS)

# --- Game Loop ---
running = True
while running:
    clock.tick(60)
    
    # Input
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -player_speed
    if keys[pygame.K_RIGHT]:
        dx = player_speed
    if keys[pygame.K_UP]:
        dy = -player_speed
    if keys[pygame.K_DOWN]:
        dy = player_speed
    
    if dx != 0 or dy != 0:
        last_direction = (dx, dy)
    
    player_x += dx
    player_y += dy
    
    # Voetafdrukken (nu dichter bij speler)
    if (dx != 0 or dy != 0):
        step_counter += 1
        if step_counter >= STEP_DELAY:
            step_counter = 0
            offset_x = -last_direction[0] * 8   # korter offset
            offset_y = -last_direction[1] * 8
            footprints.append({"pos": (player_x + 8 + offset_x, player_y + 58 + offset_y), "timer": FOOTPRINT_LIFETIME})
            footprints.append({"pos": (player_x + 26 + offset_x, player_y + 58 + offset_y), "timer": FOOTPRINT_LIFETIME})
    
    # Timers aftellen
    for f in footprints:
        f["timer"] -= 1
    footprints = [f for f in footprints if f["timer"] > 0]
    
    # --- Tekenen ---
    screen.fill(GREEN)
    
    # Voetafdrukken tekenen (donkere ellipsen)
    for f in footprints:
        alpha = int(255 * (f["timer"] / FOOTPRINT_LIFETIME))
        footprint_surface = pygame.Surface((16, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(footprint_surface, (30, 20, 10, alpha), (0, 0, 16, 8))
        screen.blit(footprint_surface, f["pos"])
    
    # Poppetje tekenen
    # Hoofd
    pygame.draw.circle(screen, SKIN, (player_x + 20, player_y), 15)
    pygame.draw.circle(screen, HAIR, (player_x + 20, player_y - 5), 15)
    
    # Romp
    pygame.draw.rect(screen, SHIRT, (player_x + 5, player_y + 10, 30, 25))
    
    # Benen
    pygame.draw.rect(screen, PANTS, (player_x + 5, player_y + 35, 10, 20))
    pygame.draw.rect(screen, PANTS, (player_x + 25, player_y + 35, 10, 20))
    
    # Schoenen (meer detail)
    # Linkerschoen
    pygame.draw.ellipse(screen, SHOE_MAIN, (player_x + 0, player_y + 52, 20, 12))
    pygame.draw.rect(screen, SHOE_SOLE, (player_x + 0, player_y + 62, 20, 4))
    # Rechterschoen
    pygame.draw.ellipse(screen, SHOE_MAIN, (player_x + 20, player_y + 52, 20, 12))
    pygame.draw.rect(screen, SHOE_SOLE, (player_x + 20, player_y + 62, 20, 4))
    
    pygame.display.flip()
    
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()

import pygame, math, sys

# --- setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
HALF_HEIGHT = HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)

# --- kleuren ---
CEILING_COLOR = (240, 240, 240) # wit plafond
FLOOR_COLOR = (139, 69, 19) # bruin vloer
WALL_COLOR_1 = (245, 245, 220) # licht beige muur
WALL_COLOR_2 = (235, 235, 200) # variatie beige muur
DOOR_COLOR = (150, 100, 50) # deur bruin

# --- map layout ---
# 1 = muur, 0 = leeg, 2 = deur
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,2,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,1],
    [1,0,1,0,1,1,1,0,1,0,0,1],
    [1,0,0,0,0,0,0,0,2,0,0,1],
    [1,0,1,0,1,1,1,0,1,0,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
]
MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)
TILE_SIZE = 64

# --- deuren (status: open/gesloten) ---
# dict met (i,j) : open_progress (0 = dicht, 1 = open)
doors = {(9,2):0, (8,5):0}
labels = {(9,2):"Koelcel", (8,5):"Keuken"}

# --- speler ---
player_x, player_y = 2*TILE_SIZE, 2*TILE_SIZE
player_angle = 0
player_speed = 2.5

# --- raycasting ---
FOV = math.pi/3
HALF_FOV = FOV/2
NUM_RAYS = 160
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = DIST * TILE_SIZE
SCALE = WIDTH // NUM_RAYS


def ray_casting(sc, px, py, pa):
    cur_angle = pa - HALF_FOV
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        for depth in range(MAX_DEPTH):
            x = px + depth * cos_a
            y = py + depth * sin_a

            i, j = int(x // TILE_SIZE), int(y // TILE_SIZE)
            if 0 <= i < MAP_WIDTH and 0 <= j < MAP_HEIGHT:
                cell = MAP[j][i]
                if cell == 1 or cell == 2:
                    # check of deur open is
                    offset = 0
                    if cell == 2:
                        prog = doors.get((i,j),0)
                        if prog >= 1:  # volledig open, geen muur tekenen
                            break
                        offset = prog * TILE_SIZE

                    depth *= math.cos(pa - cur_angle)
                    proj_height = PROJ_COEFF / (depth+0.0001)

                    if cell == 1:
                        if abs(x % TILE_SIZE - TILE_SIZE//2) < abs(y % TILE_SIZE - TILE_SIZE//2):
                            base_color = WALL_COLOR_1
                        else:
                            base_color = WALL_COLOR_2
                    else:
                        base_color = DOOR_COLOR

                    shade = 255 / (1 + depth * depth * 0.0001)
                    shade_factor = max(0.2, min(1.0, shade/255))
                    color = (int(base_color[0]*shade_factor),
                             int(base_color[1]*shade_factor),
                             int(base_color[2]*shade_factor))

                    pygame.draw.rect(sc, color,
                                     (ray*SCALE, HALF_HEIGHT - proj_height//2,
                                      SCALE, proj_height))

                    # label tonen als deur
                    if cell == 2 and (i,j) in labels:
                        text = font.render(labels[(i,j)], True, (255,255,0))
                        sc.blit(text, (ray*SCALE, HALF_HEIGHT - proj_height//2 - 30))

                    break
        cur_angle += DELTA_ANGLE


# --- main loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            # check of er een deur dichtbij is
            pi, pj = int(player_x//TILE_SIZE), int(player_y//TILE_SIZE)
            for (i,j) in doors:
                if abs(i - pi) <= 1 and abs(j - pj) <= 1:
                    if doors[(i,j)] < 1:
                        doors[(i,j)] = 1  # deur open

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        nx = player_x + player_speed * math.cos(player_angle)
        ny = player_y + player_speed * math.sin(player_angle)
        if MAP[int(ny//TILE_SIZE)][int(nx//TILE_SIZE)] == 0:
            player_x, player_y = nx, ny
    if keys[pygame.K_DOWN]:
        nx = player_x - player_speed * math.cos(player_angle)
        ny = player_y - player_speed * math.sin(player_angle)
        if MAP[int(ny//TILE_SIZE)][int(nx//TILE_SIZE)] == 0:
            player_x, player_y = nx, ny
    if keys[pygame.K_LEFT]:
        player_angle -= 0.05
    if keys[pygame.K_RIGHT]:
        player_angle += 0.05

    # achtergrond
    screen.fill(CEILING_COLOR, (0,0,WIDTH,HALF_HEIGHT))
    screen.fill(FLOOR_COLOR, (0,HALF_HEIGHT,WIDTH,HALF_HEIGHT))

    ray_casting(screen, player_x, player_y, player_angle)

    pygame.display.flip()
    clock.tick(60)
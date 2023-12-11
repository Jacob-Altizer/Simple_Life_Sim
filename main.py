import pygame, tile_map, time, math, random
from Input_Methods import button
from Entities import entity, spawn
from images import sprites

MAP_WIDTH, MAP_HEIGHT = 1920, 1080
TILE_SIZE = 16
GRID_WIDTH = MAP_WIDTH // TILE_SIZE
GRID_HEIGHT = MAP_HEIGHT // TILE_SIZE

LAND_COLOR = (39, 120, 36, 255)
WATER_COLOR = (28, 163, 236, 255)

WIN_WIDTH, WIN_HEIGHT = (GRID_WIDTH * TILE_SIZE), (GRID_HEIGHT * TILE_SIZE)

LAND_FILL_PERECENT = 45

start_frame = time.time()
frame_spacing = 16
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
background = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

gui = pygame.sprite.Group()

running = True

new_map = tile_map.Tile_Code()


new_map.generate_seed(x_size=GRID_WIDTH, y_size=GRID_HEIGHT, fill_percent=LAND_FILL_PERECENT)
generate_map_btn = button.Button((204,204,204), 300, 150)

exit_button = button.Img_Button("images/exit_button.png", 70, 70)
refresh_map_btn = button.Img_Button("images/refresh_arrow.png", 100, 100)

rocks = pygame.sprite.Group()
bunnies = pygame.sprite.Group()
plants = pygame.sprite.Group()

first_tick = True

tick_count = 0

def populate_world(group:pygame.sprite.Group, surface, Entity, amount):

    for ent in spawn.Spawn.spawn_random(surface, Entity, LAND_COLOR, amount):
        group.add(ent)

while running:

    tick_count += 1

    new_map.draw_map(GRID_WIDTH, GRID_HEIGHT, screen, TILE_SIZE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()

            if exit_button.is_clicked(position[0], position[1]):
                running = False

            if refresh_map_btn.is_clicked(position[0], position[1]):
                new_map.generate_seed(x_size=GRID_WIDTH, y_size=GRID_HEIGHT, fill_percent=LAND_FILL_PERECENT)
                first_tick = True

    for rock in rocks:
        rock.move_to_land(screen, WATER_COLOR, LAND_COLOR)

    for bunny in bunnies:
        if bunny.expire():
            bunny.kill()

        if not bunny.seeking:
            bunny.wander((WIN_WIDTH, WIN_HEIGHT))
        
        for grass in plants:
            bunny.seek(grass)
            bunny.visualize_path(screen)

    fed_bunnies = pygame.sprite.groupcollide(bunnies, plants, False, True)

    for bunny in fed_bunnies:
        bunny.seeking = False

 
    bunnies.update()
    bunnies.draw(screen)

    plants.update()
    plants.draw(screen)
    
    rocks.update()
    rocks.draw(screen)

    # draw buttons over other layers
    exit_button.draw(screen, math.floor(MAP_WIDTH * 0.96), math.floor(MAP_HEIGHT * 0.01))
    refresh_map_btn.draw(screen, math.floor(MAP_WIDTH * 0.01), math.floor(MAP_HEIGHT * 0.008))

    pygame.display.flip()

    if first_tick:
        populate_world(rocks, screen, entity.Rock, 40)
        populate_world(bunnies, screen, entity.Bunny, 120)
        populate_world(plants, screen, entity.Grass, 300)
    
    clock.tick(FPS)

    first_tick = False

pygame.quit()
print(tick_count)


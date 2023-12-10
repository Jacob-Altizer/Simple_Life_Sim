import pygame, tile_map, time, math, random
from Input_Methods import button
from Entities import entity, spawn
from images import sprites

MAP_WIDTH, MAP_HEIGHT = 1920, 1080
TILE_SIZE = 16
GRID_WIDTH = MAP_WIDTH // TILE_SIZE
GRID_HEIGHT = MAP_HEIGHT // TILE_SIZE

LAND_COLOR = (39, 153, 36, 255)
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

first_tick = True

def populate_world(group:pygame.sprite.Group, surface):

    for ent in spawn.Spawn.spawn_random(surface, entity.Rock, sprites.Rock_Sprite.sprites["rock"], LAND_COLOR, 60):
        group.add(ent)

while running:

    new_map.draw_map(GRID_WIDTH, GRID_HEIGHT, screen, TILE_SIZE)

    # draw buttons over other layers
    exit_button.draw(screen, math.floor(MAP_WIDTH * 0.96), math.floor(MAP_HEIGHT * 0.01))
    refresh_map_btn.draw(screen, math.floor(MAP_WIDTH * 0.01), math.floor(MAP_HEIGHT * 0.008))

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
                    rock.kill()

    for rock in rocks:
        rock.wander()
        
    rocks.update()
    rocks.draw(screen)

    if first_tick:
        populate_world(rocks, screen)
        print(len(rocks))

    pygame.display.flip()
    
    clock.tick(FPS)

    first_tick = False

pygame.quit()


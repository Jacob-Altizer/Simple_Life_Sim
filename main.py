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
FPS = 20

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

male_bunnies = pygame.sprite.Group()
female_bunnies = pygame.sprite.Group()

first_tick = True

tick_count = 0
grass_spawn_interval = 0

possible_spawn_points = []

def populate_world(group:pygame.sprite.Group, surface, Entity, amount, spawn_point_list):

    for ent in spawn.Spawn.spawn_random(surface, Entity, amount, spawn_point_list):
        group.add(ent)

while running:

    tick_count += 1
    grass_spawn_interval += 1

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


    if first_tick:
        for y in range(screen.get_height()):
            for x in range(screen.get_width()):
                if screen.get_at((x,y)) == LAND_COLOR:
                    possible_spawn_points.append([x,y])

    for grass in plants:
        if grass.reproduce(5, grass_spawn_interval):
            for new_grass in spawn.Spawn.spawn_random(screen, entity.Grass, 1, possible_spawn_points):
                plants.add(new_grass)

            grass_spawn_interval = 0

    for bunny in bunnies:
        bunny.move_to_land(screen, WATER_COLOR)

        if bunny.expire():
            bunny.kill()

        if not bunny.seeking:
            bunny.wander(screen, (WIN_WIDTH, WIN_HEIGHT), WATER_COLOR)
        
        for grass in plants:
            bunny.seek(screen, grass)
            bunny.visualize_path(screen)

    fed_bunnies = pygame.sprite.groupcollide(bunnies, plants, False, True)
    for bunny in pygame.sprite.groupcollide(female_bunnies, male_bunnies, False, False):
        bunny.pregnant = 1 if random.randint(0,100) > 85 else 0

    for bunny in female_bunnies:
        if bunny.pregnant == 1:
            if random.randint(0,100) > 75:
                cords = spawn.Spawn.spawn_near(screen, (math.floor(bunny.current_x), math.floor(bunny.current_y)), possible_spawn_points)
                new_bunny = entity.Bunny(cords[0], cords[1])
                bunnies.add(new_bunny)
                male_bunnies.add(new_bunny) if new_bunny.gender == 0 else female_bunnies.add(new_bunny)

                print("new_bunny")

            bunny.pregnant = 0

    for bunny in fed_bunnies:
        bunny.seeking = False
        bunny.hunger += 10

 
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
        populate_world(rocks, screen, entity.Rock, 40, possible_spawn_points)
        populate_world(bunnies, screen, entity.Bunny, 100, possible_spawn_points)
        populate_world(plants, screen, entity.Grass, 300, possible_spawn_points)

        for bunny in bunnies:
            if bunny.gender == 0:
                pygame.sprite.Group.add(male_bunnies, bunny)
            if bunny.gender == 1:
                pygame.sprite.Group.add(female_bunnies, bunny)
    
    clock.tick(FPS)

    first_tick = False

pygame.quit()
print(tick_count)
print(len(male_bunnies))
print(len(female_bunnies))


import pygame, tile_map, math, random, uuid, json
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

LAND_FILL_PERECENT = 46

BUNNY_CHANCE_TO_SPAWN = 60
BUNNY_CHANCE_TO_REPRODUCE = 75

CAT_CHANCE_TO_SPAWN = 75
CAT_CHANCE_TO_REPRODUCE = 88

frame_spacing = 16
FPS = 15

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
play_button = button.Img_Button("images/play_button.png", 250, 250)

rocks = pygame.sprite.Group()
bunnies = pygame.sprite.Group()
plants = pygame.sprite.Group()
cats = pygame.sprite.Group()

male_bunnies = pygame.sprite.Group()
female_bunnies = pygame.sprite.Group()

male_cats = pygame.sprite.Group()
female_cats = pygame.sprite.Group()

first_tick = True
sim_started = False

tick_count = 0
grass_spawn_interval = 0
grass_spawn_count = 9

possible_spawn_points = []
# roller = button.Roller_Button("gray", 200, 500, text_color=(0,0,1))


events = {}
event_count = 0
def log_event(tick:int, entity_name:str, event_name:str):
    global event_count
    event_count += 1

    event_id = uuid.uuid4().int

    new_event = [event_count, tick, entity_name, event_name]

    events[event_id] = new_event


def populate_world(group:pygame.sprite.Group, surface, Entity, amount, spawn_point_list):

    for ent in spawn.Spawn.spawn_random(surface, Entity, amount, spawn_point_list):
        group.add(ent)
        log_event(tick_count, ent.name, f"{ent.name} {amount} spawned")


def correct_seek_behavior(animal, interval):
    if interval % 5 == 2:
        animal.last_pos = animal.rect.center

    if interval % 5 == 0:
        if animal.last_pos == animal.rect.center:
            animal.seeking = False


def create_new_child(spawn_parent_group, chance_to_spawn, host_group, male_parent_group, female_parent_group, Ent_to_spawn, max_child_count, set_life_span):

    for parent in spawn_parent_group:
        if parent.pregnant == 1:
            if random.randint(0,100) > chance_to_spawn:
                cords = spawn.Spawn.spawn_near(screen, (math.floor(parent.current_x), math.floor(parent.current_y)), possible_spawn_points)
                new_ent = Ent_to_spawn(cords[0], cords[1])
                host_group.add(new_ent)
                male_parent_group.add(new_ent) if new_ent.gender == 0 else female_parent_group.add(new_ent)

                log_event(tick_count, parent.name, f"{parent.name} birthed {new_ent.name} gender {new_ent.gender} x:{parent.current_x},y:{parent.current_y}")

            parent.pregnant = 0
            if parent.child_count == max_child_count:
                parent.life_span = set_life_span
            


def reproduce(female_group, male_group, chance_to_reproduce):
    for entity in pygame.sprite.groupcollide(female_group, male_group, False, False):
        if random.randint(0,100) > chance_to_reproduce:
            entity.pregnant = 1
            log_event(tick_count, entity.name, f"{entity.name} gestating: chance {100 - chance_to_reproduce}")
        else:
            entity.pregnant = 0
            log_event(tick_count, entity.name, f"{entity.name} failed gestation: chance {chance_to_reproduce}")
        


def sort_by_gender(parent_group, female_group, male_group):
    for entity in parent_group:
        if entity.gender == 0:
            pygame.sprite.Group.add(male_group, entity)
        if entity.gender == 1:
            pygame.sprite.Group.add(female_group, entity)


def kill_if_expire(entity):

    if entity.expire():
        entity.kill()
        log_event(tick_count, entity.name, f"{entity.name} expired")
        return True
        

def cleanup_tasks():
    rocks.empty()
    bunnies.empty()
    plants.empty()
    cats.empty()

    male_bunnies.empty()
    female_bunnies.empty()

    male_cats.empty()
    female_cats.empty()

    tick_count = 0
    grass_spawn_interval = 0

    first_tick = False


while running:
    new_map.draw_map(GRID_WIDTH, GRID_HEIGHT, screen, TILE_SIZE)

    if sim_started:
        tick_count += 1
        grass_spawn_interval += 1

        if first_tick:
            for y in range(screen.get_height()):
                for x in range(screen.get_width()):
                    if screen.get_at((x,y)) == LAND_COLOR:
                        possible_spawn_points.append([x,y])

        for grass in plants:
            if grass.reproduce(2, grass_spawn_interval):
                for new_grass in spawn.Spawn.spawn_random(screen, entity.Grass, grass_spawn_count, possible_spawn_points):
                    plants.add(new_grass)
                    log_event(tick_count, new_grass.name, f"{grass_spawn_count} {new_grass.name} spawned")

                grass_spawn_interval = 0

        for bunny in bunnies:
            bunny.move_to_land(screen, WATER_COLOR)

            correct_seek_behavior(bunny, tick_count)

            kill_if_expire(bunny)

            if not bunny.seeking:
                bunny.wander(screen, (WIN_WIDTH, WIN_HEIGHT), WATER_COLOR)
            
            for grass in plants:
                bunny.seek(screen, grass)
                bunny.visualize_path(screen)

        reproduce(female_bunnies, male_bunnies, BUNNY_CHANCE_TO_REPRODUCE)
        create_new_child(female_bunnies, BUNNY_CHANCE_TO_SPAWN, bunnies, male_bunnies, female_bunnies, entity.Bunny, 5, 2)

        fed_bunnies = pygame.sprite.groupcollide(bunnies, plants, False, True)
        for bunny in fed_bunnies:
            log_event(tick_count, bunny.name, f"{bunny.name} ate grass,hunger:{bunny.hunger}->{bunny.hunger+1}")
            bunny.seeking = False
            bunny.hunger += 1


        for cat in cats:

            correct_seek_behavior(cat, tick_count)

            kill_if_expire(cat)

            if not cat.seeking:
                cat.wander(screen, (WIN_WIDTH, WIN_HEIGHT), WATER_COLOR)

            cat.move_to_land(screen, WATER_COLOR)

            for bunny in bunnies:
                cat.seek(screen, bunny)

            cat.visualize_path(screen)

        reproduce(female_cats, male_cats, CAT_CHANCE_TO_REPRODUCE)
        create_new_child(female_cats, CAT_CHANCE_TO_SPAWN, cats, male_cats, female_cats, entity.Cat, 5, 0.5)

        fed_cats = pygame.sprite.groupcollide(cats, bunnies, False, True)
        for cat in fed_cats:
            log_event(tick_count, cat.name, f"{cat.name} ate bunny,hunger:{cat.hunger}->{cat.hunger+4}")
            cat.seeking = False
            cat.hunger += 4

        bunnies.update()
        bunnies.draw(screen)

        plants.update()
        plants.draw(screen)

        rocks.update()
        rocks.draw(screen)

        cats.update()
        cats.draw(screen)

        if first_tick:
            populate_world(rocks, screen, entity.Rock, 100, possible_spawn_points)
            populate_world(bunnies, screen, entity.Bunny, 200, possible_spawn_points)
            populate_world(plants, screen, entity.Grass, 450, possible_spawn_points)
            populate_world(cats, screen, entity.Cat, 50, possible_spawn_points)

            sort_by_gender(bunnies, female_bunnies, male_bunnies)
            sort_by_gender(cats, female_cats, male_cats)

            first_tick = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if exit_button.is_clicked(mouse_pos):
                running = False

            if not sim_started:
                if refresh_map_btn.is_clicked(mouse_pos):
                    new_map.generate_seed(x_size=GRID_WIDTH, y_size=GRID_HEIGHT, fill_percent=LAND_FILL_PERECENT)
                    first_tick = True

                if play_button.is_clicked(mouse_pos):
                    sim_started = True

            else:
                if refresh_map_btn.is_clicked(mouse_pos):
                    sim_started = False
                    cleanup_tasks()

    # draw buttons over other layers
    exit_button.draw(screen, math.floor(WIN_WIDTH * 0.96), math.floor(WIN_HEIGHT * 0.01))
    refresh_map_btn.draw(screen, math.floor(WIN_WIDTH * 0.01), math.floor(WIN_HEIGHT * 0.008))

    if not sim_started:
        play_button.draw(screen, (WIN_WIDTH // 2) - (play_button.width // 2), (WIN_HEIGHT // 2) - (play_button.height // 2))

    # screen.blit(roller.build_roller(), (500, 500))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()

json_obj = json.dumps(events, indent=4)

try:
    with open("event_log.json", "w+") as log_file:
        log_file.write(json_obj)
    print(f"wrote event log file: {len(events)} events")
except:
    print(f"{Exception}\nfailed to write logs")

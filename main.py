import pygame
import tile_map
import time
import math
from Input_Methods import button
from Entities import entity as ent
from images import sprites

MAP_WIDTH, MAP_HEIGHT = 2560, 1440
TILE_SIZE = 16
GRID_WIDTH = MAP_WIDTH // TILE_SIZE
GRID_HEIGHT = MAP_HEIGHT // TILE_SIZE

WIN_WIDTH, WIN_HEIGHT = (GRID_WIDTH * TILE_SIZE), (GRID_HEIGHT * TILE_SIZE)

LAND_FILL_PERECENT = 42

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

gui = pygame.sprite.Group()

running = True

new_map = tile_map.Tile_Code()


new_map.generate_seed(x_size=GRID_WIDTH, y_size=GRID_HEIGHT, fill_percent=LAND_FILL_PERECENT)
generate_map_btn = button.Button((204,204,204), 300, 150)

exit_button = button.Img_Button("images/exit_button.png", 70, 70)
refresh_map_btn = button.Img_Button("images/refresh_arrow.png", 100, 100)

new_ent = ent.Entity(WIN_WIDTH // 2, WIN_HEIGHT // 2, sprites.Rock_Sprite.sprites["rock"])
entities = pygame.sprite.Group()
entities.add(new_ent)


while running:

    # screen.fill("red")

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

    entities.update()
    entities.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()


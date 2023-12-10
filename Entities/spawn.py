import pygame
import random

class Spawn(pygame.sprite.Sprite):

    def spawn_random(surface:pygame.Surface, Entity, ent_img, spawn_color, spawn_count):

        width = surface.get_width()
        height = surface.get_height()

        ent_list = []

        while spawn_count > 0:
            x, y = random.randint(0, width-1), random.randint(0, height-1)
            color_at_point = surface.get_at((x,y))

            if (color_at_point == spawn_color):
                ent_list.append(Entity(x, y, ent_img))
                spawn_count -= 1

        return ent_list


import pygame
import random

class Spawn(pygame.sprite.Sprite):

    def spawn_random(surface:pygame.Surface, Entity, spawn_count, SP_list:list):

        # width = surface.get_width()
        # height = surface.get_height()

        ent_list = []

        while spawn_count > 0:

            random_point = SP_list.pop(random.randint(0, len(SP_list)))
            ent_list.append(Entity(random_point[0], random_point[1]))

            spawn_count -= 1


        # while spawn_count > 0:
        #     x, y = random.randint(16, width-15), random.randint(16, height-15)
        #     color_at_point = surface.get_at((x,y))

        #     if (color_at_point == spawn_color):
        #         ent_list.append(Entity(x, y))
        #         spawn_count -= 1

        return ent_list

    def spawn_near(surface:pygame.surface.Surface, parent_entity_cords:list, SP_list:list) -> list:
        
        rand_x, rand_y = random.randint((parent_entity_cords[0] - 30), (parent_entity_cords[0] + 30)), \
                         random.randint((parent_entity_cords[0] - 30), (parent_entity_cords[0] + 30))
        
        return [rand_x, rand_y]

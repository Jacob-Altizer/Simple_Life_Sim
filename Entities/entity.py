import pygame
import csv
import random
from images import sprites

entity_ids:list = []

class Entity(pygame.sprite.Sprite):

    def __init__(self, current_x:int, current_y:int, sprite_img:pygame.Surface) -> None:
        
        pygame.sprite.Sprite.__init__(self)

        self.ent_id = self.generate_id()
        self.current_x = current_x
        self.current_y = current_y
        self.image = sprite_img

        # self.image = pygame.Surface((4, 4))
        self.rect = self.image.get_rect()
        self.rect.center = (current_x, current_y)

        self.directions = ["up", "left", "right", "down"]


    def generate_id(self):

        with open("Entities/entity_ids.csv", "r") as f:
            reader = csv.reader(f)

            for row in reader:
                entity_ids.append(row)

        new_id = int(str(random.randint(0, 99999)).zfill(5))

        duplicates = 0
        for id in entity_ids:
            if id == new_id:
                duplicates += 1

        if duplicates == 0:
            entity_ids.append(new_id)

            with open("Entities/entity_ids.csv", "a", newline="") as file:
                writer = csv.writer(file)

                writer.writerow([new_id])

            return new_id
          

    def step(self, step_length, direction):
        
        match direction:
            case "up":
                self.current_y += step_length

            case "down":
                self.current_y -= step_length

            case "left":
                self.current_x -= step_length

            case "right":
                self.current_x += step_length

        self.update_position(self.current_x, self.current_y)
        

    def wander(self):
        # rand_step = random.randint(1, 5)
        rand_direction = random.choice(self.directions)

        self.step(5, rand_direction)

    def update_position(self, x, y):
        self.rect.center = (x, y)



class Rock(Entity):

    def __init__(self, current_x:int, current_y:int, sprite_img):
        super().__init__(current_x, current_y, sprite_img)


class Grass(Entity):
    def __init__(self, current_x:int, current_y:int, sprite_img):
        super().__init__(current_x, current_y, sprite_img)


class Bunny(Entity):
    def __init__(self, current_x:int, current_y:int, sprite_img):
        super().__init__(current_x, current_y, sprite_img)

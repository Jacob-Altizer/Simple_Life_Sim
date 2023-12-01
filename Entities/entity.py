import pygame
import csv
import random

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
          

class Rock(Entity):

    def __init__(self, current_x:int, current_y:int, sprite_img):
        super().__init__(current_x, current_y, sprite_img)


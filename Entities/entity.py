import pygame
import csv
import random, math
from images import sprites

entity_ids:list = []

class Entity(pygame.sprite.Sprite):

    def __init__(self, current_x:int, current_y:int, sprite_img:pygame.Surface, step_buffer, name) -> None:
        
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        # self.ent_id = self.generate_id()
        self.current_x = current_x
        self.current_y = current_y
        self.image = sprite_img
        self.view_radius = 50
        self.step_buffer = step_buffer
        self.seeking = False
        self.last_xs = []
        self.last_ys = []
        self.last_pos = []
        self.life_span: int
        self.hunger: int
        self.current_poi = [500,500]
        self.speed = 5

        self.hunger_drain = 0.08
        self.life_drain = 0.01

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



    def step(self, step_length, destination_point:list, surface:pygame.surface.Surface):
        Dx = destination_point[0]
        Dy = destination_point[1]

        # if surface.get_at((math.ceil(Dx), math.ceil(Dy))) != (28, 163, 236, 255):

        distance = math.sqrt((self.current_x - Dx) ** 2 + (self.current_y - Dy) ** 2)
    
        if distance != 0:
            self.current_x += (step_length * (Dx - self.current_x) / distance)
            self.current_y += (step_length * (Dy - self.current_y) / distance)

        self.update_position(self.current_x, self.current_y)



    def wander(self, surface:pygame.surface.Surface, range:list, avoid_color):
        range_x = range[0]
        range_y = range[1]

        rand_x, rand_y = random.randint((self.view_radius) * -1, self.view_radius), random.randint((self.view_radius) * -1, self.view_radius)

        if len(self.last_xs) > 5:
            self.last_xs = self.last_xs[-5:]
        if len(self.last_ys) > 5:
            self.last_ys = self.last_ys[-5:]

        self.last_xs.append(rand_x+self.current_x)
        self.last_ys.append(rand_y+self.current_y)

        self.current_poi = [self.average(self.last_xs), self.average(self.last_ys)]

        self.step(self.speed, self.current_poi, surface=surface)



    def average(self, list):
        return sum(list) / len(list)



    def update_position(self, x, y):
        self.rect.center = (x, y)



    def move_to_land(self, surface:pygame.surface.Surface, avoid_color):

        x_center = int(surface.get_width() // 2)
        y_center = int(surface.get_height() // 2)

        try:
            if surface.get_at((math.floor(self.current_x), math.floor(self.current_y))) == avoid_color:

                if self.current_x < x_center:
                    self.current_x += 10

                if self.current_y < y_center:
                    self.current_y += 10

                if self.current_x > x_center:
                    self.current_x -= 10

                if self.current_y > y_center:
                    self.current_y -= 10

        except(IndexError):
            pass



    def visualize_path(self, surface):
        pygame.draw.line(surface, "gray", (self.current_x, self.current_y), self.current_poi, 1)



    def seek(self, surface, Target) -> bool:
        Target_cords = [Target.current_x, Target.current_y]

        Dx = Target_cords[0]
        Dy = Target_cords[1]

        distance = math.floor(math.sqrt((self.current_x - Dx) ** 2 + (self.current_y - Dy) ** 2))

        if distance < self.view_radius:
            self.current_poi = Target_cords
            self.step(self.speed, (self.current_poi), surface=surface)

            self.seeking = True



    def reproduce(self, tick_threshold, current_tick, condition:bool = None) -> bool:

        if condition != None:
            if (current_tick >= tick_threshold) and (condition == True):
                return True
            
        elif (current_tick >= tick_threshold):
            return True
        
        else:
            return False



    def expire(self) -> bool:

        if self.life_span <= 0:
            return True
        
        if self.hunger <= 0:
            return True
        
        self.hunger -= self.hunger_drain
        self.life_span -= self.life_drain


class Rock(Entity):

    def __init__(self, current_x:int, current_y:int):
        super().__init__(current_x, current_y, sprites.Rock_Sprite.sprites["rock"], 0, "rock")


class Grass(Entity):
    def __init__(self, current_x:int, current_y:int):
        super().__init__(current_x, current_y, sprites.Plant_Sprite.sprites["long_grass"], 0, "long_grass")


class Bunny(Entity):
    def __init__(self, current_x:int, current_y:int):
        self.life_span = random.randint(7,8)
        self.hunger = random.randint(5,6)
        self.gender = random.randint(0,1) # 0 being male, 1 being female
        self.pregnant = 0 # 0 being not pregnant, being pregnant
        self.child_count = 0
        self.speed = 5
        self.view_radius = 50

        self.hunger_drain = 0.04
        self.life_drain = 0.008

        img = random.choice(("gray_bunny", "light_brown_bunny", "white_bunny", "dark_brown_bunny"))
        super().__init__(current_x, current_y, sprites.Bunny_Sprite.sprites["gray_bunny"], 5, "bunny")


class Cat(Entity):
    def __init__(self, current_x:int, current_y:int) -> None:
        self.life_span = random.randint(9,10)
        self.hunger = random.randint(4,5)
        self.gender = random.randint(0,1) # 0 being male, 1 being female
        self.pregnant = 0 # 0 being not pregnant, being pregnant
        self.child_count = 0
        self.speed = 7
        self.view_radius = 70

        self.hunger_drain = 0.06
        self.life_drain = 0.004
        
        super().__init__(current_x, current_y, sprites.Cat_Sprite.sprites["orange_cat"], 5, "cat")
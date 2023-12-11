import csv
import os
import random
import pygame
import math

class Tile_Code():



    def __init__(self):
        
        self.file_path = f"{os.getcwd()}/Tile_Map"
        self.tile_weights = self.read_weights()

    

    def smooth_map(self, seed: list):

        new_seed = []
        y = 1
        for y in range(len(seed)):
            new_row = []
            x = 1
            for x in range(len(seed[y])):

                water_count = 0

                #print(f"{seed[y][x]} @ X:{x} Y:{y}")
                
                try:
                    local_grid = [
                        seed[y-1][x],seed[y+1][x],seed[y][x-1],
                        seed[y][x+1],seed[y+1][x+1],seed[y+1][x-1],
                        seed[y-1][x+1],seed[y-1][x-1]
                    ]
                except:
                    new_row.append(-1)

                for value in local_grid:
                    if value == -1:
                        water_count += 1

                if water_count >= 5:
                    new_row.append(-1)
                else:
                    new_row.append(1)

                x += 1

            y += 1
            new_seed.append(new_row)
    
        return new_seed



    def get_surrounding_water_count(self, tile_x, tile_y, map):

        water_count = 0

        local_grid = [
            map[tile_y-1][tile_x], map[tile_y+1][tile_x], map[tile_y][tile_x-1], map[tile_y][tile_x+1], map[tile_y+1][tile_x+1], map[tile_y+1][tile_x-1], map[tile_y-1][tile_x+1], map[tile_y-1][tile_x-1]
            ]

        for value in local_grid:
            if value < 0:
                water_count += 1

        return water_count
    


    def read_weights(self):
        """ returns 2d list containing tile names and their associated weights """
        path = f"{self.file_path}/data/map_gen_weights.csv"

        tile_weights = [] # stores data read from file

        with open(path, 'r') as file:
            reader = csv.reader(file)
            next(reader, None) # ignores headers

            # appends lines read from map_gen_weights.csv to local list tile_weights
            for line in reader:
                tile_weights.append(line)

        weight_nums = [int(item) for item in tile_weights.pop(1)] # pops and converts string weights from tile_weights to int
        tile_weights.append(weight_nums) # adds converted list of data back to tile_weights

        return tile_weights



    def generate_seed(self, x_size:int, y_size:int, fill_percent:int):
        """creates 2d list that stores tile values to create a tile map with"""

        raw_map_code = []

        for y in range(y_size):
            new_row = []
            for x in range(x_size):
                if (x == 0 or x == x_size - 1) or (y == 0 or y == y_size - 1): # or (x == 1 or x == x_size - 2) or (y == 1 or y == y_size - 2)
                    new_row.append(-1)
                else:
                    result = 1 if random.randrange(0,100,1) < fill_percent else -1
                    new_row.append(result)

            raw_map_code.append(new_row)

        max_iterations = 8
        i = 0

        temp_seed = self.smooth_map(raw_map_code)

        while i < max_iterations:
            smoother_seed = temp_seed
            temp_seed = self.smooth_map(smoother_seed)

            i += 1


        self.save_map_seed("map_seed", smoother_seed)
    


    def save_map_seed(self, file_name: str, map_seed: list):
        """saves map seed list to csv file"""

        path = f"{self.file_path}/data"
        print(path + (f"{file_name}.csv"))
        
        with open(f"{path}/{file_name}.csv", 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerows(map_seed)



    def read_tile_map_seed(self, file_name):
        
        path = f"{self.file_path}/data"

        int_row: list = []

        seed: list = []

        with open(f"{path}/{file_name}.csv", 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                for value in row:
                    int_row.append(int(value))
                    

                seed.append(int_row)
                int_row = []

        return seed
    


    def draw_map(self, width, height, surface, tile_size):

        seed = self.read_tile_map_seed("map_seed")

        for row in range(height):
            for column in range(width):

                tile_index = seed[row][column]

                if tile_index > 0:
                    pygame.draw.rect(surface, (39,120,36), (column * tile_size, row * tile_size, tile_size, tile_size))
                if tile_index < 0:
                    pygame.draw.rect(surface, (28,163,236), (column * tile_size, row * tile_size, tile_size, tile_size))
            



if __name__ == '__main__':
    new_map = Tile_Code()
    seed = new_map.read_tile_map_seed("map_seed")

    print(new_map.get_surrounding_water_count(1,1,seed))

    for row in seed:
        print(row)

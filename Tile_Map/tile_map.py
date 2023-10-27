import csv
import os
import random

class Tile_Code():


    def __init__(self):
        
        self.file_path = f"{os.getcwd()}/Tile_Map"
        self.tile_weights = self.read_weights()


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


    def generate_tile_code(self, x_size:int, y_size:int):
        """creates 2d list that stores tile values to create a tile map with"""
        map_code = []

        for i in range(y_size):
            map_code.append(random.choices(self.tile_weights[0], self.tile_weights[1], k=x_size))

        return map_code
        

    def save_map_seed(self, file_name: str, map_seed: list):
        """saves map seed list to csv file"""

        path = f"{self.file_path}/data"
        print(path + (f"{file_name}.csv"))
        
        with open(f"{path}/{file_name}.csv", 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerows(map_seed)


new_tiles = Tile_Code()

map_seed = new_tiles.generate_tile_code(30, 30)
new_tiles.save_map_seed("map_seed", map_seed)
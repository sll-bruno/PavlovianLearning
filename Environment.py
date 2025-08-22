import numpy as np

grid_dict ={
    "Vazio": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3
}

class Environment:
    def __init__(self):
        self.grid = [[0 for i in range(24)] for j in range(24)]
        self.setup_boxes()
        self.food_pos = None 
        
    def setup_boxes(self):
        self.box1_coord = [(x,y) for x in range(12,24) for y in range(12)]
        self.box2_coord = [(x,y) for x in range(12) for y in range(12,24)]
        self.box3_coord = [(x,y) for x in range(12,24) for y in range(12,24)]

        for x,y in self.box1_coord:
            self.grid[x][y] = 1
        for x,y in self.box2_coord:
            self.grid[x][y] = 2
        for x,y in self.box3_coord:
            self.grid[x][y] = 3

    def show_grid(self):
        for row in self.grid:
            print(row)

    def get_region_of_coord(self, position):
        return self.grid[position[0]][position[1]]
    
    def is_valid_position(self, position):
        return 0 <= position[0] < 24 and 0 <= position[1] < 24

    def place_food(self, position):
        if self.is_valid_position(position):
            self.grid[position[0]][position[1]] = "F" 
            self.food_pos = position

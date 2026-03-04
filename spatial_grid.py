import settings as s
import math
import numpy as np

class SpatialGrid():
    
    def __init__(self, cell_size=100):
        self.cell_size = cell_size
        self.cols = math.ceil(s.WIDTH/cell_size)
        self.rows = math.ceil(s.HEIGHT/cell_size)

        self.grid = [[[] for _ in range(self.cols)] for _ in range(self.rows)]

    def _get_cell(self, x, y):
        col = int(x/self.cell_size)
        row = int(y/self.cell_size)

        col = max(0, min(col, self.cols - 1))
        row = max(0, min(row, self.rows - 1))

        return row, col

    def add_obstacles(self, obstacle):
        minx = obstacle.x - obstacle.w/2
        miny = obstacle.y - obstacle.h/2
        maxx = obstacle.x + obstacle.w/2
        maxy = obstacle.y + obstacle.h/2

        min_row, min_col = self._get_cell(minx, miny)
        max_row, max_col = self._get_cell(maxx, maxy)

        for i in range(min_row, max_row + 1):
            for j in range(min_col, max_col + 1):
                self.grid[i][j].append(obstacle)
                

    def get_nearby_obstacles(self):
        pass

    def rebuild(self):
        pass
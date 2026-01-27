import numpy as np
from creature import Creature, WIDTH, HEIGHT
from obstacle import Obstacle

c = Creature()
c.shape_orientation()
obstacles = [Obstacle(WIDTH/2, HEIGHT, 50,50)]

print(c.ray_edge_intersection(obstacles))
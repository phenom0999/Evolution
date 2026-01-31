import numpy as np
from numba import jit
import settings as s

def get_brain(file_name="best_brain.npy"):
    saved_brain = None
    try:
        saved_brain = np.load(f"saved_brains/{file_name}")
        print("Loaded saved brain! Evolution will resume from this checkpoint.")
    except FileNotFoundError:
        print("No saved brain found. Starting from scratch.")
    return saved_brain

def get_edge_position():
    r1 = np.random.uniform(0,1)
    r2 = np.random.uniform(0,1)
    if r1 < 0.5:
        if r2 < 0.5:
            return np.array([20, np.random.uniform(20, s.HEIGHT - 20)])
        else:
            return np.array([s.WIDTH - 20, np.random.uniform(20, s.HEIGHT - 20)])
    else:
        if r2 < 0.5:
            return np.array([np.random.uniform(20, s.WIDTH - 20), 20])
        else:
            return np.array([np.random.uniform(20, s.WIDTH - 20), s.HEIGHT - 20])


@jit(nopython=True)
def get_intersection(ray_start, ray_end, wall_start, wall_end):
    # This function is mathematically pure and doesn't depend on your game settings,
    # so it can stay exactly as it was!
    x1, y1 = ray_start[0], ray_start[1]
    x2, y2 = ray_end[0], ray_end[1]
    x3, y3 = wall_start[0], wall_start[1]
    x4, y4 = wall_end[0], wall_end[1]

    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    
    if denom == 0: 
        return None, None

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

    if 0 <= ua <= 1 and 0 <= ub <= 1:
        return np.empty(2), ua 

    return None, None

import numpy as np
from numba import jit # Import Numba

def get_brain():
    saved_brain = None
    try:
        saved_brain = np.load("best_brain.npy")
        print("Loaded saved brain! Evolution will resume from this checkpoint.")
    except FileNotFoundError:
        print("No saved brain found. Starting from scratch.")

    return saved_brain

# Add the @jit decorator
# nopython=True ensures it compiles to pure machine code
@jit(nopython=True) 
def get_intersection(ray_start, ray_end, wall_start, wall_end):
    x1, y1 = ray_start[0], ray_start[1] # Unpack manually for Numba safety
    x2, y2 = ray_end[0], ray_end[1]
    x3, y3 = wall_start[0], wall_start[1]
    x4, y4 = wall_end[0], wall_end[1]

    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    
    if denom == 0: 
        return None, None

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

    if 0 <= ua <= 1 and 0 <= ub <= 1:
        # Re-pack into array for return
        # return np.array([x1 + ua * (x2 - x1), y1 + ua * (y2 - y1)]), ua
        
        # Optimization: We only actually need 'ua' (distance fraction) 
        # for vision inputs. You can skip calculating the hit point 
        # if you aren't drawing the red dots where rays hit walls.
        return np.empty(2), ua 

    return None, None
import numpy as np
from numba import jit

def get_brain():
    saved_brain = None
    try:
        saved_brain = np.load("best_brain.npy")
        print("Loaded saved brain! Evolution will resume from this checkpoint.")
    except FileNotFoundError:
        print("No saved brain found. Starting from scratch.")
    return saved_brain

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

# --- Drawing Helper ---
def draw_creature(surface, creature, is_best=False):
    """Handles the visual representation of a creature."""
    color = s.COLOR_CREATURE
    if creature.target_reached: color = (50, 255, 50)
    elif creature.stop: color = (200, 50, 50)
    if is_best: color = s.COLOR_CREATURE_BEST

    # Rotate a triangle
    # (Simple trigonometry to draw a triangle pointing in velocity direction)
    angle = creature.angle
    center = pygame.math.Vector2(creature.position[0], creature.position[1])
    
    # Points of the triangle
    size = 12 if is_best else 8
    p1 = center + pygame.math.Vector2(size, 0).rotate_rad(angle)
    p2 = center + pygame.math.Vector2(-size/2, -size/2).rotate_rad(angle)
    p3 = center + pygame.math.Vector2(-size/2, size/2).rotate_rad(angle)
    
    pygame.draw.polygon(surface, color, [p1, p2, p3])
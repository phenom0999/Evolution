import numpy as np

def get_brain():
    saved_brain = None
    try:
        saved_brain = np.load("best_brain.npy")
        print("Loaded saved brain! Evolution will resume from this checkpoint.")
    except FileNotFoundError:
        print("No saved brain found. Starting from scratch.")

    return saved_brain

def get_intersection(p1, p2, p3, p4):
    """
    Calculates intersection between Line A (p1 to p2) and Line B (p3 to p4).
    p1, p2: Start and End points of the Ray (Creature's eye)
    p3, p4: Start and End points of the Wall (Obstacle)
    Returns: Distance to intersection (0.0 to 1.0) or None
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)

    # If denom is 0, lines are parallel
    if denom == 0:
        return None

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

    # Check if intersection is within the segments
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        return ua  # Return the fraction of the ray length (distance)

    return None
import numpy as np

def get_brain():
    saved_brain = None
    try:
        saved_brain = np.load("best_brain.npy")
        print("Loaded saved brain! Evolution will resume from this checkpoint.")
    except FileNotFoundError:
        print("No saved brain found. Starting from scratch.")

    return saved_brain
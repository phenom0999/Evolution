import pygame
import numpy as np
from creature import WIDTH, HEIGHT

class Obstacle:
    def __init__(self, x, y, w, h, random=False):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.random = random
        self.edges = []  # Store edges here
        self.rect = pygame.Rect(0, 0, self.w, self.h) # Store rect here
        self.update_edges() # Calculate once

    def update_edges(self):
        # Update rect first so draw() doesn't need to recreate it
        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.rect.center = (self.x, self.y)

        # Pre-calculate edges so we don't do it 4000 times a frame
        c1 = np.array([self.x - (self.w/2), self.y - (self.h/2)])
        c2 = np.array([self.x - (self.w/2), self.y + (self.h/2)])
        c3 = np.array([self.x + (self.w/2), self.y + (self.h/2)])
        c4 = np.array([self.x + (self.w/2), self.y - (self.h/2)])

        self.edges = [
            (c1, c2),
            (c2, c3),
            (c3, c4),
            (c4, c1)
        ]

    def random_position(self):
        if self.random:
            self.x = np.random.uniform(50, WIDTH - 50)
            self.y = np.random.uniform(50, HEIGHT - 50)
            self.w = np.random.uniform(10, 50)
            self.h = np.random.uniform(10, 50)
            self.update_edges() # Recalculate only when moving

    def get_edges(self):
        return self.edges

    def draw(self, surface):
        # Use the pre-calculated rect
        pygame.draw.rect(surface, (40, 40, 45), self.rect)
        pygame.draw.rect(surface, (100, 100, 110), self.rect, 2)


    def check_collision(self, creature):
        return self.rect.collidepoint(creature.position[0], creature.position[1])

    

        


    

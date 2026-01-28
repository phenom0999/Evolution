import pygame
import numpy as np
import settings as s  # Changed from 'from creature import WIDTH, HEIGHT'

class Obstacle:
    # Made x, y, w, h optional by giving them default values of 0
    def __init__(self, x=0, y=0, w=0, h=0, random=False):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.random = random
        self.edges = []
        
        # Initialize rect. If random=True, this will be overwritten immediately.
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        
        if self.random:
            self.random_position()
        else:
            self.update_edges()

    def update_edges(self):
        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.rect.center = (self.x, self.y)

        # Edges for raycasting
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
        # Using settings (s.WIDTH) instead of imported constant
        self.x = np.random.uniform(50, s.WIDTH - 50)
        self.y = np.random.uniform(50, s.HEIGHT - 50)
        self.w = np.random.uniform(10, 50)
        self.h = np.random.uniform(10, 50)
        self.update_edges()

    def get_edges(self):
        return self.edges

    def draw(self, surface):
        pygame.draw.rect(surface, s.COLOR_OBSTACLE, self.rect)
        pygame.draw.rect(surface, (100, 100, 110), self.rect, 2)

    def check_collision(self, creature):
        return self.rect.collidepoint(creature.position[0], creature.position[1])
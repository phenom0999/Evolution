import pygame
import numpy as np
from creature import WIDTH, HEIGHT

class Obstacle:
    def __init__(self, x, y, w, h, random=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.random = random

    def draw(self, surface):
        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.rect.center = (self.x, self.y)
        # Draw main body
        pygame.draw.rect(surface, (40, 40, 45), self.rect)
        # Draw minimalist border
        pygame.draw.rect(surface, (100, 100, 110), self.rect, 2)

    def check_collision(self, creature):
        return self.rect.collidepoint(creature.position[0], creature.position[1])
    
    def random_position(self):
        if self.random:
            self.x = np.random.uniform(50, WIDTH - 50)
            self.y = np.random.uniform(50, HEIGHT - 50)
            self.w = np.random.uniform(10, 50)
            self.h = np.random.uniform(10, 50)
        return

    

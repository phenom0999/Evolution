import pygame
import numpy as np
import math
import settings as s # Changed from 'from creature import WIDTH, HEIGHT'

class Target:
    def __init__(self, move=False, random=False, r=15):
        self.r = r
        self.position = np.array([s.WIDTH/2, s.HEIGHT/2])
        self.tx = 0
        self.ty = 100
        self.move = move
        self.random = random
    
    def move_target(self):
        if self.move:
            self.tx += 0.01
            self.ty += 0.013  

            vx = math.sin(self.tx)
            vy = math.cos(self.ty)

            target_velocity = np.array([vx, vy])
            
            # Boundary checks using settings
            if self.position[0] <= 0 or self.position[0] >= s.WIDTH:
                target_velocity[0] *= -1

            if self.position[1] <= 0 or self.position[1] >= s.HEIGHT:
                target_velocity[1] *= -1

            self.position += target_velocity

    def reset(self):
        if self.random: 
            self.position = np.array([np.random.uniform(30, s.WIDTH - 30), np.random.uniform(30, s.HEIGHT - 30)])
        else:
            self.position = np.array([s.WIDTH/2, s.HEIGHT/2])


    def draw(self, surface, count=0):
        # Draw Target
        # Optional: Add a simple glow effect using alpha surface if desired, 
        # but standard circle is fine for now.
        pygame.draw.circle(surface, s.COLOR_TARGET, self.position.astype(int), self.r)

    def check_collision(self, creature):
        dx = self.position[0] - creature.position[0]
        dy = self.position[1] - creature.position[1]
        distance_sq = dx*dx + dy*dy
        return distance_sq < (self.r * self.r)
import pygame
import numpy as np
import math
from creature import WIDTH, HEIGHT

class Target:
    def __init__(self, move=False, random=False, r=15):

        self.r = r
        self.position = np.array([np.random.uniform(30, WIDTH - 30), np.random.uniform(30, HEIGHT - 30)])
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
            if self.position[0] <= 0 or self.position[0] >= WIDTH:
                target_velocity[0] *= -1

            if self.position[1] <= 0 or self.position[1] >= HEIGHT:
                target_velocity[1] *= -1

            self.position += target_velocity

        return 
    
    def random_position(self):
        if self.random: 
            self.position = np.array([np.random.uniform(30, WIDTH - 30), np.random.uniform(30, HEIGHT - 30)])
        return

    def draw(self, overlay, screen, count):
        # Draw Target with Glow
        pygame.draw.circle(overlay, (255, 255, 0, 30), self.position, 30 + math.sin(count *0.1)*5)
        pygame.draw.circle(screen, (255, 200, 0), self.position, self.r)

    def check_collision(self, creature):
        # Calculate distance between circle center and creature
        dx = self.position[0] - creature.position[0]
        dy = self.position[1] - creature.position[1]
        
        # Check squared distance (faster than using sqrt)
        distance_sq = dx*dx + dy*dy
        
        # Collision if distance is less than radius
        return distance_sq < (self.r * self.r)
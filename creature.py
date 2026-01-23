import pygame
import random
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600
TARGET = pygame.math.Vector2(WIDTH/2, 40)
MUTATION_RATE = 0.01
t = 5 
dt = 0.25 
GENE_SIZE = int(t / dt) + 1
acc_limit = 0.6  # Reduced slightly for smoother steering

class Creature:
    def __init__(self):
        self.genes = [pygame.math.Vector2(random.uniform(-acc_limit, acc_limit), 
                                         random.uniform(-acc_limit, acc_limit)) for _ in range(GENE_SIZE)]
        self.position = pygame.math.Vector2(WIDTH/2, HEIGHT - 20)
        self.currentVelocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.stop = False
        self.target_reached = False
        self.color = (100, 100, 255)
        self.max_speed = 6
        self.history = [] # For visual trails
        self.history_size = 5

    def reset(self):
        """Resets the creature for a new generation while keeping genes."""
        self.position = pygame.math.Vector2(WIDTH/2, HEIGHT - 20)
        self.currentVelocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.stop = False
        self.target_reached = False
        self.history = []

    def fitness(self, current_gene_idx):
        dist = self.position.distance_to(TARGET)
        # Normalize fitness between 0 and 1
        fitness_val = np.interp(dist, [0, WIDTH], [1, 0])
        
        if self.target_reached:
            # Huge bonus for reaching target, scaled by how fast they got there
            time_bonus = np.interp(current_gene_idx, [0, GENE_SIZE], [2, 1])
            return (fitness_val + time_bonus) * 10
        
        if self.stop:
            return fitness_val * 0.1 # Penalty for hitting walls
            
        return fitness_val ** 4

    def move(self, gene_idx):
        if not self.stop:
            # Save history for trails
            self.history.append(pygame.math.Vector2(self.position))
            if len(self.history) > self.history_size:
                self.history.pop(0)

            # Physics engine
            self.acceleration = self.genes[gene_idx]
            self.currentVelocity += self.acceleration
            
            if self.currentVelocity.length() > self.max_speed:
                self.currentVelocity.scale_to_length(self.max_speed)
            
            self.position += self.currentVelocity

    def crossover(self, partner):
        child = Creature()
        midpoint = random.randint(0, GENE_SIZE)
        # Uniform Crossover for better genetic mixing
        for i in range(GENE_SIZE):
            child.genes[i] = self.genes[i] if random.random() > 0.5 else partner.genes[i]
        return child

    def mutate(self):
        for i in range(GENE_SIZE):
            if random.random() < MUTATION_RATE:
                self.genes[i] = pygame.math.Vector2(random.uniform(-acc_limit, acc_limit), 
                                                   random.uniform(-acc_limit, acc_limit))
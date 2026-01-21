import pygame
import random
import numpy as np

WIDTH, HEIGHT = 800, 600



TARGET = pygame.math.Vector2(WIDTH/2, 40)

MUTATION_RATE = 0.01

t = 5 # Time in seconds for each generation
dt = 0.25 # Time for new gene to be activated

GENE_SIZE = int(t / dt) + 1

acc = 1

class Creature:
    def __init__(self):
        self.genes = [pygame.math.Vector2(random.uniform(-acc, acc), random.uniform(-acc, acc)) for _ in range(GENE_SIZE)]
        self.position = pygame.math.Vector2(WIDTH/2, HEIGHT - 10)  # Start at center
        self.currentVelocity = pygame.math.Vector2(0, 0)
        self.stop = False
        self.color = (0,0,0)
        self.target_reached = False
        self.target_reached_idx = GENE_SIZE
        self.max_speed = 7

    def get_color(self):
        # color
        geneX = 0
        geneY = 0
        for gene in self.genes:
            geneX += gene.x
            geneY += gene.y
                
        green = np.interp(geneX, [-30, 30], [0,200])
        blue = np.interp(geneY, [-30, 30], [200,0])
        self.color = (0, green, blue, 255)
    
    def fitness(self, idx):
        distance = self.position.distance_to(TARGET)
        fitness_value = np.interp(distance, [0,WIDTH], [1,0])
        if self.target_reached:
            speed_fitness = np.interp(idx, [0, GENE_SIZE * 30], [1, 0.25])
            fitness_value = 20 * speed_fitness
        elif self.stop:
            fitness_value *= 0
        return fitness_value ** 5
    
    def crossover(self, partner):
        child = Creature()
        midpoint = random.randint(0, GENE_SIZE)
        for i in range(GENE_SIZE):
            if i < midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]
        return child


    def mutate(self):
        for i in range(GENE_SIZE):
            if random.random() < MUTATION_RATE:
                self.genes[i] = pygame.math.Vector2(random.uniform(-acc, acc), random.uniform(-acc, acc))


    def move(self, gene_idx):
        if not self.stop:
            # 1. Acceleration comes from the gene
            self.acceleration = self.genes[gene_idx] 
            
            # 2. Velocity accumulates acceleration
            self.currentVelocity += self.acceleration 
            
            # 3. Limit the speed (The most important part for smoothness!)
            if self.currentVelocity.length() > self.max_speed:
                self.currentVelocity.scale_to_length(self.max_speed)
                
            # 4. Position accumulates velocity
            self.position += self.currentVelocity

import pygame
import random
import numpy as np

WIDTH, HEIGHT = 800, 600



TARGET = pygame.math.Vector2(WIDTH/2, 40)

MUTATION_RATE = 0.01

t = 3 # Time in seconds for each generation
dt = 0.25 # Time for new gene to be activated

GENE_SIZE = int(t / dt) + 1

speed = 5

class Creature:
    def __init__(self):
        self.genes = [pygame.math.Vector2(random.uniform(-speed, speed), random.uniform(-speed, speed)) for _ in range(GENE_SIZE)]
        self.position = pygame.math.Vector2(WIDTH/2, HEIGHT - 10)  # Start at center
        self.currentVelocity = pygame.math.Vector2(0, 0)
        self.stop = False
        self.color = (0,0,0)

    def get_color(self):
        # color
        geneX = 0
        geneY = 0
        for gene in self.genes:
            geneX += gene.x
            geneY += gene.y
                
        green = np.interp(geneX, [-30, 30], [0,255])
        blue = np.interp(geneY, [-30, 30], [255,0])
        self.color = (0, green, blue, 50)
    
    def fitness(self):
        distance = self.position.distance_to(TARGET)
        fitness_value = np.interp(distance, [0,WIDTH], [1,0])
        if self.stop:
            fitness_value *= 0
        return fitness_value * fitness_value
    
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
                self.genes[i] = pygame.math.Vector2(random.uniform(-speed, speed), random.uniform(-speed, speed))



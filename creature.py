import pygame
import random
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600
#TARGET = np.array([WIDTH/2, 40])
#TARGET = np.array([np.random.uniform(30, WIDTH - 30), np.random.uniform(30, HEIGHT - 30)])
MUTATION_RATE = 0.001
ACC_LIMIT = 5  # Reduced slightly for smoother steering


class Creature:
    def __init__(self, hidden_size=4):

        self.input_size = 4
        self.hidden_size = hidden_size
        self.output_size = 2

        self.gene_size = ((self.input_size * self.hidden_size)
                            + (self.hidden_size)
                            + (self.hidden_size * self.output_size)
                            + (self.output_size))
        self.genes = np.random.uniform(-1, 1, self.gene_size) * 0.1
            
        self.position = np.array([WIDTH/2, HEIGHT - 20])
        self.velocity = np.array([0, 0], dtype=np.float64)
        self.acceleration = np.array([0, 0], dtype=np.float64)
        self.stop = False
        self.target_reached = False
        self.color = (100, 100, 255)
        self.max_speed = 2
        self.history = [] # For visual trails
        self.history_size = 5

    def reset(self):
        """Resets the creature for a new generation while keeping genes."""
        self.position = np.array([WIDTH/2, HEIGHT - 20])
        self.velocity = np.array([0, 0], dtype=np.float64)
        self.acceleration = np.array([0, 0], dtype=np.float64)
        self.stop = False
        self.target_reached = False
        self.history = []

    def fitness(self, count, target):
        dist = np.linalg.norm(self.position - target.position)
        # Normalize fitness between 0 and 1
        fitness_val = np.interp(dist, [0, WIDTH], [1, 0])
        
        if self.target_reached:
            return 1.5 + (1.0 / (count + 1)) # Bonus for speed if reached
        
        if self.stop:
            return fitness_val * 0.1 # Penalty for hitting walls
            
        return fitness_val ** 2
    
    
    def brain(self, target):

        # Separate weights and biases from genes
        Wih, Bih, Who, Bho = np.split(self.genes, [self.input_size * self.hidden_size, 
                                            self.input_size * self.hidden_size + self.hidden_size,
                                            (self.input_size * self.hidden_size) + self.hidden_size + (self.hidden_size * self.output_size)])

        # Prepare weight and bias matrices
        Wih = Wih.reshape(self.input_size, self.hidden_size)
        Bih = Bih.reshape(1,-1)
        Who = Who.reshape(self.hidden_size, self.output_size)
        Bho = Bho.reshape(1,-1)

        # Get inputs
        # Calculate relative vector to target
        rel_x = (target.position[0] - self.position[0]) / WIDTH
        rel_y = (target.position[1] - self.position[1]) / HEIGHT
        vel_x = self.velocity[0] / self.max_speed
        vel_y = self.velocity[1] / self.max_speed

        I = np.array([rel_x, rel_y, vel_x, vel_y]).reshape(1, -1)

        # Feed forward
        H = np.tanh(I @ Wih + Bih)
        O = np.tanh(H @ Who + Bho) * ACC_LIMIT

        # Return the acceleration vector
        return np.squeeze(O)


    def move(self, target):
        if not self.stop:

            # Physics engine
            self.acceleration = self.brain(target)
            self.velocity += self.acceleration
            
            if np.linalg.norm(self.velocity) > self.max_speed:
                self.velocity = self.velocity * (self.max_speed / np.linalg.norm(self.velocity))
            
            self.position += self.velocity

    def crossover(self, partner):
        child = Creature()
        # Uniform Crossover for better genetic mixing
        for i in range(self.gene_size):
            child.genes[i] = self.genes[i] if random.random() > 0.5 else partner.genes[i]
        return child

    def mutate(self):
        for i in range(self.gene_size):
            if random.random() < MUTATION_RATE:
                # Nudge the weight rather than replacing it
                self.genes[i] += np.random.normal(0, 1)

    def save_genes(self, filename="best_brain.npy"):
        np.save(filename, self.genes)
        print(f"Brain saved to {filename}")

    def load_genes(self, filename="best_brain.npy"):
        try:
            self.genes = np.load(filename)
            print(f"Brain loaded from {filename}")
            return True # Success
        except FileNotFoundError:
            print(f"No saved brain found at {filename}")
            return False # Failure

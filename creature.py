import pygame
import random
import numpy as np
import math
from helpers import get_intersection

# Constants
WIDTH, HEIGHT = 800, 600
#TARGET = np.array([WIDTH/2, 40])
#TARGET = np.array([np.random.uniform(30, WIDTH - 30), np.random.uniform(30, HEIGHT - 30)])
MUTATION_RATE = 0.001
ACC_LIMIT = 5  # Reduced slightly for smoother steering


class Creature:
    def __init__(self, hidden_size=4, saved_brain=None):
        self.num_rays = 4
        self.input_size = self.num_rays + 4
        self.hidden_size = hidden_size
        self.output_size = 2

        self.gene_size = ((self.input_size * self.hidden_size)
                            + (self.hidden_size)
                            + (self.hidden_size * self.output_size)
                            + (self.output_size))
        
        if saved_brain is not None:
            self.genes = saved_brain.copy() # Copy the saved genes
            self.mutate() # Mutate immediately so they aren't all identical clones
        else:
            self.genes = np.random.uniform(-1, 1, self.gene_size) * 0.1
            
        self.position = np.array([WIDTH/2, HEIGHT - 20])
        self.velocity = np.array([0, 0], dtype=np.float64)
        self.acceleration = np.array([0, 0], dtype=np.float64)
        self.stop = False
        self.target_reached = False
        self.color = (100, 100, 255)
        self.max_speed = 2
        self.angle = 0
        self.vision_inputs = [0] * self.num_rays

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
    
    
    def brain(self, target, obstacles):

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

        # Update Geometry BEFORE thinking
        if np.linalg.norm(self.velocity) > 0.1:
            self.angle = math.atan2(self.velocity[1], self.velocity[0])

        # Calculate eye position relative to current position
        eye_offset = pygame.math.Vector2(10, 0).rotate(math.degrees(self.angle))
        self.eye = self.position + np.array([eye_offset.x, eye_offset.y])

        # Get vision inputs
        self.vision_inputs = self.ray_edge_intersection(obstacles)

        # Prepare inputs
        input_list = [rel_x, rel_y, vel_x, vel_y] + self.vision_inputs
        I = np.array(input_list).reshape(1, -1)

        # Feed forward
        H = np.tanh(I @ Wih + Bih)
        O = np.tanh(H @ Who + Bho) * ACC_LIMIT

        # Return the acceleration vector
        return np.squeeze(O)


    def move(self, target, obstacles):
        if not self.stop:

            # Physics engine
            self.acceleration = self.brain(target, obstacles)
            self.velocity += self.acceleration
            
            if np.linalg.norm(self.velocity) > self.max_speed:
                self.velocity = self.velocity * (self.max_speed / np.linalg.norm(self.velocity))
            
            self.position += self.velocity

    def crossover(self, partner):
        child = Creature(hidden_size=self.hidden_size)
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
        
    def shape_orientation(self, surface=None, is_best=False, draw=False):

        # Calculate orientation
        self.angle = 0
        if np.linalg.norm(self.velocity) > 0:
            self.angle = math.atan2(self.velocity[1], self.velocity[0])
        
        # Draw Triangle (pointing toward velocity)
        size = 10 if not is_best else 14
        self.eye = self.position + pygame.math.Vector2(size, 0).rotate(math.degrees(self.angle))
        self.p2 = self.position + pygame.math.Vector2(-size/2, -size/2).rotate(math.degrees(self.angle))
        self.p3 = self.position + pygame.math.Vector2(-size/2, size/2).rotate(math.degrees(self.angle))
        
        color = (0, 200, 255)
        if self.target_reached: color = (50, 255, 50)
        if self.stop and not self.target_reached: color = (200, 50, 50)
        if is_best: color = (255, 255, 0)

        if draw:
            pygame.draw.polygon(surface, color, [self.eye, self.p2, self.p3])

        return

    def vision(self, surface=None, FOV=60, range=60, show_FOV=False):
        """" Ray Casting
         FOV in degrees, range in pixels """

        num_rays = self.num_rays
        eye = self.eye # get the position of eye
        rays = []

        # rotate the rays
        for offset in np.linspace(-FOV/2, FOV/2, num_rays):
            offset_rad = math.radians(offset)
            direction = pygame.math.Vector2(1, 0).rotate_rad(self.angle + offset_rad)
            rays.append(eye + direction * range)

        if show_FOV:
            for ray in rays:
                pygame.draw.line(surface, (255, 255, 0), eye, ray)

        return rays
    
    def ray_edge_intersection(self, obstacles):

        ray_ends = self.vision()
        self.vision_inputs = []

        for ray_end in ray_ends:
            closest_dist = 1.0 # Default: 1.0 means "Max Distance / Saw Nothing"
            
            # Check THIS ray against EVERY wall of EVERY obstacle
            for obs in obstacles:
                edges = obs.get_edges() # Get the 4 walls
                for edge in edges:
                    wall_start, wall_end = edge[0], edge[1]
                    
                    _, dist_fraction = get_intersection(
                        self.eye, ray_end, wall_start, wall_end
                    )
                    
                    if dist_fraction is not None:
                        # We want the CLOSEST hit for this specific ray
                        if dist_fraction < closest_dist:
                            closest_dist = dist_fraction
            
            # Invert so 1.0 = Wall is touching me, 0.0 = No wall seen
            self.vision_inputs.append(1.0 - closest_dist)

        return self.vision_inputs

            

import numpy as np
import math
import random
from helpers import get_intersection, get_edge_position
import settings as s 

class Creature:
    def __init__(self, saved_brain=None):
        # 1. Properties
        self.position = get_edge_position()
        self.velocity = np.zeros(2)
        self.acceleration = np.zeros(2)
        self.angle = 0
        
        # 2. State
        self.stop = False
        self.target_reached = False
        
        # 3. Brain Structure
        self.num_rays = s.NUM_RAYS
        self.input_size = self.num_rays + 4 # 4 for rel_x, rel_y, vel_x, vel_y
        self.hidden_size = s.HIDDEN_SIZE
        self.output_size = 2
        
        # Calculate total genes needed
        self.gene_size = ((self.input_size * self.hidden_size) + self.hidden_size + 
                          (self.hidden_size * self.output_size) + self.output_size)

        # 4. Genetics
        if saved_brain is not None:
            self.genes = saved_brain.copy()
            self.mutate()
        else:
            self.genes = np.random.uniform(-1, 1, self.gene_size) * 0.1

    def get_vision(self, obstacles):
        """Calculates distances to obstacles using raycasting."""
        eye_offset = np.array([math.cos(self.angle), math.sin(self.angle)]) * 10
        eye_pos = self.position + eye_offset
        
        vision_readings = []
        
        # Calculate ray directions
        # We use linspace to get angles from -FOV/2 to +FOV/2 relative to current angle
        ray_angles = np.linspace(-s.FOV/2, s.FOV/2, self.num_rays)
        
        for deg in ray_angles:
            rad = self.angle + math.radians(deg)
            ray_dir = np.array([math.cos(rad), math.sin(rad)])
            ray_end = eye_pos + (ray_dir * s.VIEW_RANGE)
            
            closest_dist = 1.0 # default (saw nothing)
            
            # Check intersection with all obstacles
            for obs in obstacles:
                for edge in obs.edges:
                    _, dist_fraction = get_intersection(eye_pos, ray_end, edge[0], edge[1])
                    if dist_fraction is not None and dist_fraction < closest_dist:
                        closest_dist = dist_fraction
            
            # Invert: 1.0 means CLOSE (danger), 0.0 means FAR (safe)
            vision_readings.append(1.0 - closest_dist)
            
        return vision_readings

    def think(self, target, obstacles):
        """Neural Network Feed Forward."""
        if self.stop: return

        # 1. Inputs
        rel_pos = (target.position - self.position) / [s.WIDTH, s.HEIGHT]
        norm_vel = self.velocity / s.MAX_SPEED
        vision = self.get_vision(obstacles)
        
        inputs = np.concatenate([rel_pos, norm_vel, vision])
        
        # 2. Extract Weights/Biases (reshaping logic)
        end_ih = self.input_size * self.hidden_size
        end_bih = end_ih + self.hidden_size
        end_ho = end_bih + (self.hidden_size * self.output_size)
        
        Wih = self.genes[0:end_ih].reshape(self.input_size, self.hidden_size)
        Bih = self.genes[end_ih:end_bih]
        Who = self.genes[end_bih:end_ho].reshape(self.hidden_size, self.output_size)
        Bho = self.genes[end_ho:]
        
        # 3. Process
        hidden = np.tanh(np.dot(inputs, Wih) + Bih)
        output = np.tanh(np.dot(hidden, Who) + Bho)
        
        # 4. Set Acceleration
        self.acceleration = output * s.ACC_LIMIT

    def update(self):
        """Physics Update."""
        if self.stop: return

        self.velocity += self.acceleration
        
        # Limit speed
        speed = np.linalg.norm(self.velocity)
        if speed > s.MAX_SPEED:
            self.velocity = (self.velocity / speed) * s.MAX_SPEED
            
        self.position += self.velocity
        
        # Update angle only if moving
        if speed > 0.1:
            self.angle = math.atan2(self.velocity[1], self.velocity[0])
            
        # Boundary Check
        if not (0 < self.position[0] < s.WIDTH and 0 < self.position[1] < s.HEIGHT):
            self.stop = True

    def calculate_fitness(self, target):
        dist = np.linalg.norm(self.position - target.position)
        score = np.interp(dist, [0, s.WIDTH], [1, 0])
        
        if self.target_reached:
            return 1.5 # Bonus
        if self.stop:
            return score * 0.1 # Penalty
            
        return score ** 2

    # Genetics Methods
    def crossover(self, partner):
        child = Creature(saved_brain=None)
        # Randomly select genes from self or partner
        mask = np.random.rand(self.gene_size) > 0.5
        child.genes = np.where(mask, self.genes, partner.genes)
        return child

    def mutate(self):
        # Vectorized mutation is faster than a for-loop
        mutation_mask = np.random.rand(self.gene_size) < s.MUTATION_RATE
        changes = np.random.normal(0, 1, size=self.gene_size)
        self.genes[mutation_mask] += changes[mutation_mask]
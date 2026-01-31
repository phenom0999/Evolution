import numpy as np
import random
import settings as s
from entity.creature import Creature

class Population:
    def __init__(self, saved_brain=None):
        self.creatures = [Creature(saved_brain) for _ in range(s.POPULATION_SIZE)]
        self.generation = 0
        self.best_creature = None

    def update(self, target, obstacles):
        """Runs the physics/logic for all creatures."""
        active_count = 0
        for creature in self.creatures:
            if not creature.stop:
                creature.think(target, obstacles)
                creature.update()
                
                # Check collisions (Logic moved here or kept in main, 
                # but better to have the population manage its own state)
                if target.check_collision(creature):
                    creature.stop = True
                    creature.target_reached = True
                
                for obs in obstacles:
                    if obs.check_collision(creature):
                        creature.stop = True

                active_count += 1
        return active_count

    def evaluate(self, target):
        """Calculates fitness and creates the next generation."""
        # 1. Calculate fitness
        fitness_scores = [c.calculate_fitness(target) for c in self.creatures]
        
        # 2. Find best
        max_fitness = max(fitness_scores)
        best_idx = fitness_scores.index(max_fitness)
        self.best_creature = self.creatures[best_idx]
        
        # 3. Selection Pool (Weighted probability)
        # Add epsilon to avoid division by zero
        probs = np.array(fitness_scores) + 1e-8
        probs /= probs.sum()
        
        # 4. Create New Generation
        new_creatures = []
        
        # Elitism: Keep the champion?
        if s.ELITISM:
            champion = Creature()
            champion.genes = self.best_creature.genes.copy()
            new_creatures.append(champion)
            self.best_creature = champion
            
        # Fill the rest
        while len(new_creatures) < s.POPULATION_SIZE:
            # Pick two parents based on fitness probability
            parent_a, parent_b = np.random.choice(self.creatures, size=2, p=probs)
            
            child = parent_a.crossover(parent_b)
            child.mutate()
            new_creatures.append(child)
            
        self.creatures = new_creatures
        self.generation += 1

    def start_generation_from(self, start_gen):
        self.generation = start_gen
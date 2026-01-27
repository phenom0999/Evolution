from creature import Creature, WIDTH, HEIGHT
from obstacle import Obstacle
from target import Target
from helpers import get_brain
import random
import pygame
import math
import numpy as np


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 22)

# Before the loop
overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Config
saved_brain = None
load_brain = True
if load_brain: saved_brain = get_brain()

population_size = 100
population = [Creature(saved_brain=saved_brain, hidden_size=10) for _ in range(population_size)]
obstacles_num = 15
obstacle_size = 75
obstacles = [Obstacle  (np.random.uniform(50, WIDTH - obstacle_size),
                        np.random.uniform(50, HEIGHT - obstacle_size),
                        np.random.uniform(10, obstacle_size),
                        np.random.uniform(10, obstacle_size),
                        random=True)
                        for _ in range(obstacles_num)]
target = Target(move=False, random=True)

generation = 0
gene_idx = 0
count = 0
best_creature = None
show_only_best = False


FRAMES = 500
FPS = 90



running = True
while running:
    # Use a surface that supports transparency for trails
    overlay.fill((0,0,0,0))
    screen.fill((15, 15, 20)) # Deep space blue/black

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        # NEW: Key handler
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if best_creature:
                    best_creature.save_genes()
                else:
                    # If generation 0 and no best defined yet, save the first one or handle error
                    population[0].save_genes()
    
    keys = pygame.key.get_pressed()
    show_only_best = keys[pygame.K_SPACE]

    # Generation Reset Logic
    if count >= FRAMES or len([c for c in population if c.stop]) == population_size:
        
        # Calculate Fitness and Selection
        weights = [c.fitness(count, target) + 1e-8 for c in population]
        current_best_idx = weights.index(max(weights))
        best_creature = population[current_best_idx]
        new_pop = []
        # Elitism
        elite = best_creature
        elite.reset()
        new_pop.append(elite)

        while len(new_pop) < population_size:
            parents = random.choices(population, weights=weights, k=2)
            child = parents[0].crossover(parents[1])
            child.mutate()
            new_pop.append(child)
        
        population = new_pop

        # Random target position
        target.random_position()

        # Random obstacle position 
        for obs in obstacles: obs.random_position()

        gene_idx = 0
        count = 0
        generation += 1

        continue
    
    # move target
    target.move_target()

    # draw target
    target.draw(overlay, screen, count)

    # draw obstacles
    for obs in obstacles: obs.draw(screen)

    for c in population:
        if not c.stop:

            # Check collision with obstacle
            for obs in obstacles:
                if obs.check_collision(c): c.stop = True
            
            # Check collision with target
            if target.check_collision(c):
                c.stop = True
                c.target_reached = True
                
            # Boundary checks
            if not (0 < c.position[0] < WIDTH and 0 < c.position[1] < HEIGHT):
                c.stop = True

            c.move(target, obstacles)

        if show_only_best:
            if c == best_creature: c.shape_orientation(surface=overlay, is_best=True, draw=True)
        else:
            c.shape_orientation(surface=overlay, is_best=c == best_creature, draw=True)
            #c.vision(surface=overlay, show_FOV=True)

    screen.blit(overlay, (0,0))
    
    # UI
    ui_color = (200, 200, 200)
    screen.blit(font.render(f"Generation: {generation}", True, ui_color), (20, 20))

    success_count = len([c for c in population if c.target_reached])
    screen.blit(font.render(f"Success rate: {success_count}/{len(population)}", True, ui_color), (20, 50))
    
    pygame.display.flip()
    count += 1

    clock.tick(FPS)  

pygame.quit()
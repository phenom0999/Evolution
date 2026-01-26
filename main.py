from creature import Creature, WIDTH, HEIGHT
from obstacle import Obstacle
from target import Target
import random
import pygame
import math
import numpy as np

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 22)

# Config
population_size = 500
population = [Creature() for _ in range(population_size)]
load_brain = True
obstacles_num = 10
obstacles = [Obstacle  (np.random.uniform(30, WIDTH - 30),
                        np.random.uniform(30, HEIGHT - 30),
                        np.random.uniform(20, 50))
                        for _ in range(obstacles_num)]
target = Target(move=True)

# get brain if load_brain
if load_brain:
    saved_brain = None
    try:
        saved_brain = np.load("best_brain.npy")
        print("Loaded saved brain! Evolution will resume from this checkpoint.")
    except FileNotFoundError:
        print("No saved brain found. Starting from scratch.")

    for c in population:
        if saved_brain is not None:
            c.genes = saved_brain.copy() # Copy the saved genes
            c.mutate() # Mutate immediately so they aren't all identical clones
    


generation = 0
gene_idx = 0
count = 0
best_creature = None
show_only_best = False


FRAMES = 500


def draw_creature(surface, creature, is_best=False):
    if len(creature.history) > 1:
        # Draw Trail
        points = list(creature.history)
        if len(points) >= 2:
            color = (0, 255, 255, 50) if not is_best else (255, 255, 0, 150)
            pygame.draw.lines(surface, color, False, points, 1 if not is_best else 2)

    # Calculate orientation
    angle = 0
    if np.linalg.norm(creature.velocity) > 0:
        angle = math.atan2(creature.velocity[1], creature.velocity[0])
    
    # Draw Triangle (pointing toward velocity)
    size = 10 if not is_best else 14
    p1 = creature.position + pygame.math.Vector2(size, 0).rotate(math.degrees(angle))
    p2 = creature.position + pygame.math.Vector2(-size/2, -size/2).rotate(math.degrees(angle))
    p3 = creature.position + pygame.math.Vector2(-size/2, size/2).rotate(math.degrees(angle))
    
    color = (0, 200, 255)
    if creature.target_reached: color = (50, 255, 50)
    if creature.stop and not creature.target_reached: color = (200, 50, 50)
    if is_best: color = (255, 255, 0)

    pygame.draw.polygon(surface, color, [p1, p2, p3])


running = True
while running:
    # Use a surface that supports transparency for trails
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
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
    if count >= FRAMES:
        
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

        gene_idx = 0
        count = 0
        generation += 1

        continue
    
    # move target
    target.move_target()

    # draw target
    target.draw(overlay, screen, count)


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

            c.move(target)

        if show_only_best:
            if c == best_creature: draw_creature(overlay, c, True)
        else:
            draw_creature(overlay, c, c == best_creature)

    screen.blit(overlay, (0,0))
    
    # UI
    ui_color = (200, 200, 200)
    screen.blit(font.render(f"Generation: {generation}", True, ui_color), (20, 20))

    success_count = len([c for c in population if c.target_reached])
    screen.blit(font.render(f"Success rate: {success_count}/{len(population)}", True, ui_color), (20, 50))
    
    pygame.display.flip()
    count += 1

pygame.quit()
from creature import Creature
import random
import pygame

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
target = pygame.math.Vector2(WIDTH, HEIGHT)
populationSize = 5
mutation_rate = 0.01
elitism = False

population = [Creature() for _ in range(populationSize)]  # Fixed initialization
bestCreature = None
bestScore = 0

for generation in range(100):
    # Reset each creature's state before simulation
    for p in population:
        p.reset()

    # Simulate without interactive wind
    simulateCreature(population, WIDTH, HEIGHT, interactive=False)

    # Evaluate fitness
    current_max = -1
    totalFitness = 0
    current_best = None

    for p in population:
        fitness = p.calculateFitness(target)
        totalFitness += fitness
        if fitness > current_max:
            current_max = fitness
            current_best = p

    if current_max > bestScore:
        bestScore = current_max
        bestCreature = current_best

    if bestScore >= 1.0:  # Example threshold
        print("Solution found!")
        break

    # Create new population
    matingPool = []
    if totalFitness > 0:
        for p in population:
            n = int((p.fitness / totalFitness) * populationSize)
            matingPool.extend([p] * n)
    else:
        matingPool = population.copy()

    new_population = []
    if elitism and bestCreature:
        new_population.append(bestCreature)

    while len(new_population) < populationSize:
        parentA = random.choice(matingPool)
        parentB = random.choice(matingPool)
        child = parentA.crossover(parentB)
        child.mutate()
        new_population.append(child)

    population = new_population[:populationSize]

pygame.quit()
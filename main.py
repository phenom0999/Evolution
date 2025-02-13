from creature import Creature, WIDTH, HEIGHT, GENE_SIZE, TARGET, dt
import random
import pygame


# Initialize Pygame
pygame.init()

pygame.display.set_caption("Genetic Algorithm")


populationSize = 500

population = [Creature() for _ in range(populationSize)]  # Fixed initialization

screen = pygame.display.set_mode((800, 600))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (200, 200, 100)
BROWN = (150, 150, 150)
font = pygame.font.Font(None, 30)


bestCreature = None
bestFitness = 0
elitism = True

count = 0
generation = 0
n_success_creatures = 0
max_success = 0

gene_idx = 0

# Create a clock object
clock = pygame.time.Clock()

FPS = 30 

df = int(FPS * dt) # Frames for new gene to be activated


obstacle_width = 350
obstacle_height = 20
obstacle_x = WIDTH/2
obstacle_y = HEIGHT/2
OBSTACLE = pygame.math.Vector2(obstacle_x, obstacle_y)

target_width = 60
target_height = 40


running = True
while running:

    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close button clicked
            running = False

    # activate next gene
    if count % df == 0:
        gene_idx += 1

    # generation stops if gene_idx is out of index
    if gene_idx >= GENE_SIZE:

        # do everything here

        # create mating pool
        mating_pool = []
        for creature in population:
            fitness = creature.fitness()
            n = [creature] * (int(fitness * 100))
            mating_pool += n

            # also update the bestFitness
            if fitness > bestFitness:
                bestFitness = fitness
                bestCreature = creature
    
        
        new_population = []
        if elitism and bestCreature:
            bestCreature.position = pygame.math.Vector2(WIDTH/2, HEIGHT - 10)
            new_population.append(bestCreature)
        while len(new_population) < populationSize:
            parentA = random.choice(mating_pool)
            parentB = random.choice(mating_pool)
            child = parentA.crossover(parentB)
            child.mutate()
            new_population.append(child)

        population = new_population[:populationSize]

        max_success = max(max_success, n_success_creatures) # update max successful creature count

        # reset count
        count = 0
        gene_idx = 0
        n_success_creatures = 0
        generation += 1
        
        continue

    # Draw target
    rect_target = pygame.Rect(0, 0, target_width, target_height)
    rect_target.center = TARGET  # Set center directly

    # Draw obstacle
    rect_obs = pygame.Rect(0, 0, obstacle_width, obstacle_height)
    rect_obs.center = OBSTACLE

    pygame.draw.rect(screen, YELLOW, rect_target)
    pygame.draw.rect(screen, BROWN, rect_obs)

    
    for creature in population:
        if creature.stop and not creature.target_reached:
            creature.color = (150, 0, 0)
        else:
            creature.get_color()
        pygame.draw.circle(screen, creature.color, creature.position, 10)

        # Check to see if the creature has collided with the obstacle
        if (obstacle_x - obstacle_width/2 <= creature.position.x <= obstacle_x + obstacle_width/2 and
    obstacle_y - obstacle_height/2 <= creature.position.y <= obstacle_y + obstacle_height/2):
            creature.stop = True
        # Check to see if the creature has reached the target
        elif (WIDTH/2 - target_width/2 <= creature.position.x <= WIDTH/2 + target_width/2 and
    40 - target_height/2 <= creature.position.y <= 40 + target_height/2):
            if not creature.target_reached:
                n_success_creatures += 1
            creature.stop = True
            creature.target_reached = True

        else:
            creature.position += creature.genes[gene_idx]
        
    

    count += 1

    # Display Generation Count
    gen_text = font.render(f"Gen: {generation}", True, WHITE)
    text_rect = gen_text.get_rect(center=(50, 40))
    screen.blit(gen_text, text_rect)  # Draw text

    success_text = font.render(f"N Success: {max_success}", True, WHITE)
    text_rect = gen_text.get_rect(center=(50, 80))
    screen.blit(success_text, text_rect)  # Draw text
    pygame.display.update()  # Update the screen


    # Limit frame rate
    clock.tick(FPS)  # This makes sure the game runs at 60 FPS



pygame.quit()
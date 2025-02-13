from creature import Creature, WIDTH, HEIGHT, GENE_SIZE, TARGET, dt
import random
import pygame
from obstacle import Obstacle


# Initialize Pygame
pygame.init()

pygame.display.set_caption("Genetic Algorithm")


populationSize = 10000

population = [Creature() for _ in range(populationSize)]  # Fixed initialization

screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (200, 200, 100)
BROWN = (150, 150, 150)
font = pygame.font.Font(None, 30)


bestCreature = population[0] 
bestFitness = 0
elitism = True

count = 0
generation = 0
n_success_creatures = 0
max_success_rate = 0

total_fitness = 0
mating_pool_size = populationSize * 100

gene_idx = 0

# Create a clock object
clock = pygame.time.Clock()

FPS = 30 

df = int(FPS * dt) # Frames for new gene to be activated


target_width = 60
target_height = 40

# create two obstacles
obs1 = Obstacle(WIDTH - 200, HEIGHT/4, 400, 20)
obs2 = Obstacle(250, HEIGHT/2, 500, 20)
obs3 = Obstacle(WIDTH - 200, 3 * HEIGHT/ 4, 500, 20)

show_best_creature = False


running = True
while running:

    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close button clicked
            running = False
        
    # Check if SPACE key is held down
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        show_best_creature = True
    else:
        show_best_creature = False

    # activate next gene
    if count % df == 0:
        gene_idx += 1

    # generation stops if gene_idx is out of index
    if gene_idx >= GENE_SIZE:

        # do everything here

        # create mating pool
        mating_pool = []

        for creature in population:
            fitness = creature.fitness(count)
            total_fitness += fitness

        mating_pool_rate = mating_pool_size / total_fitness
        print(mating_pool_rate, total_fitness, bestFitness)

        for creature in population:
            fitness = creature.fitness(count)
            n = [creature] * (int(fitness * mating_pool_rate))
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

        max_success_rate = max(max_success_rate, int((n_success_creatures / populationSize) * 100)) # update max successful creature count

        # reset count
        count = 0
        gene_idx = 0
        n_success_creatures = 0
        total_fitness = 0
        generation += 1
        
        continue

    # Draw target
    rect_target = pygame.Rect(0, 0, target_width, target_height)
    rect_target.center = TARGET  # Set center directly

    # Draw obstacles
    obs1.draw(screen, BROWN)
    obs2.draw(screen, BROWN)
    obs3.draw(screen, BROWN)
    pygame.draw.rect(screen, YELLOW, rect_target)

    
    for creature in population:
        if creature.stop and not creature.target_reached:
            creature.color = (150, 0, 0)
        else:
            creature.get_color()

        if not show_best_creature or creature == bestCreature:
                pygame.draw.circle(screen, creature.color, creature.position, 10)


        # Check to see if the creature has collided with the obstacle
        if obs1.check_collision(creature) or obs2.check_collision(creature) or obs3.check_collision(creature):
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

    success_text = font.render(f"Max success rate: {max_success_rate}%", True, WHITE)
    text_rect = gen_text.get_rect(center=(50, 80))
    screen.blit(success_text, text_rect)  # Draw text
    pygame.display.update()  # Update the screen



    # Limit frame rate
    clock.tick(FPS)  # This makes sure the game runs at 60 FPS



pygame.quit()
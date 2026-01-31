import pygame
import settings as s
from population import Population
from obstacle import Obstacle
from target import Target
from helpers import get_brain
import numpy as np

# --- Drawing Helper ---
def draw_creature(surface, creature, is_best=False):
    """Handles the visual representation of a creature."""
    color = s.COLOR_CREATURE
    if creature.target_reached: color = (50, 255, 50)
    elif creature.stop: color = (200, 50, 50)
    if is_best: color = s.COLOR_CREATURE_BEST

    # Rotate a triangle
    # (Simple trigonometry to draw a triangle pointing in velocity direction)
    angle = creature.angle
    center = pygame.math.Vector2(creature.position[0], creature.position[1])
    
    # Points of the triangle
    size = 12 if is_best else 8
    p1 = center + pygame.math.Vector2(size, 0).rotate_rad(angle)
    p2 = center + pygame.math.Vector2(-size/2, -size/2).rotate_rad(angle)
    p3 = center + pygame.math.Vector2(-size/2, size/2).rotate_rad(angle)
    
    pygame.draw.polygon(surface, color, [p1, p2, p3])


# --- Main Application ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 18)

    # Setup
    saved_genes = get_brain("new_brain.npy") # Ensure helpers.py is updated to use exception handling safely
    pop = Population(saved_brain=saved_genes)
    
    # Init Environment
    obstacles = [Obstacle(random=True) for _ in range(15)] # Update Obstacle to use kwargs if preferred
    target = Target(move=True, random=False)

    frame_count = 0
    running = True

    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and pop.best_creature:
                    np.save("saved_brains/best_brain.npy", pop.best_creature.genes)
                    print("Brain Saved.")
        
        # show only best when space is pressed
        keys = pygame.key.get_pressed()
        show_only_best = keys[pygame.K_SPACE]

        # 2. Logic Updates
        active_creatures = pop.update(target, obstacles)
        target.move_target()

        # Check End of Generation
        all_dead = active_creatures == 0
        time_up = frame_count >= s.GENERATION_FRAMES
        
        if all_dead or time_up:
            print(f"Generation {pop.generation} Complete. Evolving...")
            pop.evaluate(target)
            
            # Reset Environment
            target.reset()
            for obs in obstacles: obs.random_position()
            frame_count = 0

        # 3. Rendering
        screen.fill(s.COLOR_BG)
        
        # Draw Target & Obstacles
        target.draw(screen, frame_count) # Pass screen, not overlay, for simplicity
        for obs in obstacles: 
            obs.draw(screen)

        # Draw Creatures
        keys = pygame.key.get_pressed()
        show_best_only = keys[pygame.K_SPACE]

        for creature in pop.creatures:
            is_best = (creature == pop.best_creature)
            if show_best_only and not is_best:
                continue
            draw_creature(screen, creature, is_best)

        # UI
        success_num = len([c for c in pop.creatures if c.target_reached])
        info = font.render(f"Gen: {pop.generation} | Success Rate: {success_num}/{s.POPULATION_SIZE}", True, (200, 200, 200))
        screen.blit(info, (10, 10))

        pygame.display.flip()
        clock.tick(s.FPS)
        frame_count += 1

    pygame.quit()

if __name__ == "__main__":
    main()
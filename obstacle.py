import pygame

class Obstacle:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (x, y)

    def draw(self, surface):
        # Draw main body
        pygame.draw.rect(surface, (40, 40, 45), self.rect)
        # Draw minimalist border
        pygame.draw.rect(surface, (100, 100, 110), self.rect, 2)

    def check_collision(self, creature):
        return self.rect.collidepoint(creature.position[0], creature.position[1])
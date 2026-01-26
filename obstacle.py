import pygame

class Obstacle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.radius = r

    def draw(self, surface):
        # Draw main circular body
        pygame.draw.circle(surface, (40, 40, 45), (int(self.x), int(self.y)), self.radius)
        # Draw border
        pygame.draw.circle(surface, (100, 100, 110), (int(self.x), int(self.y)), self.radius, 2)

    def check_collision(self, creature):
        # Calculate distance between circle center and creature
        dx = self.x - creature.position[0]
        dy = self.y - creature.position[1]
        
        # Check squared distance (faster than using sqrt)
        distance_sq = dx*dx + dy*dy
        
        # Collision if distance is less than radius
        return distance_sq < (self.radius * self.radius)
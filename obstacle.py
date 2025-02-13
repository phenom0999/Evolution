import pygame
class Obstacle:

    def __init__(self, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
        self.obstacle_width = obstacle_width
        self.obstacle_height = obstacle_height
        self.obstacle_x = obstacle_x
        self.obstacle_y = obstacle_y
        self.obstacle_position = pygame.math.Vector2(obstacle_x, obstacle_y)

    def draw(self, surface, color):
        rect_obs = pygame.Rect(0, 0, self.obstacle_width, self.obstacle_height)
        rect_obs.center = self.obstacle_position
        pygame.draw.rect(surface, color, rect_obs)

    def check_collision(self, creature):
        if (self.obstacle_x - self.obstacle_width/2 <= creature.position.x <= self.obstacle_x + self.obstacle_width/2 and
    self.obstacle_y - self.obstacle_height/2 <= creature.position.y <= self.obstacle_y + self.obstacle_height/2):
            return True


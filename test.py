import numpy as np
from creature import WIDTH, HEIGHT
from obstacle import Obstacle


import pygame

o = Obstacle(WIDTH/2, HEIGHT/2, 30, 30)

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))  # clear screen

    # draw stuff here
    edges = o.get_edges()

    for edge in edges:
        start = edge[0]
        end   = edge[1]

        pygame.draw.line(
            screen,
            (255, 255, 0),
            tuple(start),
            tuple(end),
            2
        )


    pygame.display.flip()     # update screen
    clock.tick(60)             # 60 FPS

pygame.quit()

"""
Created on 2019-11-20

Project: pygame
@author: ollejernstrom
"""
import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60

clock = pygame.time.Clock


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


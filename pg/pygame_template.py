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
WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 20
        self.hight = 40
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.get_rect()

    def update(self):
        pass


running = True
while running:
    clock.tick(FPS)
    rocket = Rocket()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    pygame.display.flip()

pygame.quit()

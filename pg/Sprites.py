"""
Created on 2019-11-20

Project: pygame
@author: ollejernstrom
"""
import pygame
import random


from pg.settings import *
from math import atan2, degrees


vec = pygame.math.Vector2
vec3 = pygame.math.Vector3


class Rocket(pygame.sprite.Sprite):
    def __init__(self, speed, target):
        pygame.sprite.Sprite.__init__(self)
        self.width = 20
        self.height = 30
        self.image_orig = pygame.Surface((self.width, self.height))
        self.image_orig.fill(WHITE)
        # self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.vel = vec(0, 0)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        # Random spawnpoint
        self.speed = speed
        self.target = target
        self.last_update = pygame.time.get_ticks()
        # Random side from which the rocket will come from

        self.side = random.random()
        # Left
        if self.side < 0.25:
            self.pos = vec(-30, random.randrange(-30, HEIGHT))
        # Right
        if 0.25 < self.side < 0.50:
            self.pos = vec(WIDTH + 30, random.randrange(-30, HEIGHT))
        # Up
        if 0.50 < self.side < 0.75:
            self.pos = vec(random.randrange(-30, WIDTH + 30), -30)
        # Down
        if self.side > 0.75:
            self.pos = vec(random.randrange(-30, WIDTH + 30), HEIGHT + 30)


    def update(self):
        self.angle = atan2(self.vel[1], self.vel[0])
        self.angle = degrees(self.angle) - 90
        self.rotate()
        # Add vel
        self.direction = vec(self.target.pos - self.pos)
        self.direction = pygame.math.Vector2.normalize(self.direction)
        self.vel = vec(self.speed * self.direction[0], self.speed * self.direction[1])

        # Angle



        self.pos += self.vel

        # print(self.angle)
        # set new pos
        self.rect.center = self.pos


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now

            # Creates a new variable which rotates the image
            new_image = pygame.transform.rotate(self.image_orig, -self.angle)
            old_center = self.rect.center
            # Uppdates the sprite
            self.image = new_image
            self.rect.center = old_center


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 20
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(P_C)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # pos is temporary vairable for calulations
        self.pos = vec(WIDTH / 2, HEIGHT / 2)



    def update(self):
        self.pos = pygame.mouse.get_pos()

        # Set new pos
        self.rect.center = self.pos
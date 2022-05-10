"""
Created on 2019-11-20

Project: pygame
@author: ollejernstrom
"""
import pygame
import random
from os import path

from settings import *
from math import atan2, degrees


vec = pygame.math.Vector2
vec3 = pygame.math.Vector3


img_dir = path.join(path.dirname(__file__), 'img')


def load_image(filename):
    return pygame.image.load(path.join(img_dir, filename)).convert()


class Rocket(pygame.sprite.Sprite):
    def __init__(self, speed, target, img):
        pygame.sprite.Sprite.__init__(self)
        self.width = 30
        self.height = 50
        self.image_orig = pygame.transform.scale(
            img, (self.width, self.height))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        # Random spawnpoint
        self.speed = speed
        self.target = target
        self.last_update = pygame.time.get_ticks()
        # Random side from which the rocket will come from
        self.spawn(random.random())

    def spawn(self, side):
        # Left
        if side < 0.25:
            self.pos = vec(-30, random.randrange(-30, HEIGHT))
        # Right
        if 0.25 < side < 0.50:
            self.pos = vec(WIDTH + 30, random.randrange(-30, HEIGHT))
        # Up
        if 0.50 < side < 0.75:
            self.pos = vec(random.randrange(-30, WIDTH + 30), -30)
        # Down
        if side > 0.75:
            self.pos = vec(random.randrange(-30, WIDTH + 30), HEIGHT + 30)

    def update(self):
        self.angle = atan2(self.vel[1], self.vel[0])
        self.angle = degrees(self.angle) + 90
        self.rotate(self.angle)
        # Add vel
        self.direction = vec(self.target.pos - self.pos)
        self.direction = pygame.math.Vector2.normalize(self.direction)
        self.vel = vec(
            self.speed * self.direction[0], self.speed * self.direction[1])

        # Angle

        self.pos += self.vel

        # print(self.angle)
        # set new pos
        self.rect.center = self.pos

    def rotate(self, degrees):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now

            # Creates a new variable which rotates the image
            new_image = pygame.transform.rotate(self.image_orig, -degrees)
            old_center = self.rect.center
            # Uppdates the sprite
            self.image = new_image
            self.rect.center = old_center


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img = load_image('alien.png')
        self.width = 16
        self.height = 14
        self.image = pygame.transform.scale(
            self.img, (int(self.width * 5/4), int(self.height * 5/4)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # pos is temporary vairable for calulations
        self.pos = vec(WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.pos = pygame.mouse.get_pos()

        # Set new pos
        self.rect.center = self.pos

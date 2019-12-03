"""
Created on 2019-11-20

Project: pygame
@author: ollejernstrom
"""
import pygame
import random
from os import path
import pg.Sprites as sprites
from pg.settings import *

pygame.init()

pygame.mouse.set_cursor(*pygame.cursors.diamond)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mouse.set_pos([WIDTH / 2, HEIGHT / 2])


rocket_list = []



running = True
while running:
    clock.tick(FPS)

    #  Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Update
    all_sprites.update()

    # Collision
    hits = pygame.sprite.spritecollide(player, rockets, True)
    for hit in hits:
        if hit:
            player.kill()
            for i in rockets:
                i.kill()

    for sprite in rockets:
        temp_group = rockets.copy()
        temp_group.remove(sprite)
        # print(temp_group)
        rocket_hit = pygame.sprite.spritecollide(sprite, temp_group, True)

        if rocket_hit:
            rocket = sprites.Rocket(speed=ROCKETSPEED, target=player)
            rockets.add(rocket)
            rocket_list.append(i)
            all_sprites.add(rocket)

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()


class Game:
    def __init(self):
        pygame.init()
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.mouse.set_pos([WIDTH / 2, HEIGHT / 2])

    def load_data(self):
        ##IMPORTERA HIGHSCORE FIL####
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as file:
            try:
                self.highscore = int(file.read())

            except:
                self.highscore = 0

    def new(self):
        self.score = 0

        self.rockets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.player = sprites.Player()
        self.all_sprites.add(self.player)

        for i in range(STARTROCKETS):
            r = sprites.Rocket(speed=ROCKETSPEED, target=self.player)
            self.rockets.add(r)
            self.all_sprites.add(rocket)



        self.run()

    def run(self):
        # Game Loop
        self.clock.tick(FPS)
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        pass

    def events(self):
        pass

    def draw(self):
        pass

    def start_screen(self):
        pass

    def go_scree(self):
        pass

    def draw_text(self):
        pass

    def wait_for_key(self):
        pass
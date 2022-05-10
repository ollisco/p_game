"""
Created on 2019-11-20

Project: pygame
@author: ollejernstrom
"""
import pygame
import random
from os import path
import Sprites as sprites
from settings import *

pygame.init()

pygame.mouse.set_cursor(*pygame.cursors.diamond)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mouse.set_pos([WIDTH / 2, HEIGHT / 2])


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.rocket_img = sprites.load_image('pp.png')

        self.bkg_img = sprites.load_image('sky2.png')
        self.bkg_rect = self.bkg_img.get_rect()

        self.load_data()

    def load_data(self):
        ##IMPORTERA HIGHSCORE FIL####
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as file:
            try:
                self.highscore = int(file.read())

            except Exception as e:
                print(e)
                self.highscore = 0

        print(self.highscore)

    def new(self):
        self.score = 0
        pygame.mouse.set_pos([WIDTH / 2, HEIGHT / 2])

        self.rockets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.player = sprites.Player()
        self.all_sprites.add(self.player)

        for i in range(STARTROCKETS):
            r = sprites.Rocket(speed=ROCKETSPEED,
                               target=self.player, img=self.rocket_img)
            self.rockets.add(r)
            self.all_sprites.add(r)

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
        # Update
        self.all_sprites.update()

        # Collision
        hits = pygame.sprite.spritecollide(self.player, self.rockets, True)
        for hit in hits:
            if hit:
                self.player.kill()
                for i in self.rockets:
                    i.kill()
                    self.playing = False

        for sprite in self.rockets:
            temp_group = self.rockets.copy()
            temp_group.remove(sprite)
            # print(temp_group)
            rocket_hit = pygame.sprite.spritecollide(sprite, temp_group, True)

            if rocket_hit:
                self.score += 1
                r = sprites.Rocket(speed=ROCKETSPEED,
                                   target=self.player, img=self.rocket_img)
                self.rockets.add(r)
                self.all_sprites.add(r)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.player = False
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.playing:
                    self.player = False
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.bkg_img, self.bkg_rect)
        self.all_sprites.draw(screen)
        self.draw_text('Score: ' + str(self.score), 40, WHITE, WIDTH / 2, 10)
        pygame.display.flip()

    def start_screen(self):
        pass

    def go_screen(self):
        if not self.running:
            return
        color = (255, 160, 122)
        go_img = sprites.load_image('sky.png')
        go_rect = go_img.get_rect()

        logo = pygame.transform.scale(
            sprites.load_image('alien.png'), (200, 200))
        logo.set_colorkey(BLACK)

        logo2 = pygame.transform.scale(
            sprites.load_image('pp.png'), (150, 200))
        logo2.set_colorkey(BLACK)

        self.load_data()
        self.screen.fill(BLACK)
        self.screen.blit(go_img, go_rect)
        self.screen.blit(logo, (0, 0))
        self.screen.blit(logo2, (WIDTH-150, 0))
        self.draw_text('GAME OVER!', 50, color, WIDTH / 2, HEIGHT / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text('NEW HIGHSCORE: ' + str(self.highscore),
                           40, color, WIDTH / 2, HEIGHT / 2)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))

        else:
            self.draw_text('Score: ' + str(self.score), 30,
                           color, WIDTH / 2, HEIGHT / 2)
            self.draw_text('High score: ' + str(self.highscore),
                           40, color, WIDTH / 2, (HEIGHT / 2) + 40)
        self.draw_text('Press a key to start', 50,
                       color, WIDTH / 2, HEIGHT * 0.75)

        pygame.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False

                if event.type == pygame.KEYUP:
                    waiting = False


g = Game()
while g.running:
    g.new()
    g.go_screen()


pygame.quit()

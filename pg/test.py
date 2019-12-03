"""
Created on 2019-11-27

Project: p_game
@author: ollejernstrom
"""
import pygame
from os import path
import random


class Game:

    def __init__(self):
        # Init Fönster etc
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        self.running = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        ##IMPORTERA HIGHSCORE FIL####
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as file:
            try:
                self.highscore = int(file.read())

            except:
                self.highscore = 0

    def new(self):
        # starta ett nytt game
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        # SPAWNAR PLATFORM

        for p in PLATFORM_LIST:
            p = Platform(*p)
            self.all_sprites.add(p)
            self.platforms.add(p)

        ######

        self.player = Player(self)
        self.all_sprites.add(self.player)



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
        # Game loop - Update
        self.all_sprites.update()

        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player , self.platforms, False)
            if hits:
                lowest_platform = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest_platform.rect.centery:
                        lowest_platform = hit


                self.player.pos.y = lowest_platform.rect.top
                self.player.vel.y = 0
                self.player.jumping = False

        # skrolla fönstret
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for p in self.platforms:
                p.rect.y += abs(self.player.vel.y)
                # loopar över platformer och kollar om platform är utanför fönstret och tar isf bort
                if p.rect.top >= HEIGHT:
                    p.kill() # Tar bort
                    self.score += 10

        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False

        # print(self.platforms) # Kolla att platform bort fungerar.

        # skapa nya platformer när man skrollar fönstret
        while len(self.platforms) < 6:

            width = random.randrange(50, 100)
            height = random.randrange(12, 25)
            x = random.randrange(0, WIDTH-width)
            y = random.randrange(-60, -30)

            p = Platform(width, height, x, y)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # Game Loop - Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.player.jump_cut()

    def draw(self):
        # Game loop - Rita
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text('Score: ' + str(self.score), 40, OLIVE, WIDTH / 2, 10)
        pygame.display.flip()

    def show_start_screen(self):
        # Startskärmen
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 70, SILVER, WIDTH / 2, HEIGHT / 4)
        self.draw_text('Press a key to start', 50, SILVER, WIDTH / 2, HEIGHT / 2)
        self.draw_text('High Score: ' + str(self.highscore), 30, SILVER, WIDTH / 2, HEIGHT * 0.75)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BG_COLOR)
        self.draw_text('GAME OVER!', 50, GO_COLOR, WIDTH / 2, HEIGHT / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text('NEW HIGHSCORE: ' + str(self.highscore), 40, GO_COLOR, WIDTH / 2,  HEIGHT / 2)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))

        else:
            self.draw_text('Score: ' + str(self.score), 30, GO_COLOR, WIDTH / 2, HEIGHT / 2)
            self.draw_text('High score: ' + str(self.highscore), 40, GO_COLOR, WIDTH / 2, (HEIGHT / 2) + 40 )
        self.draw_text('Press a key to start', 50, GO_COLOR, WIDTH / 2, HEIGHT * 0.75)

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
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()

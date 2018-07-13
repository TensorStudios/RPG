"""

Tensor Studios - RPG!

Developed by
Jonathan Layman
Andrew Albright
Devin Emnett


"""


import pygame as pg
import sys
from Settings import *
from Sprites import *
from os import path
from tilemap import *


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def button(game, msg, x, y, w, h, ic, ac, action=None):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(game.screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                game.intro = False
            elif action == "quit":
                pg.quit()
                quit()
    else:
        pg.draw.rect(game.screen, ic, (x, y, w, h))

    smallText = pg.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    game.screen.blit(textSurf, textRect)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(game.screen, ac, (x, y, w, h))
    else:
        pg.draw.rect(game.screen, ic, (x, y, w, h))

    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    game.screen.blit(textSurf, textRect)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'SBMap.txt'))
        self.gameover_font = path.join(img_folder, 'Game Over Font.TTF')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,180))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        if self.paused:
            self.screen.blit(self.dim_screen, (0,0))
            self.draw_text("MOTHA' FUCKIN' PAUSED", self.gameover_font, 70, WHITE, WIDTH/2, HEIGHT/2, align='center')
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.intro = True
        while self.intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            self.screen.fill(DARKGREY)
            largeText = pg.font.Font(self.gameover_font, 90)
            TextSurf, TextRect = text_objects("TOWER DEFENSE!!!", largeText)
            TextRect.center = ((WIDTH / 2), (HEIGHT / 2))
            self.screen.blit(TextSurf, TextRect)

            button(game, "START", 150, 450, 150, 100, LIGHTGREEN, GREEN, "play")
            button(game, "QUIT", 150, 550, 150, 100, LIGHTRED, RED, "quit")

            pg.display.update()


        # self.screen.fill(DARKGREY)
        # self.draw_text("GAME NAME TBD", self.gameover_font, 50, BLACK, WIDTH/2, HEIGHT/3, align='center')
        # self.draw_text("PRESS ANY KEY TO BEGIN", self.gameover_font, 50, BLACK, WIDTH / 2, HEIGHT / 2, align='center')
        # pg.display.flip()
        # self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("YOU DIED", self.gameover_font, 100, WHITE, WIDTH/2, HEIGHT/2, align='center')
        self.draw_text("Press Any Key", self.gameover_font, 75, WHITE, WIDTH/2, HEIGHT*3/4, align='center')
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False



# create the game object
intro = True
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

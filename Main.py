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

    smallText = pg.font.Font("freesansbold.ttf", 30)
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
# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 500
    BAR_HEIGHT = 60
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_player_mana(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 500
    BAR_HEIGHT = 40
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, BLUE, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_player_equip1(surf, x, y, pct):
    BAR_LENGTH = 100
    BAR_HEIGHT = 100
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, BLACK, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_player_equip2(surf, x, y, pct):
    BAR_LENGTH = 100
    BAR_HEIGHT = 100
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, BLACK, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        # Load folder locations
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')

        # Load game map
        self.map = Map(path.join(game_folder, 'SBMap.txt'))
        self.gameover_font = path.join(img_folder, 'Game Over Font.TTF')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,180))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()

        # Load map, spawn appropriate sprites
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)

        # Create the camera object
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

        # mobs hit player, if a mob runs into the player, knock playe back and deal damage to player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

    # Debug function to draw grid to screen
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        # Set the caption of the game to be the current FPS
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        # Set the background of the screen to the Background color
        self.screen.fill(BGCOLOR)

        # Debug draw grid
        # self.draw_grid()

        # Draw each sprite to the screen
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        if self.paused:
            self.screen.blit(self.dim_screen, (0,0))
            self.draw_text("MOTHA' FUCKIN' PAUSED", self.gameover_font, 70, WHITE, WIDTH/2, HEIGHT/2, align='center')
        # HUD Functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        draw_player_mana(self.screen, 10, 70, self.player.health / PLAYER_HEALTH)
        draw_player_equip1(self.screen, 700, 10, 1)
        draw_player_equip2(self.screen, 830, 10, 1)

        # Draw player attack animation (only displays if recently attacked)
        self.player.attack_animation()

        # Flip the screen
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_TAB:
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

    def show_start_screen(game):
        game.intro = True
        while game.intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            game.screen.fill(DARKGREY)
            largeText = pg.font.Font('freesansbold.ttf', 90)
            TextSurf, TextRect = text_objects("Game Name TBD", largeText)
            TextRect.center = ((WIDTH / 2), (HEIGHT / 4))
            game.screen.blit(TextSurf, TextRect)

            button(game, "NEW GAME", WIDTH/2 - 150, 350, 300, 75, WHITE, LIGHTGREY, "play")
            button(game, "LOAD", WIDTH/2 - 150, 450, 300, 75, WHITE, LIGHTGREY, "load")
            button(game, "SETTINGS", WIDTH / 2 - 150, 550, 300, 75, WHITE, LIGHTGREY, "settings")
            button(game, "QUIT", WIDTH/2 - 150, 650, 300, 75, WHITE, LIGHTGREY, "quit")

            pg.display.update()

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
    g.show_start_screen()

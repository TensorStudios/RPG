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
        self.draw_debug = False

    def load_data(self):
        # Load folder locations
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map_folder = path.join(game_folder, "Maps")

        # Load game map
        self.map = Map(path.join(game_folder, 'SBMap.txt'))
        self.map_img = None
        self.gameover_font = path.join(img_folder, 'Game Over Font.TTF')
        self.inventory_font = path.join(img_folder, "coolvetica rg.ttf")
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        # Class variable initiation
        self.mouse_dir = None

        # Load Spritesheet image
        self.spritesheet_k_r = Spritesheet(path.join(img_folder, "Knight.png"))
        self.spritesheet_k_l = Spritesheet(path.join(img_folder, "Knight Left.png"))
        self.spritesheet_k_a_r = Spritesheet(path.join(img_folder, "Knight Attack Pose.png"))
        self.spritesheet_k_a_l = Spritesheet(path.join(img_folder, "Knight Attack Pose Left.png"))
        self.spritesheet_aa_s = Spritesheet(path.join(img_folder, "Sword Attack Animation.png"))
        self.spritesheet_z_r = Spritesheet(path.join(img_folder, "Zombie.png"))
        self.spritesheet_z_l = Spritesheet(path.join(img_folder, "Zombie Left.png"))

        self.weapon_animations = {
            "sword": {
                "Frame Rate": 100,
                "Images": {
                    0: self.spritesheet_aa_s.get_image(0, 0, 160, 160),
                    1: self.spritesheet_aa_s.get_image(160, 0, 160, 160),
                    2: self.spritesheet_aa_s.get_image(0, 160, 160, 160)
                }
            }
        }
        for weapon in self.weapon_animations:
            for image in self.weapon_animations[weapon]["Images"]:
                self.weapon_animations[weapon]["Images"][image].set_colorkey(BG_SPRITE_COLOR)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, "Map1.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.show_inventory = False
        self.dialog = False
        self.dialog_selection = None
        self.dialog_text = ""
        self.dialog_options = []

        # Load map, spawn appropriate sprites
        for tile_object in self.map.tmxdata.objects:
            object_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == "Player":
                self.player = Player(self, object_center.x, object_center.y)
            if tile_object.name == "Mob":
                Mob(self, object_center.x, object_center.y)
            if tile_object.name == "Wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "NPC":
                NonPlayerCharacter(self, object_center.x, object_center.y)

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
        self.mouse_dir = vec(self.camera.mouse_adjustment(pg.mouse.get_pos())) - vec(self.player.pos)
        self.all_sprites.update()
        self.camera.update(self.player)

        # mobs hit player, if a mob runs into the player, knock player back and deal damage to player
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

    def open_inventory(self):
        if self.show_inventory:
            self.draw_player_inventory(self.screen, 750, 150, self.player.inventory)

    def draw_player_inventory(self, surf, x, y, inventory):
        box_height = 500
        box_width = 250
        rect = pg.Rect(x, y, box_width, box_height)
        outline_rect = pg.Rect(x, y, box_width, box_height)
        pg.draw.rect(surf, BLACK, rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)

        text_height = 25

        mouse = pg.mouse.get_pressed()

        for position, item in enumerate(inventory):
            rect = pg.Rect(x + 5, y + 15 + (position * text_height), box_width, text_height)
            if rect.collidepoint(pg.mouse.get_pos()):
                self.draw_text(item, self.inventory_font, 20, BLUE, x + 5, y + 15 + (position * text_height), "w")
                if mouse[0]:
                    self.player.use_item(position)
            else:
                self.draw_text(item, self.inventory_font, 20, WHITE, x + 5, y + 15 + (position * text_height), "w")

    def open_dialog(self):
        if self.dialog:
            self.draw_dialog(self.screen, self.dialog_text, self.dialog_options)

    def draw_dialog(self, surf, message, options):
        x = 100
        y = 500
        box_height = 250
        box_width = 800
        rect = pg.Rect(x, y, box_width, box_height)
        outline_rect = pg.Rect(x, y, box_width, box_height)
        options_rect = pg.Rect(x, y, box_width / 5, box_height)
        pg.draw.rect(surf, BLACK, rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)
        pg.draw.rect(surf, WHITE, options_rect, 2)

        text_height = 20

        mouse = pg.mouse.get_pressed()

        # Draw options
        for position, option in enumerate(options):
            rect = pg.Rect(x + 5, y + 15 + (position * text_height), box_width, text_height)
            if rect.collidepoint(pg.mouse.get_pos()):
                self.draw_text(option, self.inventory_font, 20, BLUE, x + 5, y + 15 + (position * text_height), "w")
                if mouse[0]:
                    self.dialog_selection = position
            else:
                self.draw_text(option, self.inventory_font, 20, WHITE, x + 5, y + 15 + (position * text_height), "w")

        # Draw text
        self.draw_text(message, self.inventory_font, 20, WHITE, x + 5 + (box_width / 5), y + 15, "w")

    def draw(self):
        # Set the caption of the game to be the current FPS
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        # Set the background of the screen to the Background color
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        # Debug draw grid
        # self.draw_grid()

        # Draw each sprite to the screen
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(wall.rect), 1)
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("MOTHA' FUCKIN' PAUSED", self.gameover_font, 70, WHITE, WIDTH / 2, HEIGHT / 2,
                           align='center')
        # HUD Functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        draw_player_mana(self.screen, 10, 70, self.player.health / PLAYER_HEALTH)
        draw_player_equip1(self.screen, 700, 10, 1)
        draw_player_equip2(self.screen, 830, 10, 1)
        self.open_inventory()
        self.open_dialog()

        # Flip the screen
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.show_inventory = False
                    self.dialog = False
                if event.key == pg.K_TAB:
                    self.paused = not self.paused
                if event.key == pg.K_b:
                    # Show inventory
                    self.show_inventory = not self.show_inventory
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_t:
                    self.dialog = False

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
            largeText = pg.font.Font('freesansbold.ttf', 90)
            TextSurf, TextRect = text_objects("Game Name TBD", largeText)
            TextRect.center = ((WIDTH / 2), (HEIGHT / 4))
            self.screen.blit(TextSurf, TextRect)

            button(self, "NEW GAME", WIDTH / 2 - 150, 350, 300, 75, WHITE, LIGHTGREY, "play")
            button(self, "LOAD", WIDTH / 2 - 150, 450, 300, 75, WHITE, LIGHTGREY, "load")
            button(self, "SETTINGS", WIDTH / 2 - 150, 550, 300, 75, WHITE, LIGHTGREY, "settings")
            button(self, "QUIT", WIDTH / 2 - 150, 650, 300, 75, WHITE, LIGHTGREY, "quit")

            pg.display.update()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("YOU DIED", self.gameover_font, 100, WHITE, WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text("Press Any Key", self.gameover_font, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align='center')
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
g = Game()
while True:
    g.show_start_screen()
    g.new()
    g.run()
    g.show_go_screen()

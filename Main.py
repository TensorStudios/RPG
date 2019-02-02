"""

Tensor Studios - RPG!

Developed by
Jonathan Layman
Andrew Albright
Devin Emnett


"""

import logging
import datetime
import pygame as pg
import sys
from Settings import *
from Sprites import *
from os import path, chdir, getcwd
from tilemap import *
from NPC.NPC import QuestNPC
from NPC.Quests import Quests
from Player.PlayerData import PLAYER
from Interface.UI import *


logging.basicConfig(filename=f"logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log", level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")


class Game:
    def __init__(self):
        logging.debug("Initializing Game")
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.draw_debug = False

    def load_data(self):
        logging.info("Loading Game")
        # Load folder locations
        game_folder = getcwd()
        img_folder = resource_path(game_folder + '/img/')
        self.map_folder = resource_path(game_folder + "/Maps/")

        # Load game map
        self.map = None
        self.map_img = None
        logging.debug("loading Fonts")
        self.gameover_font = resource_path(img_folder + 'Game Over Font.TTF')
        self.inventory_font = resource_path(img_folder + "coolvetica rg.ttf")
        logging.debug("success")
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        # Class variable initiation
        self.mouse_dir = None

        # health pack image
        logging.debug("loading healthpack img")
        self.healthpack_img = pg.image.load(resource_path(img_folder + "health_pack.png")).convert()
        self.healthpack_img = pg.transform.scale(self.healthpack_img, (20, 20))
        logging.debug("success")

        # Load Spritesheet image for animations
        logging.debug("loading spritesheet imgs")
        self.spritesheet_k_r = Spritesheet(resource_path(img_folder + "Knight.png"))
        self.spritesheet_k_l = Spritesheet(resource_path(img_folder + "Knight Left.png"))
        self.spritesheet_k_a_r = Spritesheet(resource_path(img_folder + "Knight Attack Pose.png"))
        self.spritesheet_k_a_l = Spritesheet(resource_path(img_folder + "Knight Attack Pose Left.png"))
        self.spritesheet_aa_s = Spritesheet(resource_path(img_folder + "Attack Animation.png"))
        self.spritesheet_fire_attack = Spritesheet(resource_path(img_folder + "Fire Attack.png"))
        self.spritesheet_z_r = Spritesheet(resource_path(img_folder + "Zombie.png"))
        self.spritesheet_z_l = Spritesheet(resource_path(img_folder + "Zombie Left.png"))

        self.weapon_animations = {
            "sword": {
                "Frame Rate": 100,
                "Images": {
                    0: self.spritesheet_aa_s.get_image(0, 0, 160, 160),
                    1: self.spritesheet_aa_s.get_image(0, 160, 160, 160)
                }
            },
            "fire sword": {
                "Frame Rate": 100,
                "Images": {
                    0: self.spritesheet_fire_attack.get_image(0, 0, 160, 160),
                    1: self.spritesheet_fire_attack.get_image(0, 160, 160, 160)
                }
            }
        }
        for weapon in self.weapon_animations:
            for image in self.weapon_animations[weapon]["Images"]:
                self.weapon_animations[weapon]["Images"][image].set_colorkey(BG_SPRITE_COLOR)
        logging.debug("Success")
        logging.info("Successfully loaded all data")

    def new(self):
        # initialize all variables and do all the setup for a new game
        logging.info("Loading New game settings")
        logging.info("Creating sprite groups")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.spawn_zones = []
        logging.info("Loading map")
        self.map = TiledMap(resource_path(self.map_folder + "Map1.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        logging.info("reseting class variables")
        self.show_inventory = False
        self.dialog = False
        self.dialog_selection = None
        self.dialog_text = ""
        self.dialog_options = []
        self.pause_menu_selection = None

        # Load map, spawn appropriate sprites
        logging.info("Placing sprites and objects on map")
        for tile_object in self.map.tmxdata.objects:
            object_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == "Player":
                self.player = Player(self, object_center.x, object_center.y)
                logging.debug("Placing Player Sprite")
            elif tile_object.name == "Mob":
                Mob(self, object_center.x, object_center.y)
                logging.debug("Placing Mob Sprite")
            elif tile_object.name == "Wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                logging.debug("Placing Obstacle sprite")
            elif tile_object.name == "Health":
                Item(self, (object_center.x, object_center.y), tile_object.name)
                logging.debug("Placing Item Sprite")
            elif tile_object.name == "NPC":
                QuestNPC(self, object_center.x, object_center.y, ID=int(tile_object.type))
                logging.debug("Placing NPC Sprite")
            elif tile_object.name == "Mob_Spawn_Zone":
                MobSpawnZone(tile_object.x, tile_object.y, tile_object.width, tile_object.height, self)
            else:
                logging.warning(f"{tile_object.name} is unable to be loaded because it has not been coded yet")

        # Create the camera object
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False

    def run(self):
        # game loop - set self.playing = False to end the game
        logging.info("Run main game")
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        logging.warning("Quitting Game")
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        logging.debug("Calculating Update Loop")

        # Get the direction of the mouse relative to the character
        self.mouse_dir = vec(self.camera.mouse_adjustment(pg.mouse.get_pos())) - vec(self.player.pos)

        self.all_sprites.update()
        self.camera.update(self.player)

        # if there are spawn zones, update them
        for zone in self.spawn_zones:
            zone.update()

        # mobs hit player, if a mob runs into the player, knock player back and deal damage to player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.take_damage(MOB_DAMAGE)
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        #player hits item
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            self.player.add_item(hit.type)
            hit.kill()

    # Debug function to draw grid to screen
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    # Trigger inventory screen
    def open_inventory(self):
        if self.show_inventory:
            logging.debug("Inventory Open")
            self.draw_player_inventory(self.screen, 750, 150, self.player.inventory)

    # Draw inventory on screen
    def draw_player_inventory(self, surf, x, y, inventory):
        box_height = 500
        box_width = 250
        rect = pg.Rect(x, y, box_width, box_height)
        outline_rect = pg.Rect(x, y, box_width, box_height)
        pg.draw.rect(surf, BLACK, rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)

        text_height = 25

        mouse = pg.mouse.get_pressed()

        # check if mouse is over item and inventory and highlight blue if that is the case
        for position, item in enumerate(inventory):
            rect = pg.Rect(x + 5, y + 15 + (position * text_height), box_width, text_height)
            if rect.collidepoint(pg.mouse.get_pos()):
                self.draw_text(item, self.inventory_font, 20, BLUE, x + 5, y + 15 + (position * text_height), "w")
                # If the item is left clicked, tell the player to use the item
                if mouse[0]:
                    self.player.use_item(position)
            else:
                self.draw_text(item, self.inventory_font, 20, WHITE, x + 5, y + 15 + (position * text_height), "w")

    # Trigger dialog
    def open_dialog(self):
        if self.dialog:
            logging.debug("Open Dialog")
            self.draw_dialog(self.screen, self.dialog_text, self.dialog_options)

    # Draw dialog
    def draw_dialog(self, surf, message, options):
        """

        :param surf: The game screen
        :param message: The message of the NPC Text, passed from the NPC Class
        :param options: THe Options of the NPC Text, also passed from the NPC Class

        Once an option is chosen, the NPC Class looks at self.dialog_selection to handle the reaction.
        The NPC Class will reset self.dialog_selection back to None once it has been handled

        """
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
        for position, option in options.items():
            option_text = option["Text"]
            rect = pg.Rect(x + 5, y + 5 + (int(position) * text_height), box_width, text_height)
            # Change dialog text color, just like in inventory
            if rect.collidepoint(pg.mouse.get_pos()):
                self.draw_text(option_text, self.inventory_font,
                               20, BLUE, x + 5, y + (int(position) * text_height), "w")
                # If dialog option is clicked, pass that to the NPC
                if mouse[0]:
                    logging.debug(f"Dialog option selected: {position} ")
                    self.dialog_selection = str(position)
            else:
                self.draw_text(option_text, self.inventory_font,
                               20, WHITE, x + 5, y + (int(position) * text_height), "w")

        # Draw text
        self.draw_text(message, self.inventory_font, 20, WHITE, x + 5 + (box_width / 5), y + 15, "w")

    def pause_menu(self):
        logging.info("Game paused")
        self.screen.blit(self.dim_screen, (0, 0))
        self.draw_text("MOTHA' FUCKIN' PAUSED", self.gameover_font, 70, WHITE, WIDTH / 2, HEIGHT / 4,
                       align='center')

        # Add menu, find mouse position and options
        mouse = pg.mouse.get_pressed()
        y = 350
        spacing = 100

        menu_options = {
            0: "Save",
            1: "Load",
            2: "Main Menu",
            3: "Resume"
        }
        # Change color of option moused over and select it by clicking, just like inventory screen
        for position, option in enumerate(menu_options):
            rect = pg.Rect(0, y + (position * spacing) - (spacing / 2), WIDTH, spacing)
            if rect.collidepoint(pg.mouse.get_pos()):
                self.draw_text(menu_options[position], self.gameover_font, 50, BLUE, WIDTH / 2,
                               y + (position * spacing), align="center")
                if mouse[0]:
                    self.pause_menu_selection = position
            else:
                self.draw_text(menu_options[position], self.gameover_font, 50, WHITE, WIDTH / 2,
                               y + (position * spacing), align="center")

        # Handle option chosen
        if self.pause_menu_selection == 0:
            self.save_game()
        elif self.pause_menu_selection == 1:
            self.load_game()
        elif self.pause_menu_selection == 2:
            self.load_main_menu()
        elif self.pause_menu_selection == 3:
            self.resume_game()

    # Placeholder for game save
    def save_game(self):
        self.pause_menu_selection = None
        logging.info("Game Saved")

    # Placeholder for game load
    def load_game(self):
        self.pause_menu_selection = None
        logging.info("Game Loaded")

    # Go to main menu, resets game
    # Can also resume game from where pause screen was
    def load_main_menu(self):
        self.pause_menu_selection = None
        self.playing = False
        logging.info("Loading Main Menu")

    # Resume game
    def resume_game(self):
        self.pause_menu_selection = None
        self.paused = False
        logging.info("Resuming Game")

    def draw(self):
        logging.debug("Drawing to screen")
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
                try:
                    pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(sprite.hit_rect), 1)
                except AttributeError:
                    continue
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(wall.rect), 1)
        if self.paused:
            self.pause_menu()

        # HUD Functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER["Health"])
        draw_player_mana(self.screen, 10, 70, self.player.mana / PLAYER["Mana"])
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
                    logging.debug("ESC Pressed")
                if event.key == pg.K_TAB:
                    self.paused = not self.paused
                    logging.debug("Tab Pressed")
                if event.key == pg.K_b:
                    # Show inventory
                    self.show_inventory = not self.show_inventory
                    logging.debug("b pressed")
                if event.key == pg.K_h:
                    # Show rects
                    self.draw_debug = not self.draw_debug
                    logging.debug("h pressed")
                if event.key == pg.K_t:
                    # Close dialog if it is open
                    self.dialog = False
                    logging.debug("t pressed")

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
        logging.info("Show start screen")
        self.intro = True
        while self.intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.screen.fill(DARKGREY)
            largeText = pg.font.Font(resource_path(getcwd() + "/img/coolvetica rg.ttf"), 90)
            TextSurf, TextRect = text_objects("Game Name TBD", largeText)
            TextRect.center = ((WIDTH / 2), (HEIGHT / 4))
            self.screen.blit(TextSurf, TextRect)

            button(self, "NEW GAME", WIDTH / 2 - 150, 350, 300, 75, WHITE, LIGHTGREY, "play")
            button(self, "LOAD", WIDTH / 2 - 150, 450, 300, 75, WHITE, LIGHTGREY, "load")
            button(self, "SETTINGS", WIDTH / 2 - 150, 550, 300, 75, WHITE, LIGHTGREY, "settings")
            button(self, "QUIT", WIDTH / 2 - 150, 650, 300, 75, WHITE, LIGHTGREY, "quit")

            pg.display.update()

    def show_go_screen(self):
        logging.info("Show game over screen")
        if self.player.health <= 0:
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
    logging.info("Calling Start Screen")
    g.show_start_screen()
    logging.info("Calling New game")
    g.new()
    logging.info("Callilng Game loop")
    g.run()
    logging.info("Calling Game over screen")
    g.show_go_screen()

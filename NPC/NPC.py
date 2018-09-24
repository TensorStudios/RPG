import pygame as pg
import math
from itertools import cycle
from Settings import *
from Sprites import collide_with_walls, collide_hit_rect
from NPC.Conversations import npc_conversations

vec = pg.math.Vector2


class NonPlayerCharacter(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # When you subclass an NPC, be sure to add in proper images
        self.images = {
            "Example": "example"
        }
        # Remember to set the colorkey for the image just like this:
        # for image in self.images:
        #     self.images[image].set_colorkey(BG_SPRITE_COLOR)
        self.image = pg.Surface((TILESIZE, TILESIZE))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = NPC_HEALTH
        self.click_delay = pg.time.get_ticks()
        self.active = False
        self.dialog_step = "initial"
        self.id = 0

    def get_clicked(self):
        mouse = pg.mouse.get_pressed()

        # Check distance from player
        now = pg.time.get_ticks()
        dist = self.pos - self.game.player.hit_rect.center
        if mouse[0]:
            if self.game.camera.apply_rect(self.hit_rect).collidepoint(pg.mouse.get_pos()):
                if now - self.click_delay > 1000:
                    self.click_delay = now
                    if 0 < dist.length() < SPEAK_RANGE:
                        self.active = True
        if dist.length() > SPEAK_RANGE:
            self.active = False
            self.reset_dialog()

    def reset_dialog(self):
        self.game.dialog = False
        self.game.dialog_selection = None
        self.game.dialog_text = ""
        self.game.dialog_options = []
        self.active = False

    def get_dialog_text_and_options(self):
        return npc_conversations["id"][self.id][self.dialog_step]["text"], \
               npc_conversations["id"][self.id][self.dialog_step]["options"].keys()

    def handle_dialog(self, *args):
        pass

    def update(self):
        pass


class TestNPC(NonPlayerCharacter):
    def __init__(self, game, x, y):
        NonPlayerCharacter.__init__(self, game, x, y)
        self.images = {
            "NPC_r": self.game.spritesheet_k_r.get_image(0, 0, 100, 100)
        }
        self.image = self.images["NPC_r"]
        for image in self.images:
            self.images[image].set_colorkey(BG_SPRITE_COLOR)
        self.id = 1
        self.health_packs = 1

    def dialog_text(self):
        text = ""
        options = []
        if self.dialog_step == "initial":
            text, options = self.get_dialog_text_and_options()

        return text, options

    def handle_dialog(self, *args):
        args = args[0]
        if "health" in args:
            if self.health_packs > 0:
                self.health_packs -= 1
                self.game.player.add_item("Health")
        if "explain" in args:
            self.reset_dialog()
            self.active = True
        if "d_2" in args:
            self.dialog_step = "d_2"
        if "close" in args:
            self.dialog_step = "d_3"
            self.reset_dialog()

    def update(self):
        self.get_clicked()
        if self.health <= 0:
            self.kill()
        # self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(NPC_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        if self.vel.x >= 0:
            self.image = self.images["NPC_r"]
        else:
            self.image = self.images["NPC_r"]
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        if self.active:
            if self.game.dialog_selection is None:
                self.game.dialog = True
                self.game.dialog_text, self.game.dialog_options = self.get_dialog_text_and_options()
            else:
                self.handle_dialog(npc_conversations["id"][self.id][self.dialog_step]["options"]
                                   [self.game.dialog_selection])

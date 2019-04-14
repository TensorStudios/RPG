import logging
import pygame as pg
from Settings import *
import random
from NPC import Quests
from Items.Weapons import WEAPONS
from Player.PlayerData import PLAYER, get_exp_requirement
from os import path, chdir, getcwd
import sys


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relative_path)
    return path.join(path.abspath("."), relative_path)


vec = pg.math.Vector2


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.hit_rect)


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Spritesheet:
    # utility class for loading and parsing sprites
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename)

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y, respawn=False):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = {
            "Zombie_r": self.game.spritesheet_z_r.get_image(0, 0, 100, 100),
            "Zombie_l": self.game.spritesheet_z_l.get_image(0, 0, 100, 100)
        }
        self.image = self.images["Zombie_r"]
        self.highlight = False
        self.targeted = False
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.x = 0
        self.y = 0
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.health_bar = None
        self.target = game.player

        self.patrol_change = pg.time.get_ticks()
        self.patrol_direction = random.randrange(0, 361)
        self.spawn_number = len(self.game.mobs)
        # add a list of all of the quests this mob is a target for
        self.quests = [1]
        # show damage number
        self.show_damage = False
        self.damage_show_time = 200
        self.damage_show_current = pg.time.get_ticks()
        self.floating_dmg_amount = None
        self.floating_dmg_font = pg.font.Font(resource_path(getcwd() + "/img/coolvetica rg.ttf"), 35)
        logging.info(f"Created Mob {self.spawn_number}")
        self.dying = False
        self.death_timer = 100
        self.death_timer_start = pg.time.get_ticks()

    def __str__(self):
        return f"Mob {self.spawn_number}"

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < MOB_AVOID_RADIUS:
                    self.acc += dist.normalize()

    @ staticmethod
    def eight_directional_movement(direction):
        if direction.x > 0:
            if direction.y > 0:
                return vec(1, 1)
            else:
                return vec(1, -1)
        else:
            if direction.y > 0:
                return vec(-1, 1)
            else:
                return vec(-1, -1)

    def patrol(self):
        now = pg.time.get_ticks()
        if now > self.patrol_change:
            self.patrol_change = now + PATROL_CHANGE_TIME
            self.patrol_direction = random.randrange(0, 361)
        self.rect.center = self.pos
        self.rot = self.patrol_direction

    def grant_exp(self):
        self.game.player.collect_exp(MOB_EXP)

    def update_quest(self):
        for quest in self.quests:
            if quest in Quests.QUEST_STATUS["Active"]:
                logging.info(f"Adding to counter for quest id: {self.quests}")
                Quests.update_quest_progress(quest, 1)

    def highlight_on_mouseover(self):
        mouse = pg.mouse.get_pos()

        if self.game.camera.apply_rect(self.rect).collidepoint(mouse):
            # print("I am moused over")
            self.image.fill((255, 0, 0, 200), special_flags=pg.BLEND_RGBA_MULT)
            self.targeted = True
        else:
            self.targeted = False

    def take_damage(self, damage):
        self.health -= damage
        self.show_damage = True
        self.floating_dmg_amount = damage
        self.damage_show_current = pg.time.get_ticks()

    def display_floating_damage(self):
        # Display floating damage text
        if self.floating_dmg_amount is not None:
            now = pg.time.get_ticks()
            # print(now - self.damage_show_current < self.damage_show_time)
            if now - self.damage_show_current < self.damage_show_time:
                floating_dmg_surface = self.floating_dmg_font.render(str(self.floating_dmg_amount), True, WHITE)
                floating_dmg_rect = floating_dmg_surface.get_rect()
                floating_dmg_rect.midtop = (self.rect.width / 2, 0)
                self.image.blit(floating_dmg_surface, floating_dmg_rect)
            else:
                self.floating_dmg_amount = None

    def update(self):
        logging.debug(f"updating mob {self.spawn_number}")
        if self.health <= 0:
            if self.dying:
                if pg.time.get_ticks() - self.death_timer_start > self.death_timer:
                    logging.info(f"Mob {self.spawn_number} has died")
                    self.grant_exp()
                    self.update_quest()
                    if random.random() >= DROP_RATE:
                        Item(self.game, self.pos, "Health")
                    self.kill()
            else:
                self.dying = True
                self.death_timer_start = pg.time.get_ticks()
                self.display_floating_damage()
        else:
            target_dist = self.target.pos - self.pos
            if target_dist.length_squared() < DETECT_RADIUS**2:
                self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
                # self.rect = self.image.get_rect()
            else:
                self.patrol()
            self.rect.center = self.pos
            self.acc = self.eight_directional_movement(vec(1, 0).rotate(-self.rot))
            self.avoid_mobs()
            self.acc.scale_to_length(MOB_SPEED)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            # Commented out acceleration equation below
            self.pos += self.vel * self.game.dt
            self.hit_rect.centerx = self.pos.x
            if self.vel.x >= 0:
                self.image = self.images["Zombie_r"].copy()
            else:
                self.image = self.images["Zombie_l"].copy()
                self.image.convert_alpha()
            self.highlight_on_mouseover()
            self.draw_health()
            self.display_floating_damage()

            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class MobSpawnZone:
    def __init__(self, x, y, width, height, game):
        self.groups = game.all_sprites
        self.target = 5
        self.mobs = []
        self.game = game
        self.game.spawn_zones.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.respawn_timer = 5000
        self.respawn_time = pg.time.get_ticks()

    def create_spawn_point(self, _dir):
        if _dir == "x":
            x = random.randrange(self.x, self.x + self.width)
            return x
        if _dir == "y":
            y = random.randrange(self.y, self.y + self.height)
            return y

    def update(self):
        now = pg.time.get_ticks()
        for position, mob in enumerate(self.mobs):
            if not mob.alive():
                self.mobs.pop(position)
        if now - self.respawn_time > self.respawn_timer:
            self.respawn_time = now
            if len(self.mobs) < self.target:
                logging.info("Mob Spawn Zone: Spawning Mob")
                self.mobs.append(Mob(self.game, self.create_spawn_point("x"), self.create_spawn_point("y")))


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, _type):
        self._layer = ITEM_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.healthpack_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.type = _type
        self.rect.center = pos

import pygame as pg
import math
from itertools import cycle

from Settings import *


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
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = {
            "Walk_r_1": self.game.spritesheet_k_r.get_image(0, 0, 100, 100),
            "Walk_r_2": self.game.spritesheet_k_r.get_image(100, 0, 100, 100),
            "Walk_r_3": self.game.spritesheet_k_r.get_image(0, 100, 100, 100),
            "Walk_r_4": self.game.spritesheet_k_r.get_image(100, 100, 100, 100),
            "Walk_l_1": self.game.spritesheet_k_l.get_image(0, 0, 100, 100),
            "Walk_l_2": self.game.spritesheet_k_l.get_image(100, 0, 100, 100),
            "Walk_l_3": self.game.spritesheet_k_l.get_image(0, 100, 100, 100),
            "Walk_l_4": self.game.spritesheet_k_l.get_image(100, 100, 100, 100),
            "Attack_r_1": self.game.spritesheet_k_a_r.get_image(0, 0, 100, 100),
            "Attack_r_2": self.game.spritesheet_k_a_r.get_image(100, 0, 100, 100),
            "Attack_r_3": self.game.spritesheet_k_a_r.get_image(0, 100, 100, 100),
            "Attack_r_4": self.game.spritesheet_k_a_r.get_image(100, 100, 100, 100),
            "Attack_l_1": self.game.spritesheet_k_a_l.get_image(0, 0, 100, 100),
            "Attack_l_2": self.game.spritesheet_k_a_l.get_image(100, 0, 100, 100),
            "Attack_l_3": self.game.spritesheet_k_a_l.get_image(0, 100, 100, 100),
            "Attack_l_4": self.game.spritesheet_k_a_l.get_image(100, 100, 100, 100),
        }
        self.walk_cycle = cycle(range(4))
        self.frame = 0
        self.walk_right = [self.images["Walk_r_1"],
                           self.images["Walk_r_2"],
                           self.images["Walk_r_3"],
                           self.images["Walk_r_4"]]
        self.walk_left = [self.images["Walk_l_1"],
                           self.images["Walk_l_2"],
                           self.images["Walk_l_3"],
                           self.images["Walk_l_4"]]
        self.attack_right = [self.images["Attack_r_1"],
                           self.images["Attack_r_2"],
                           self.images["Attack_r_3"],
                           self.images["Attack_r_4"]]
        self.attack_left = [self.images["Attack_l_1"],
                           self.images["Attack_l_2"],
                           self.images["Attack_l_3"],
                           self.images["Attack_l_4"]]
        self.image = self.walk_right[self.frame]
        self.walk_frame_time = pg.time.get_ticks() - SPRITE_FRAME_DELAY
        for image in self.images:
            self.images[image].set_colorkey(BG_SPRITE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.facing = "R"
        self.direction = 270.0
        self.health = PLAYER_HEALTH
        self.last_attack = pg.time.get_ticks() - 150
        self.attack_radius = WEAPON_RANGE
        self.attack_speed = WEAPON_SPEED
        self.damage = WEAPON_DAMAGE
        self.attacking = False
        self.inventory = [
            "Health",
            "Health",
            "Health"
        ]
        self.inventory_click_delay = pg.time.get_ticks()
        self.damage_time = pg.time.get_ticks()

    def update_frame(self, update=True):
        if update:
            self.frame = self.walk_cycle.__next__()
        return self.frame

    def attack(self):
        # Find mobs in range
        mobs_in_range = []
        for mob in self.game.mobs:
            if self.pos.distance_squared_to(mob.pos) <= self.attack_radius ** 2:
                mobs_in_range.append(mob)
        # Check if it has been long enough
        now = pg.time.get_ticks()
        if now - WEAPON_SPEED > self.last_attack:
            # Toggle animation flag
            self.attacking = True
            self.last_attack = now
            # Character Attack Pose
            if self.facing == "R":
                self.image = self.attack_right[self.update_frame()]
            else:
                self.image = self.attack_left[self.update_frame()]
            WeaponAnimation(self.attack_speed, self.direction, "sword", self.game, self)

            for mob in mobs_in_range:
                # Check if the mob is within the weapon arc
                # largest degree
                high_angle = (self.direction + WEAPON_ARC) % 360
                # Smallest degree
                low_angle = (self.direction - WEAPON_ARC) % 360
                # The angle of the mob to the player
                mob_angle = (self.pos - mob.pos).normalize()
                # Add 180 degrees to make it easy to compare angles
                mob_angle = vec(0, 0).angle_to(mob_angle) + 180

                # See if the mob angle is within the two angles
                if high_angle >= mob_angle >= low_angle:
                    mob.health -= WEAPON_DAMAGE
                    # print("Hit")
                # account for if the mob is at a high angle and high_angle is at a low value
                elif high_angle < 90:
                    if mob_angle >= 315:
                        mob_angle -= 360
                    low_angle -= 360
                    if high_angle >= mob_angle >= low_angle:
                        # print("Hit")
                        mob.health -= WEAPON_DAMAGE

    def take_damage(self, damage):
        now = pg.time.get_ticks()
        if now - self.damage_time >= PLAYER_DAMAGE_MITIGATION_TIME:
            self.damage_time = now
            self.health -= damage

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        movex = False
        movey = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel += vec(-PLAYER_SPEED, 0)
            movex = True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel += vec(PLAYER_SPEED, 0)
            movex = True
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel += vec(0, -PLAYER_SPEED)
            movey = True
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel += vec(0, PLAYER_SPEED)
            movey = True
        if movex and movey:
            self.vel *= 0.7071
        if keys[pg.K_SPACE]:
            self.attack()

    def get_direction(self):
        # find what direction the player is facing
        if self.vel != vec(0, 0):
            self.direction = vec(0, 0).angle_to(self.vel.normalize())
            # print(self.direction)

    def add_item(self, item):
        if item in INVENTORY_TYPES:
            self.inventory.append(item)
        else:
            print("Error, item doesn't exist")

    def use_item(self, item):
        now = pg.time.get_ticks()
        if now - self.inventory_click_delay > CLICK_DELAY:
            self.inventory_click_delay = now
            used_item = self.inventory.pop(item)
            if used_item == "Health":
                self.health += 25
                if self.health > PLAYER_HEALTH:
                    self.health = PLAYER_HEALTH

    def update(self):
        self.get_keys()
        self.direction = -self.game.mouse_dir.angle_to(vec(1, 0)) % 360
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.npcs, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_walls(self, self.game.npcs, 'y')
        self.rect.center = self.hit_rect.center

        # Animate character
        now = pg.time.get_ticks()
        if now >= self.walk_frame_time + SPRITE_FRAME_DELAY:
            self.walk_frame_time = now
            # Determine facing by mouse position
            if 90 < self.direction < 270:
                self.facing = "L"
                self.image = self.walk_left[self.update_frame(False)]
            else:
                self.facing = "R"
                self.image = self.walk_right[self.update_frame(False)]
            # Animate movement if character is moving
            if self.vel != vec(0, 0):
                if self.attacking:
                    if self.facing == "R":
                        self.image = self.attack_right[self.update_frame()]
                    else:
                        self.image = self.attack_left[self.update_frame()]
                else:
                    if self.facing == "R":
                        self.image = self.walk_right[self.update_frame()]
                    else:
                        self.image = self.walk_left[self.update_frame()]
            # Animate attacking if character is attacking but standing still
            else:
                if self.attacking:
                    if self.facing == "R":
                        self.image = self.attack_right[self.update_frame(False)]
                    else:
                        self.image = self.attack_left[self.update_frame(False)]


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = {
            "Zombie_r": self.game.spritesheet_z_r.get_image(0, 0, 100, 100),
            "Zombie_l": self.game.spritesheet_z_l.get_image(0, 0, 100, 100)
        }
        for image in self.images:
            self.images[image].set_colorkey(BG_SPRITE_COLOR)
        self.image = self.images["Zombie_r"]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < MOB_AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        if self.health <= 0:
            self.kill()
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(MOB_SPEED)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        if self.vel.x >= 0:
            self.image = self.images["Zombie_r"]
        else:
            self.image = self.images["Zombie_l"]
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


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


# Sprite for Animating weapon attacks
class WeaponAnimation(pg.sprite.Sprite):
    def __init__(self, speed, rotation, type, game, character):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.speed = speed
        self.rot = rotation
        self.frame = 0
        self.frame_rate = 75
        self.type = type
        self.game = game
        self.character = character
        self.rot = -(self.character.direction - WEAPON_ARC + 90) % 360
        self.last_update = pg.time.get_ticks()
        self.image = self.game.weapon_animations[self.type]["Images"][0]
        self.image = pg.transform.rotate(self.image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.game.camera.apply_pos(self.character.rect.center)
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center

    @staticmethod
    def place_rect(angle):
        if 0 <= angle < 90:
            return"TL"
        elif 90 <= angle < 180:
            return "TR"
        elif 180 <= angle < 270:
            return "BR"
        elif 270 <= angle < 360:
            return "BL"

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if self.frame == len(self.game.weapon_animations[self.type]["Images"]):
                self.character.attacking = False
                self.kill()
            else:
                self.image = self.game.weapon_animations[self.type]["Images"][self.frame]
                self.image = pg.transform.rotate(self.image, self.rot)
                self.rect = self.image.get_rect()
                self.rect.center = self.character.rect.center
                self.frame += 1


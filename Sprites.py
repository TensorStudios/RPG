import pygame as pg
import math

from Settings import *


vec = pg.math.Vector2


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


def degreesToRadians(deg):
    return deg/180.0 * math.pi


def draw_circle_arc(screen, color, center, radius, startDeg, endDeg, thickness):
    (x, y) = center
    rect = (x - radius, y - radius, radius * 2, radius * 2)
    startRad = degreesToRadians(startDeg)
    endRad = degreesToRadians(endDeg)

    pg.draw.arc(screen, color, rect, startRad, endRad, thickness)


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.direction = 270.0
        self.health = PLAYER_HEALTH
        self.last_attack = pg.time.get_ticks() - 150
        self.attack_radius = WEAPON_RANGE
        self.attack_speed = WEAPON_SPEED
        self.damage = WEAPON_DAMAGE
        self.attacking = False

    def attack(self):
        # Call animation
        self.attacking = True
        # Find mobs in range
        mobs_in_range = []
        for mob in self.game.mobs:
            if self.pos.distance_squared_to(mob.pos) <= self.attack_radius ** 2:
                mobs_in_range.append(mob)
        # Collide that rectangle with enemy
        now = pg.time.get_ticks()
        # Check if it has been long enough
        if now - WEAPON_SPEED > self.last_attack:
            self.last_attack = now
            # print(f"Player Angle: {self.direction}")
            for mob in mobs_in_range:
                # Check if the mob is within the weapon arc
                # largest degree
                high_angle = (self.direction + WEAPON_ARC) % 360
                # Smallest degree
                low_angle = (self.direction - WEAPON_ARC) % 360
                # The angle of the mob to the player
                mob_angle = (self.pos - mob.pos).normalize()
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
                # else:
                #     print("Not facing the right direction")
                # print(f"High: {high_angle}, Mob angle: {mob_angle}, Low angle: {low_angle}")

    def attack_animation(self):
        # Find points of triangle
        point1 = self.game.camera.apply_pos(self.pos)
        point2 = vec()
        point3 = vec()
        point2.from_polar((WEAPON_RANGE, self.direction + WEAPON_ARC))
        point3.from_polar((WEAPON_RANGE, self.direction - WEAPON_ARC))
        point2 += point1
        point3 += point1
        # print(point1, point2, point3)
        now = pg.time.get_ticks()
        if now - 100 < self.last_attack:
            pg.draw.polygon(self.game.screen, WHITE, [point1, point2, point3])
        else:
            self.attacking = False

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel += vec(-PLAYER_SPEED, 0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel += vec(PLAYER_SPEED, 0)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel += vec(0, -PLAYER_SPEED)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel += vec(0, PLAYER_SPEED)
        if keys[pg.K_SPACE]:
            self.attack()

    def get_direction(self):
        # find what direction the player is facing
        if self.vel != vec(0, 0):
            self.direction = vec(0, 0).angle_to(self.vel.normalize())
            # print(self.direction)

    def update(self):
        self.get_keys()
        self.get_direction()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH

    def update(self):
        if self.health <= 0:
            self.kill()
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


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

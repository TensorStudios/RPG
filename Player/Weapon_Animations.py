import pygame as pg
from Player.PlayerData import PLAYER


class WeaponAnimation(pg.sprite.Sprite):
    def __init__(self, speed, rotation, _type, game, character):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.speed = speed
        self.rot = rotation
        self.frame = 0
        self.frame_rate = 75
        self.type = _type
        self.game = game
        self.character = character
        self.rot = -(self.character.direction - PLAYER["Weapon"]["Arc"] + 90) % 360
        self.last_update = pg.time.get_ticks()
        self.image = self.game.weapon_animations[self.type]["Images"][0]
        self.image = pg.transform.rotate(self.image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.character.rect.center
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
        if self.character.attacking:
            self.rect.center = self.character.rect.center

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

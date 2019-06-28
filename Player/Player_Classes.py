import logging
import pygame as pg
from itertools import cycle
from Settings import *
from NPC import Quests
from Items.Weapons import WEAPONS
from Player.PlayerData import PLAYER, get_exp_requirement
from Player.Weapon_Animations import WeaponAnimation, Arrow
from Sprites import collide_with_walls
from Items.Weapons import WEAPONS
from Items.Armor import ARMOR, HATS
from Items.Consumables import CONSUMABLES

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, weapon="Sword", chest="Armor_1", hat="Hat_1"):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walk_cycle = cycle(range(4))
        self.frame = 0
        PLAYER["Weapon"] = WEAPONS[weapon]
        PLAYER["Chest"] = ARMOR[chest]
        PLAYER["Hat"] = HATS[hat]

        # These variables need to be overwritten in the sub class of the mob
        self.images = {}
        self.walk_right = []
        self.walk_left = []
        self.attack_right = []
        self.attack_left = []
        self.right_click_ability = "Replace Me"
        self.charging = False
        self.health = 0
        self.mana = 0
        self.rot_speed = 0
        self.mana_recharge_timer = 0
        self.rect = 0

        self.walk_frame_time = pg.time.get_ticks() - SPRITE_FRAME_DELAY
        self.hit_rect = PLAYER["Hit Rect"]
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.facing = "R"
        self.direction = 270.0
        self.last_attack = pg.time.get_ticks() - 150
        self.attacking = False
        self.inventory = [
            "Health",
            "Health",
            "Health",
        ]
        self.inventory_click_delay = pg.time.get_ticks()
        self.damage_time = pg.time.get_ticks()
        self.equipped = [WEAPONS[weapon], ARMOR[chest], HATS[hat]]
        self.trained_weapons = ["Bow", "Sword"]
        self.consumable_timeout = pg.time.get_ticks()
        self.consumable_active = None

        # Level Up
        self.level = 1
        self.exp = 0

        # Stats
        self.base_strength = 10
        self.base_dexterity = 10
        self.base_intellect = 10
        self.base_haste = 0
        self.base_mastery = 0
        self.base_armor_value = 0

        # Applied Stats
        self.strength = self.base_strength
        self.dexterity = self.base_dexterity
        self.intellect = self.base_intellect
        self.haste = self.base_haste
        self.mastery = self.base_mastery
        self.armor_value = self.base_armor_value

        logging.info("Player Character Created")

    def __str__(self):
        return "Player Character"

    def update_frame(self, update=True):
        if update:
            self.frame = self.walk_cycle.__next__()
        return self.frame

    def attack(self, ability="Default"):
        # Overwrite this ability with the appropriate class method
        pass

    def take_damage(self, damage):
        now = pg.time.get_ticks()
        # calculate damage reduction from armor. each point of armor = 0.1% damage reduction
        mitigation_factor = 1 - (self.armor_value * PLAYER["Mitigation From Armor"])
        # If there is more than 100% damage reduction, set the reduction to 100%
        if mitigation_factor < 0:
            mitigation_factor = 0
        if now - self.damage_time >= PLAYER["Damage Mitigation Time"]:
            logging.info(f"Player takes {int(damage * mitigation_factor)} damage")
            self.damage_time = now
            self.health -= int(damage * mitigation_factor)

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        movex = False
        movey = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel += vec(-PLAYER["Speed"], 0)
            movex = True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel += vec(PLAYER["Speed"], 0)
            movex = True
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel += vec(0, -PLAYER["Speed"])
            movey = True
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel += vec(0, PLAYER["Speed"])
            movey = True
        if movex and movey:
            self.vel *= 0.7071
        if self.charging:
            self.vel /= 2

        # Attack keys

        if self.game.dialog is False:
            click = pg.mouse.get_pressed()
            if click == (1, 0, 0):
                self.attack()
            if click == (0, 0, 1):
                self.attack(ability=self.right_click_ability)
            if click == (0, 0, 0):
                self.charging = False

    def get_direction(self):
        # find what direction the player is facing
        if self.vel != vec(0, 0):
            self.direction = vec(0, 0).angle_to(self.vel.normalize())
            logging.debug(f"player facing {self.direction}")

    def add_item(self, item):
        if item in INVENTORY_TYPES:
            self.inventory.append(item)
            logging.info(f"{item} added to inventory")
        else:
            logging.info(f"Error, item doesn't exist: {item} perhaps it needs to be added to INVENTORY_TYPES")
            print(f"Error, item doesn't exist: {item} perhaps it needs to be added to INVENTORY_TYPES")

    def use_item(self, item, drop=False):
        now = pg.time.get_ticks()
        if now - self.inventory_click_delay > CLICK_DELAY:
            self.inventory_click_delay = now
            used_item = self.inventory.pop(item)
            if drop is True:
                used_item = None

            # If item is a consumable
            if used_item in CONSUMABLES:
                if CONSUMABLES[used_item]["Effect Duration"] is None:
                    if CONSUMABLES[used_item]["Effect Type"] == "Heal":
                        self.health += CONSUMABLES[used_item]["Effect Value"]
                        if self.health > PLAYER["Health"]:
                            self.health = PLAYER["Health"]
                else:
                    self.consumable_timeout = pg.time.get_ticks() + CONSUMABLES[used_item]["Effect Duration"]
                    self.consumable_active = used_item

            # If item is equipment
            elif used_item in ARMOR:
                # add former item to inventory
                self.add_item(PLAYER["Chest"]["Name"])

                # equip Item
                PLAYER["Chest"] = ARMOR[used_item]
            elif used_item in HATS:
                # add former item to inventory
                self.add_item(PLAYER["Hat"]["Name"])

                # equip Item
                PLAYER["Hat"] = HATS[used_item]
            elif used_item in WEAPONS:
                if WEAPONS[used_item]["Type"] in self.trained_weapons:
                    # add former item to inventory
                    self.add_item(PLAYER["Weapon"]["Name"])

                    # equip Item
                    PLAYER["Weapon"] = WEAPONS[used_item]
                else:
                    logging.info(f"You cannot equip {WEAPONS[used_item]['Type']}")
                    print(f"You cannot equip {WEAPONS[used_item]['Type']}")
                    self.add_item(used_item)

            else:
                if used_item is None:
                    print("Item was dropped")
                else:
                    print("Something went wrong")
            print("Item used:", used_item)

            # For Debugging only uncomment to see stats as gear changes
            self.apply_stats_from_gear()
            print(f"Stats: STR: {self.strength}, DEX: {self.dexterity}, HASTE: {self.haste}")
            print(f"Equipped items: {self.equipped[0]['Name'], self.equipped[1]['Name'], self.equipped[2]['Name']}")

    def collect_exp(self, exp):
        self.exp += exp
        logging.info(f"Player has gained {exp} exp and now has {self.exp} exp")
        logging.info(f"current level: {self.level}, exp needed: {get_exp_requirement(self.level)}")
        if self.level < 100:
            while self.exp >= get_exp_requirement(self.level):
                self.exp -= get_exp_requirement(self.level)
                self.level += 1
                PLAYER["Health"] += PLAYER["Level Up"]["Health Increase"]
                self.health = PLAYER["Health"]
                self.apply_stats_from_levelup(PLAYER["Level Up"]["STR Increase"],
                                              PLAYER["Level Up"]["DEX Increase"],
                                              PLAYER["Level Up"]["INT Increase"],)
                logging.info(f"Player has leveled up to {self.level}")
                logging.info(f"Player health has increased to {PLAYER['Health']}")

    def recharge_mana(self):
        now = pg.time.get_ticks()
        if now - self.mana_recharge_timer > self.mana_recharge:
            self.mana_recharge_timer = now
            self.mana += 1
            if self.mana >= PLAYER["Mana"]:
                self.mana = PLAYER["Mana"]

    def calculate_haste(self, base_speed):
        haste_increase = (1000 / base_speed) * (1 + (self.haste / 1000))
        return 1000 / haste_increase

    def apply_stats_from_gear(self):
        self.equipped = [PLAYER["Weapon"], PLAYER["Chest"], PLAYER["Hat"]]
        self.strength = self.base_strength
        self.dexterity = self.base_dexterity
        self.intellect = self.base_intellect
        self.haste = self.base_haste
        self.mastery = self.base_mastery
        self.armor_value = self.base_armor_value

        for item in self.equipped:
            self.strength += item["STR"]
            self.dexterity += item["DEX"]
            self.intellect += item["INT"]
            self.haste += item["HASTE"]
            self.mastery += item["MASTERY"]
            self.armor_value += item["Armor_value"]

    def apply_stats_from_levelup(self, strength=0, dexterity=0, intellect=0, haste=0, mastery=0):
        self.base_strength += strength
        self.base_dexterity += dexterity
        self.base_intellect += intellect
        self.haste += haste
        self.mastery += mastery

    def update(self):
        # Recharge Mana
        self.recharge_mana()

        self.apply_stats_from_gear()

        # Check for active consumables
        if self.consumable_active is not None:
            # Check if the duration has expired
            if pg.time.get_ticks() <= self.consumable_timeout:
                if self.consumable_active == "Haste":
                    self.haste += CONSUMABLES["Haste"]["Effect Value"]
                if self.consumable_active == "Armor":
                    self.armor_value += CONSUMABLES["Armor"]["Effect Value"]
            # If the duration has expired, reset the active potion
            else:
                self.consumable_active = None
                self.consumable_timeout = None

        self.inventory.sort()

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


class Knight(Player):
    def __init__(self, game, x, y):
        Player.__init__(self, game, x, y, "Sword", "Armor_1", "Hat_1")
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
        self.right_click_ability = "Fire Attack"

        # These commands need to be placed in each class
        self.image = self.walk_right[self.frame]
        for image in self.images:
            self.images[image].set_colorkey(BG_SPRITE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect.center = self.rect.center
        self.right_click_ability = "Fire Attack"
        self.trained_weapons = ["Swrod"]

        # stats
        self.health = PLAYER["Health"]
        self.mana = PLAYER["Mana"]
        self.mana_recharge = PLAYER["Mana Recharge"]
        self.mana_recharge_timer = pg.time.get_ticks()
        self.attack_radius = PLAYER["Weapon"]["Range"]
        self.attack_speed = PLAYER["Weapon"]["Speed"]
        self.damage = PLAYER["Weapon"]["Damage"]

    def attack(self, ability="Default"):
        # Find mobs in range
        ability_modifier = PLAYER["Abilities"][ability]["Damage Modifier"]
        mobs_in_range = []
        for mob in self.game.mobs:
            if self.pos.distance_squared_to(mob.pos) <= self.attack_radius ** 2:
                mobs_in_range.append(mob)
        # Check if player has enough mana
        cost = PLAYER["Abilities"][ability]["Mana Cost"] < self.mana
        # Check if it has been long enough
        now = pg.time.get_ticks()
        if now - self.calculate_haste(self.attack_speed) > self.last_attack and cost is True:
            # Toggle animation flag
            self.attacking = True
            self.last_attack = now
            logging.debug("player attacks")
            # spend mana cost of ability
            self.mana -= PLAYER["Abilities"][ability]["Mana Cost"]
            # Character Attack Pose
            if self.facing == "R":
                self.image = self.attack_right[self.update_frame()]
            else:
                self.image = self.attack_left[self.update_frame()]

            # Spawn Weapon Animation
            logging.debug("spawning weapon animation")
            if ability == "Fire Attack":
                logging.debug("Fire Weapon Animation")
                WeaponAnimation(self.attack_speed, self.direction, "fire sword", self.game, self)
            elif ability == "Default":
                logging.debug("Normal Weapon Animation")
                WeaponAnimation(self.attack_speed, self.direction, "sword", self.game, self)
            else:
                logging.warning(f"An inproper player ability was called: {ability}")
                WeaponAnimation(self.attack_speed, self.direction, "sword", self.game, self)

            # Target enemies by mouse
            for mob in mobs_in_range:
                if mob.targeted:
                    logging.debug("hit connects")
                    damage = int(self.damage * self.strength / 10 * ability_modifier)
                    logging.info(f"hit connects for {damage} damage")
                    mob.take_damage(damage)

            # # Hit all mobs in range
            # for mob in mobs_in_range:
            #     # Check if the mob is within the weapon arc
            #     # largest degree
            #     high_angle = (self.direction + self.attack_arc) % 360
            #     # Smallest degree
            #     low_angle = (self.direction - self.attack_arc) % 360
            #     # The angle of the mob to the player
            #     mob_angle = (self.pos - mob.pos).normalize()
            #     # Add 180 degrees to make it easy to compare angles
            #     mob_angle = vec(0, 0).angle_to(mob_angle) + 180
            #
            #     # See if the mob angle is within the two angles
            #     if high_angle >= mob_angle >= low_angle:
            #         logging.debug("hit connects")
            #         mob.health -= self.damage
            #     # account for if the mob is at a high angle and high_angle is at a low value
            #     elif high_angle < 90:
            #         if mob_angle >= 315:
            #             mob_angle -= 360
            #         low_angle -= 360
            #         if high_angle >= mob_angle >= low_angle:
            #             damage = int(self.damage * self.damage_modifier * ability_modifier)
            #             logging.info(f"hit connects for {damage} damage")
            #             mob.health -= damage


class Ranger(Player):
    def __init__(self, game, x, y):
        Player.__init__(self, game, x, y, "Bow", "Light_1", "Hat_1")
        self.images = {
            "Walk_r_1": self.game.spritesheet_r_r.get_image(0, 0, 100, 100),
            "Walk_r_2": self.game.spritesheet_r_r.get_image(100, 0, 100, 100),
            "Walk_r_3": self.game.spritesheet_r_r.get_image(0, 100, 100, 100),
            "Walk_r_4": self.game.spritesheet_r_r.get_image(100, 100, 100, 100),
            "Walk_l_1": self.game.spritesheet_r_l.get_image(0, 0, 100, 100),
            "Walk_l_2": self.game.spritesheet_r_l.get_image(100, 0, 100, 100),
            "Walk_l_3": self.game.spritesheet_r_l.get_image(0, 100, 100, 100),
            "Walk_l_4": self.game.spritesheet_r_l.get_image(100, 100, 100, 100),
            "Attack_r_1": self.game.spritesheet_r_r.get_image(0, 0, 100, 100),
            "Attack_r_2": self.game.spritesheet_r_r.get_image(100, 0, 100, 100),
            "Attack_r_3": self.game.spritesheet_r_r.get_image(0, 100, 100, 100),
            "Attack_r_4": self.game.spritesheet_r_r.get_image(100, 100, 100, 100),
            "Attack_l_1": self.game.spritesheet_r_l.get_image(0, 0, 100, 100),
            "Attack_l_2": self.game.spritesheet_r_l.get_image(100, 0, 100, 100),
            "Attack_l_3": self.game.spritesheet_r_l.get_image(0, 100, 100, 100),
            "Attack_l_4": self.game.spritesheet_r_l.get_image(100, 100, 100, 100),
        }
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
        self.right_click_ability = "Default"

        # These commands need to be placed in each class
        self.image = self.walk_right[self.frame]
        for image in self.images:
            self.images[image].set_colorkey(BG_SPRITE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect.center = self.rect.center
        self.right_click_ability = "Charged Shot"
        self.trained_weapons = ["Bow"]

        # stats
        self.health = PLAYER["Health"]
        self.mana = PLAYER["Mana"]
        self.mana_recharge = PLAYER["Mana Recharge"]
        self.mana_recharge_timer = pg.time.get_ticks()
        self.attack_speed = PLAYER["Weapon"]["Speed"]
        self.damage = PLAYER["Weapon"]["Damage"]

        # Charging attack
        self.charging = False
        self.charge_start = pg.time.get_ticks()
        self.charge_last = pg.time.get_ticks()
        self.charge_time = 1000

    def attack(self, ability="Default"):
        # Find mobs in range
        ability_modifier = PLAYER["Abilities"][ability]["Damage Modifier"]
        # Check if player has enough mana
        cost = PLAYER["Abilities"][ability]["Mana Cost"] < self.mana
        # Check if it has been long enough
        now = pg.time.get_ticks()
        if now - self.calculate_haste(self.attack_speed) > self.last_attack and cost is True:
            # Toggle animation flag
            self.attacking = True
            self.last_attack = now
            logging.debug("player attacks")
            # spend mana cost of ability
            # Character Attack Pose
            if self.facing == "R":
                self.image = self.attack_right[self.update_frame()]
            else:
                self.image = self.attack_left[self.update_frame()]

            # Calculate default damage
            if ability == "Default":
                damage = int(self.damage * self.dexterity / 10 * ability_modifier)
                logging.debug("Spawning Arrow sprite")
                _dir = -self.game.mouse_dir.angle_to(vec(1, 0)) % 360
                self.mana -= PLAYER["Abilities"][ability]["Mana Cost"]
                Arrow(self.game, self.rect.center, _dir, damage)

        # handle_charged shot
        if ability == "Charged Shot":
            if not self.charging:
                self.charging = True
                self.charge_start = pg.time.get_ticks()
                self.charge_last = pg.time.get_ticks()
            else:
                now = pg.time.get_ticks()
                # check if the mouse button has been lifted up
                if now - self.charge_last > 25:
                    # print(now - self.charge_last)
                    # print("timed out")
                    self.charging = False
                # check if the charge time has been completed
                elif now - self.charge_start >= self.calculate_haste(self.charge_time):
                    self.mana -= PLAYER["Abilities"][ability]["Mana Cost"]
                    if self.mana < 0:
                        self.mana = 0
                    damage = int(self.damage * self.dexterity / 5 * ability_modifier)
                    self.charging = False
                    logging.debug("Spawning Arrow sprite")
                    _dir = -self.game.mouse_dir.angle_to(vec(1, 0)) % 360
                    Arrow(self.game, self.rect.center, _dir, damage)
                    # print("Shooting")
                # if the mouse button is still pressed and the time is not up
                else:
                    self.charge_last = now
                    # print("Charging up")

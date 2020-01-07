import pygame as pg
import logging
import math
from itertools import cycle
from Settings import *
from Sprites import collide_with_walls, collide_hit_rect
from NPC import Quests
import json

with open("NPC/conversations.json") as json_file:
    NPC_id = json.load(json_file)
vec = pg.math.Vector2


# Master class for NPC
class NonPlayerCharacter(pg.sprite.Sprite):
    def __init__(self, game, x, y, ID):
        self.groups = game.all_sprites, game.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # When you subclass an NPC, be sure to add in proper images
        self.images = {
            "Example": "example"
        }
        # Remember to set the colorkey for the image just like this:
        # I think this i
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
        self.id = ID
        self.quest_id = None
        self.dialog_shortcut = None # We will need to pass in the relevant quest or conversation location
        self.dialog_next = None

    # Check if the NPC was clicked and the player is close enough. Also checks if the player has walked away
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
        if dist.length() > SPEAK_RANGE and self.active:
            self.active = False
            self.reset_dialog()

    # Will reset the dialog data
    def reset_dialog(self):
        self.game.dialog = False
        self.game.dialog_selection = None
        self.game.dialog_link = None
        self.game.dialog_tags = None
        self.game.dialog_end_d = None
        self.game.dialog_text = ""
        self.game.dialog_options = []
        self.dialog_step = None
        self.active = False

    # Used by main.py to get the text and options to display
    def get_dialog_text_and_options(self):
        # If the NPC should be at the "Empty Dialog screen"
        if self.dialog_step is None:
            text = NPC_id[str(self.id)]["Default Text"]
            option_num = 1
            options = {}
            # Loop Through conversations for NPC and add the Node if it is active
            link_correction = lambda x: x if x is not None else "Step 1"
            for conv_id, values in NPC_id[str(self.id)]["Conversations"].items():
                if NPC_id[str(self.id)]["Conversations"][conv_id]["Active"] is True:
                    options[option_num] = {
                        "Text": NPC_id[str(self.id)]["Conversations"][conv_id]["Node Title"],
                        "Link": ["Conversations", conv_id, link_correction(self.dialog_step)],
                        "Tags": [],
                        "End Dialog": True,
                    }
                    option_num += 1
            # Loop Through Quests for NPC and add the Node if it is active
            for quest_id, values in NPC_id[str(self.id)]["Quests"].items():
                if NPC_id[str(self.id)]["Quests"][quest_id]["Active"] is True:
                    options[option_num] = {
                        "Text": NPC_id[str(self.id)]["Quests"][quest_id]["Node Title"],
                        "Link": ["Quests", quest_id, link_correction(self.dialog_step)],
                        "Tags": [],
                        "End Dialog": True,
                    }
                    option_num += 1
            options[option_num] = {
                "Text": "Bye",
                "Link": None,
                "Tags": [],
                "End Dialog": True
            }

        # If the NPC should be into a conversation
        else:
            text = self.dialog_shortcut["Text"]
            options = self.dialog_shortcut["Options"]

        return text, options

    # Fill this in!
    # Handle the dialog user interface
    def handle_dialog(self, *args):
        pass

    # Fill this in!
    # Update the npc on the screen
    def update(self):
        pass


class QuestNPC(NonPlayerCharacter):
    def __init__(self, game, x, y, ID):
        NonPlayerCharacter.__init__(self, game, x, y, ID)
        self.images = {
            "NPC_r": self.game.spritesheet_k_r.get_image(0, 0, 100, 100)
        }
        self.image = self.images["NPC_r"]
        for image in self.images:
            self.images[image].set_colorkey(BG_SPRITE_COLOR)
        self.id = ID
        self.dialog_step = None
        self.default_text = "Hello Traveler"

    def handle_dialog(self, quest, conv_link, end_dialog, tags, force_close=False):
        # Handle dialog on "Empty" Screen
        # logging.info("Quest: ", quest, "conv link: ", conv_link, "Dialog Step: ", self.dialog_step)
        if force_close:
            self.reset_dialog()
        else:
            if self.dialog_step is None:
                logging.info("Handling empty dialog screen")
                self.dialog_shortcut = NPC_id[str(self.id)][self.game.dialog_link[0]][self.game.dialog_link[1]][self.game.dialog_link[2]]
                dialog_step = self.game.dialog_link[2]
                self.reset_dialog()
                self.active = True
                self.dialog_step = dialog_step

            # Handle dialog in quest or conv screens
            else:
                logging.info(f"Tags: {tags}")
                self.quest_id = quest
                # set the dialog shortcut so that it properly displays the text
                self.dialog_next = NPC_id[str(self.id)][conv_link[0]][str(conv_link[1])]["Next"]
                if conv_link[0] == "Conversations" and conv_link[2] is not None:
                    self.dialog_step = NPC_id[str(self.id)]["Conversations"][str(conv_link[1])][conv_link[2]]
                    self.dialog_shortcut = NPC_id[str(self.id)]["Conversations"][str(conv_link[1])][conv_link[2]]
                if end_dialog:
                    self.reset_dialog()
                else:
                    dialog_step = self.game.dialog_link[2]
                    self.reset_dialog()
                    self.dialog_step = dialog_step
                    self.active = True

                # Handle Non-Quest Tags Here
                if "Deactivate" in tags:
                    NPC_id[str(self.id)][conv_link[0]][str(conv_link[1])]["Active"] = False
                    if self.dialog_next is not None:
                        NPC_id[str(self.id)][conv_link[0]][str(self.dialog_next)]["Active"] = True
                if "Health" in tags:
                    logging.info("Giving Player Health")
                    self.game.player.add_item("Health")

                # Handle Quests here
                if self.quest_id is not None:
                    if "Start" in tags:
                        quest_step = Quests.change_quest_status(self.quest_id, "Active")
                        self.dialog_step = NPC_id[str(self.id)]["Quests"][str(conv_link[1])][quest_step]
                        self.dialog_shortcut = NPC_id[str(self.id)]["Quests"][str(conv_link[1])][quest_step]
                    if "Cancel" in tags:
                        quest_step = Quests.update_quest_progress(self.quest_id, abandon=True)
                        self.dialog_step = NPC_id[str(self.id)]["Quests"][str(conv_link[1])][quest_step]
                        self.dialog_shortcut = NPC_id[str(self.id)]["Quests"][str(conv_link[1])][quest_step]
                    if "Close" in tags:
                        quest_step = Quests.change_quest_status(self.quest_id, "Close")
                        NPC_id[str(self.id)][conv_link[0]][str(conv_link[1])]["Active"] = False
                        self.handle_quest_reward()
                        self.quest_id = None
                    if self.quest_id is not None and Quests.check_quest_progress(self.quest_id):
                        Quests.change_quest_status(self.quest_id, "Complete")

    def handle_quest_reward(self):
        reward = Quests.Quests["Quest ID"][self.quest_id]["Reward"]

        # This is duplicate code, it can be consolidated with handle_dialog
        if reward == "Health":
            logging.info("Rewarding player with Health")
            self.game.player.add_item("Health")
        else:
            logging.warning("This reward has not been added to the code yet")

    # Check if quest is complete
    def quest_status(self):
        if self.quest_id is not None:
            if Quests.check_quest_progress(self.quest_id):
                quest_step = Quests.change_quest_status(self.quest_id, "Complete")
                self.dialog_step = NPC_id[str(self.id)]["Quests"][str(self.quest_id)][quest_step]
                self.dialog_shortcut = NPC_id[str(self.id)]["Quests"][str(self.quest_id)][quest_step]

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
            # If player has accepted quest, check if quest is complete
            self.quest_status()

            # If this NPC has been clicked, but not options have been selected, tell the game what to display
            if self.game.dialog_selection is None:
                self.game.dialog = True
                self.game.dialog_text, self.game.dialog_options = self.get_dialog_text_and_options()
            else:
                if self.game.dialog_link is None:
                    self.handle_dialog(quest=None,
                                       conv_link=self.game.dialog_selection,
                                       end_dialog=True,
                                       tags=[],
                                       force_close=True)

                elif self.game.dialog_link[0] == "Conversations":
                    # Handle conversation close
                    if self.dialog_step is None:
                        self.handle_dialog(quest=None,
                                           conv_link=self.game.dialog_link,
                                           end_dialog=True,
                                           tags=[])

                    # Handle Normal conversaiton
                    else:
                        self.handle_dialog(quest=None,
                                           conv_link=self.game.dialog_link,
                                           end_dialog=self.game.dialog_end_d,
                                           tags=self.game.dialog_tags)
                # Handle quests here
                elif self.game.dialog_link[0] == "Quests":
                    quest = self.game.dialog_link[1]

                    # Handle conversation close
                    if self.dialog_step is None:
                        self.handle_dialog(quest=quest,
                                           conv_link=self.game.dialog_link,
                                           end_dialog=True,
                                           tags=[])

                    # Handle Normal quest dialog
                    else:
                        self.handle_dialog(quest=quest,
                                           conv_link=self.game.dialog_link,
                                           end_dialog=self.game.dialog_end_d,
                                           tags=self.game.dialog_tags)

import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
LIGHTGREEN = (0, 200, 0)
RED = (255, 0, 0)
LIGHTRED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# # Player Settings
# PLAYER_SPEED = 600
# PLAYER_HIT_RECT = pg.Rect(0, 0, 60, 90)
# PLAYER_HEALTH = 100
# PLAYER_DAMAGE_MITIGATION_TIME = 100
#
# # Weapon Settings
# WEAPON_RANGE = 200
# WEAPON_SPEED = 500
# WEAPON_DAMAGE = 25
# WEAPON_ARC = 45

# Mob Settings
MOB_HIT_RECT = pg.Rect(0, 0, 35, 70)
MOB_SPEED = 50
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
DETECT_RADIUS = 400
MOB_AVOID_RADIUS = 100
PATROL_CHANGE_TIME = 3000
MOB_EXP = 5

# NPC Settings
NPC_HIT_RECT = pg.Rect(0, 0, 60, 60)
NPC_HEALTH = 10
NPC_SPEED = 0
SPEAK_RANGE = 125

# Layers
PLAYER_LAYER = 3
ITEM_LAYER = 2
ATTACK_LAYER = 2
WALL_LAYER = 1

# Character Sprite Animation
SPRITE_FRAME_DELAY = 125
BG_SPRITE_COLOR = (94, 80, 80)
WEAPON_RECT = pg.Rect(0, 0, 80, 80)

# Inventory
CLICK_DELAY = 500
INVENTORY_TYPES = [
    "Health",
    "Armor_1",
    "Armor_2",
    "Light_1",
    "Light_2",
    "Hat_1",
    "Hat_2",
    "Sword",
    "Sword_rare",
    "Bow",
    "Bow_rare"
]

# Items
ITEM_IMAGES = {'health': 'health_pack.png'}

# Item Drop Rate
DROP_RATE = 0.5

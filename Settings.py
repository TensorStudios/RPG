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

# Player Settings
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0, 0, 60, 60)
PLAYER_HEALTH = 100
PLAYER_ATTACK_DELAY = 500

# Weapon Settings
WEAPON_RANGE = 200
WEAPON_SPEED = 500
WEAPON_DAMAGE = 25
WEAPON_ARC = 45

# Mob Settings
MOB_HIT_RECT = pg.Rect(0, 0, 35, 35)
MOB_SPEED = 250
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
DETECT_RADIUS = 400

# Layers
PLAYER_LAYER = 3
ATTACK_LAYER = 2
WALL_LAYER = 1

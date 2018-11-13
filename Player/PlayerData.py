import pygame as pg
from Items import Weapons

PLAYER = {
    "Speed": 600,
    "Hit Rect": pg.Rect(0, 0, 60, 90),
    "Health": 100,
    "Damage Mitigation Time": 100,
    "Weapon": Weapons.WEAPONS["Sword"],
    "Level Up": {
        "Exp Required": 5,
        "Dmg Increase": 1.1, # Percentage increase
        "Health Increase": 5
    }
}

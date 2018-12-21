import pygame as pg
from Items import Weapons

PLAYER = {
    "Speed": 600,
    "Hit Rect": pg.Rect(0, 0, 60, 90),
    "Health": 100,
    "Mana": 50,
    "Mana Recharge": 200,
    "Damage Mitigation Time": 100,
    "Weapon": Weapons.WEAPONS["Sword"],
    "Abilities": {
        "Fire Attack": {
            "Damage Modifier": 2,
            "Mana Cost": 20
        },
        "Default": {
            "Damage Modifier": 1,
            "Mana Cost": 0
        }
    },
    "Level Up": {
        "Exp Required": 5,
        "Dmg Increase": 1.1, # Percentage increase
        "Health Increase": 5
    }
}


def get_exp_requirement(level):
    return level * 5

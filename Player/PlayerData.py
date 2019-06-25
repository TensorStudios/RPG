import pygame as pg
from Items import Weapons
from Items import Armor

PLAYER = {
    "Speed": 600,
    "Hit Rect": pg.Rect(0, 0, 60, 90),
    "Health": 100,
    "Mana": 50,
    "Mana Recharge": 200,
    "Damage Mitigation Time": 100,
    "Weapon": Weapons.WEAPONS["Sword"],
    "Chest": Armor.ARMOR["Armor_1"],
    "Hat": Armor.ARMOR["Hat_1"],
    "Abilities": {
        "Fire Attack": {
            "Damage Modifier": 1.5,
            "Mana Cost": 20
        },
        "Default": {
            "Damage Modifier": 1,
            "Mana Cost": 0
        },
        "Charged Shot": {
            "Damage Modifier": 1.5,
            "Mana Cost": 5
        }
    },
    "Level Up": {
        "Exp Required": 5,
        "STR Increase": 1,
        "DEX Increase": 1,
        "INT Increase": 1,
        "Health Increase": 5
    }
}


def get_exp_requirement(level):
    if level == 1:
        return 10
    elif 1 < level < 5:
        return round(10 * (1.81 ** (level - 1)))
    elif 4 < level < 10:
        return round(59 * (1.2165 ** (level - 4)))
    elif 9 < level < 50:
        return round(158 * (1.1090550 ** (level - 9)))
    elif 49 < level < 55:
        return round(9925 * (1.063975 ** (level - 49)))
    elif 54 < level < 60:
        return round(13532 * (1.056363 ** (level - 54)))
    elif 59 < level < 100:
        return round(17801 * (1.00315265 ** (level - 59)))


if __name__ == "__main__":
    total_xp = 0
    for x in range(1, 101):
        exp = get_exp_requirement(x)
        print(f"Level {x}: {exp}")
        total_xp += exp
    print(total_xp)

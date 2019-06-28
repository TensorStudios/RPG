# First three letters are the type for identifying later

WEAPONS = {
    "Sword": {
        "Name": "Sword",
        "Type": "Sword",
        "Range": 200,
        "Speed": 500,
        "Damage": 10,
        "Arc": 45,
        "STR": 50,
        "INT": 0,
        "DEX": 0,
        "HASTE": 50,
        "MASTERY": 50,
        "Armor_value": 0,
    },
    "Sword_rare": {
        "Name": "Sword_rare",
        "Type": "Sword",
        "Range": 200,
        "Speed": 500,
        "Damage": 20,
        "Arc": 45,
        "STR": 100,
        "INT": 0,
        "DEX": 0,
        "HASTE": 100,
        "MASTERY": 100,
        "Armor_value": 0,
    },
    "Bow": {
        "Name": "Bow",
        "Type": "Bow",
        "Speed": 500,
        "Damage": 10,
        "STR": 0,
        "INT": 0,
        "DEX": 50,
        "HASTE": 50,
        "MASTERY": 0,
        "Armor_value": 0,
    },
    "Bow_rare": {
        "Name": "Bow_rare",
        "Type": "Bow",
        "Speed": 500,
        "Damage": 20,
        "STR": 0,
        "INT": 0,
        "DEX": 100,
        "HASTE": 100,
        "MASTERY": 0,
        "Armor_value": 0,
    },
}
print(type(WEAPONS))
import csv

ARMOR = {}
WEAPONS = {}
HATS = {}

with open("Items/Armor.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        for key, value in row.items():
            try:
                row[key] = int(value)
            except ValueError:
                continue
        ARMOR[row["Name"]] = row
with open("Items/Weapons.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        for key, value in row.items():
            try:
                row[key] = int(value)
            except ValueError:
                continue
        WEAPONS[row["Name"]] = row
with open("Items/Hats.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        for key, value in row.items():
            try:
                row[key] = int(value)
            except ValueError:
                continue
        HATS[row["Name"]] = row

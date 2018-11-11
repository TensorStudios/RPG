import logging

"""
Another .json type file

Information on quests, can be altered by NPCs in  the game
"""

Quests = {
    "Quest ID": {
        0: {
            "Available": True,
            "Status": "Not started",
            "Linked Quest": None,
            "Start NPC ID": 2,
            "End NPC ID": 2,
            "Prerequisites": None,
            "Requirement": {
                "Description": "Kill 5 Zombies",
                "Counter": 0,
                "Goal": 5
            },
            "Reward": "Health",
            "Complete": False
        },
        1: {
            "Available": False,
            "Status": "Not Started",
            "Linked Quest": 1,
            "Start NPC ID": 2,
            "End NPC ID": 2,
            "Prerequisites": None,
            "Requirement": {
                "Description": "Deliver 5 Health packs",
                "Counter": 0,
                "Goal": 5
            },
            "Reward": "Health",
            "Complete": False
        }
    }
}

QUEST_STATUS = {
    "Not Started": [],
    "Active": [],
    "Complete": []
}


def refresh_quests():
    for status in QUEST_STATUS:
        status = []
    for quest_id, quest in enumerate(Quests["Quest ID"]):
        if quest["Status"] == "Not started" and quest_id not in QUEST_STATUS["Not Started"]:
            QUEST_STATUS["Not Started"].append(quest_id)
        if quest["Status"] == "Active" and quest_id not in QUEST_STATUS["Active"]:
            QUEST_STATUS["Active"].append(quest_id)
        if quest["Status"] == "Complete" and quest_id not in QUEST_STATUS["Complete"]:
            QUEST_STATUS["Complete"].append(quest_id)


def change_quest_status(quest_id, status):
    Quests["Quest ID"][quest_id]["Status"] = status
    refresh_quests()


if __name__ == "__main__":
    refresh_quests()

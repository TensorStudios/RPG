import logging

"""
Another .json type file

Information on quests, can be altered by NPCs in  the game
"""

# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

Quests = {
    "Quest ID": {
        1: {
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
        },
        2: {
            "Available": False,
            "Status": "Not started",
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
        }
    }
}

QUEST_STATUS = {
    "Not Started": [],
    "Active": [],
    "Complete": []
}


def refresh_quests():
    QUEST_STATUS["Not Started"] = []
    QUEST_STATUS["Active"] = []
    QUEST_STATUS["Complete"] = []

    for quest_id, quest in Quests["Quest ID"].items():
        if quest["Status"] == "Not started" and quest_id not in QUEST_STATUS["Not Started"]:
            QUEST_STATUS["Not Started"].append(quest_id)
        if quest["Status"] == "Active" and quest_id not in QUEST_STATUS["Active"]:
            QUEST_STATUS["Active"].append(quest_id)
        if quest["Status"] == "Complete" and quest_id not in QUEST_STATUS["Complete"]:
            QUEST_STATUS["Complete"].append(quest_id)
    logging.debug(f"Quest ID's Not Started: {QUEST_STATUS['Not Started']}")
    logging.debug(f"Quest ID's Active: {QUEST_STATUS['Active']}")
    logging.debug(f"Quest ID's Completed: {QUEST_STATUS['Complete']}")


def change_quest_status(quest_id, status):
    assert status in ["Not started", "Active", "Complete"]
    logging.info(f"Changing Status of quest id: {quest_id} to {status}")
    Quests["Quest ID"][quest_id]["Status"] = status
    refresh_quests()

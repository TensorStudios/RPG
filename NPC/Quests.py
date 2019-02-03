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
            "Status": "Not Started",
            "Linked Quest": None,
            "Start NPC ID": 2,
            "End NPC ID": 2,
            "Prerequisites": None,
            "Conv Links": {
                "Not Started": 1,
                "Active": 2,
                "Complete": 4,
                "Close": 5
            },
            "Requirement": {
                "Description": "Kill 5 Zombies",
                "Counter": 0,
                "Goal": 1
            },
            "Reward": "Health",
        },
        2: {
            "Available": False,
            "Status": "Not Started",
            "Linked Quest": 1,
            "Start NPC ID": 2,
            "End NPC ID": 2,
            "Prerequisites": None,
            "Conv Links": {
                "Not Started": 5,
                "Active": 5,
                "Complete": 5,
                "Close": 5
            },
            "Requirement": {
                "Description": "Deliver 5 Health packs",
                "Counter": 0,
                "Goal": 5
            },
            "Reward": "Health",
        }
    },
    3: {
        "Available": True,
        "Status": "Not Started",
        "Linked Quest": None,
        "Start NPC ID": 1,
        "End NPC ID": 1,
        "Prerequisites": None,
        "Conv Links": {
            "Not Started": 1,
            "Active": 2,
            "Complete": 3,
            "Close": 5
        },
        "Requirement": {
            "Description": "Get a healthpack",
            "Counter": 0,
            "Goal": 1
        },
        "Reward": "Health",
    }
}

QUEST_STATUS = {
    "Not Started": [],
    "Active": [],
    "Complete": [],
    "Close": []
}


def refresh_quests():
    QUEST_STATUS["Not Started"] = []
    QUEST_STATUS["Active"] = []
    QUEST_STATUS["Complete"] = []
    QUEST_STATUS["Close"] = []

    for quest_id, quest in Quests["Quest ID"].items():
        if quest["Status"] == "Not Started" and quest_id not in QUEST_STATUS["Not Started"]:
            QUEST_STATUS["Not Started"].append(quest_id)
        if quest["Status"] == "Active" and quest_id not in QUEST_STATUS["Active"]:
            QUEST_STATUS["Active"].append(quest_id)
        if quest["Status"] == "Complete" and quest_id not in QUEST_STATUS["Complete"]:
            QUEST_STATUS["Complete"].append(quest_id)
        if quest["Status"] == "Close" and quest_id not in QUEST_STATUS["Close"]:
            QUEST_STATUS["Close"].append(quest_id)
    logging.info(f"Quest ID's Not Started: {QUEST_STATUS['Not Started']}")
    logging.info(f"Quest ID's Active: {QUEST_STATUS['Active']}")
    logging.info(f"Quest ID's Completed: {QUEST_STATUS['Complete']}")
    logging.info(f"Quest ID's Closed: {QUEST_STATUS['Close']}")


def change_quest_status(quest_id, status):
    assert status in ["Not Started", "Active", "Complete", "Close"]
    logging.info(f"Changing Status of quest id: {quest_id} to {status}")
    Quests["Quest ID"][quest_id]["Status"] = status
    refresh_quests()
    return Quests["Quest ID"][quest_id]["Conv Links"][status]


def check_quest_progress(quest_id):
    logging.debug(f"Checking Quest Status for quest id: {quest_id}")
    quest = Quests["Quest ID"][quest_id]
    if quest["Status"] == "Active":
        if quest["Requirement"]["Counter"] == quest["Requirement"]["Goal"]:
            logging.debug(f"quest id: {quest_id} has met all of it's requirements")
            return True
        else:
            logging.debug(f"quest id: {quest_id} has not met all of it's requirements")
            return False
    elif quest["Status"] == "Complete":
        return True
    else:
        logging.debug(f"quest id: {quest_id} is not active")


def update_quest_progress(quest_id, amount=0, abandon=False):
    quest = Quests["Quest ID"][quest_id]

    # Abandon quest if flag is True
    if abandon:
        logging.info(f"Abandoning quest id: {quest_id}")
        change_quest_status(quest_id, "Not Started")
        return Quests["Quest ID"][quest_id]["Conv Links"]["Not Started"]
        # If I abandon a quest once I have completed some of the requirements, should the requirements be saved?

    # Update quest requirement counter with amount
    if quest["Status"] == "Active":
        quest["Requirement"]["Counter"] += amount
        if quest["Requirement"]["Counter"] >= quest["Requirement"]["Goal"]:
            quest["Requirement"]["Counter"] = quest["Requirement"]["Goal"]
        logging.info(f"quest: {quest_id} has met {quest['Requirement']['Counter']} of {quest['Requirement']['Goal']}")

        if quest["Requirement"]["Counter"] == quest["Requirement"]["Goal"]:
            change_quest_status(quest_id, "Complete")

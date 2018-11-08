"""
Conversation data

This closely resembles a .json filetype and could possibly become a database table

npc_conversations
 - The NPC will display dialog according to the Dialog ID
 - The NPC ID isn't used in the code but helps to organize the data
 - The Text is the NPC text
 - The options refer to the corresponding option in conversation_options

conversation_options
 - The ID is referred to by the conversation
 - The Quest ID links to the appropriate quest
 - The Text is the option test
 - End Dialog represents if the dialog is closed after the option is selected
 - Tags are a list of strings that the NPC will handle

"""

NPC_id: {
    1: {
        "Dialog ID": {
            1: {
                "Text": "It's dangerous to go alone, take this",
                "Options": {
                    1: {
                        "Text": "Thanks",
                        "Link": 3,
                        "Tags": ["Health"],
                        "End Dialog": True
                    },
                    2: {
                        "Text": "What is this?",
                        "Link": 2,
                        "Tags": [],
                        "End Dialog": False
                    }
                }
            },
            2: {
                "Text": "This healthpack will restore some life when used.",
                "Options": {
                    1: {
                        "Text": "Thanks",
                        "Link": 3,
                        "Tags": ["Health"],
                        "End Dialog": False
                    }
                }
            },
            3: {
                "Text": "You already have my healthpack, back off man",
                "Options": {
                    1: {
                        "Text": ". . .",
                        "Link": 3,
                        "Tags": [],
                        "End Dialog": True
                    }
                }
            }
        }
    }
}

npc_conversations = {
    "Dialog ID": {
        1: {
            "NPC ID": 1,
            "Text": "It is dangerous to go alone, take this.",
            "options": [1, 2],
        },
        2: {
            "NPC ID": 1,
            "Text": "This healthpack will restore some life when used.",
            "options": [1],
        },
        3: {
            "NPC ID": 1,
            "Text": "You already have my healthpack, back off man",
            "options": [3],
        },
        4: {
            "NPC ID": 2,
            "Text": "Would you kindly remove these zombies?",
            "options": [4, 5],
        },
        5: {
            "NPC ID": 2,
            "Text": "If you change your mind, talk to me again",
            "options": [6],
        },
        6: {
            "NPC ID": 2,
            "Text": "What are you waiting for?",
            "options": [7, 8],
        },
        7: {
            "NPC ID": 2,
            "Text": "Great job. Here is your reward",
            "options": [9],
        },
        8: {
            "NPC ID": 2,
            "Text": "Thanks for solving our problem!",
            "options": [10],
        },
    },
}

conversation_options = {
    "ID": {
        1: {
            "Quest ID": None,
            "Text": "Thanks",
            "Conversation Link ID": 3,
            "End Dialog": True,
            "Tags": ["health"],
        },
        2: {
            "Quest ID": None,
            "Text": "What is this?",
            "Conversation Link ID": 2,
            "End Dialog": False,
            "Tags": [],
        },
        3: {
            "Quest ID": None,
            "Text": "...",
            "Conversation Link ID": 3,
            "End Dialog": True,
            "Tags": [],
        },
        4: {
            "Quest ID": 1,
            "Text": "Sure!",
            "Conversation Link ID": 6,
            "End Dialog": True,
            "Tags": [],
        },
        5: {
            "Quest ID": None,
            "Text": "Hell no",
            "Conversation Link ID": 5,
            "End Dialog": False,
            "Tags": [],
        },
        6: {
            "Quest ID": 1,
            "Text": "Ok",
            "Conversation Link ID": 4,
            "End Dialog": True,
            "Tags": [],
        },
        7: {
            "Quest ID": 1,
            "Text": "On it!'",
            "Conversation Link ID": 6,
            "End Dialog": True,
            "Tags": [],
        },
        8: {
            "Quest ID": None,
            "Text": "Nah...",
            "Conversation Link ID": 5,
            "End Dialog": False,
            "Tags": [],
        },
        9: {
            "Quest ID": None,
            "Text": "Thanks!",
            "Conversation Link ID": 8,
            "End Dialog": True,
            "Tags": ["quest complete"],
        },
        10: {
            "Quest ID": None,
            "Text": "No Problem",
            "Conversation Link ID": 8,
            "End Dialog": True,
            "Tags": [],
        },
    }
}

list_of_actions = [
"close",
"health",
"explain"
]

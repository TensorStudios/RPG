# npc_conversations = {
#     "id": {
#         1: {
#             "initial": {
#                 "text": "It is dangerous to go alone, take this.",
#                 "options": {
#                     "Thanks": ["close", "health"],
#                     "What is this?": ["explain", "d_2"]
#                 }
#             },
#             "d_2": {
#                 "text": "This healthpack will restore some life when used.",
#                 "options": {
#                     "Thanks": ["close", "health"]
#                 }
#             },
#             "d_3": {
#                 "text": "You already have my health pack, back off man",
#                 "options": {
#                     "...": ["close"]
#                 }
#             }
#         }
#     }
# }

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
            "Conversation Link ID": None,
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
            "Quest ID": 1,
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
            "Text": "Working on it!'",
            "Conversation Link ID": 6,
            "End Dialog": True,
            "Tags": [],
        },
        8: {
            "Quest ID": 1,
            "Text": "I've changed my mind",
            "Conversation Link ID": 5,
            "End Dialog": False,
            "Tags": [],
        },
        9: {
            "Quest ID": 1,
            "Text": "Thanks!",
            "Conversation Link ID": 8,
            "End Dialog": True,
            "Tags": ["quest complete"],
        },
        10: {
            "Quest ID": 1,
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

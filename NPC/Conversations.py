"""

NPC_id data represents a .json filetype and will be upgraded in a future commit to take advantage of that

The structure goes as such

NPC_id (The ID of the NPC referred to)
    - Default Text (What does the NPC Say when at the "Empty" Menu
    - Dialog ID (What step of the conversation are we at)
        - Quest_ID (None if there is no quest associated, otherwise it is the ID of the quest)
        - Text (What the NPC is saying
        - Options (Options the player can get)
            - Option 1 (Must be an int())
                - Text (of the option)
                - Link (to the next dialog id)
                - Tags (what happens when this option is chosen if there is anything more than progressing to another
                dialog id)
                - End Dialog (Does this end the dialog screen with the NPC)


"""
# This is the old form, keeping it in case the data is corrupted or a better way to do this is found

import logging
import json

logging.warning("Conversations.py was just imported and should not have been. If this py file was ran manually ignore "
                "this message")

NPC_id = {
    1: {
        "Default Text": "Hello Traveler",
        "Conversations": {
            1: {
                "Node Title": "Let's Talk",
                "Active": True,
                "Step 1": {
                    "Text": "It's dangerous to go alone, take this",
                    "Options": {
                        1: {
                            "Text": "Thanks",
                            "Link": ["Conversations", 1, None],
                            "Tags": ["Deactivate", "Health"],
                            "End Dialog": True
                        },
                        2: {
                            "Text": "What is this?",
                            "Link": ["Conversations", 1, "Step 2"],
                            "Tags": [],
                            "End Dialog": False
                        },
                    },
                },
                "Step 2": {
                    "Text": "This healthpack will restore some life when used.",
                    "Options": {
                        1: {
                            "Text": "Thanks",
                            "Link": None,
                            "Tags": ["Deactivate", "Health"],
                            "End Dialog": True
                        },
                    },
                },
            },
            2: {
                "Node Title": "Please Sir...",
                "Active": False,
                "Step 1": {
                    "Text": "You already have my healthpack, back off man",
                    "Options": {
                        "Link": None,
                        "Tags": [],
                        "End Dialog": True
                    },
                }
            },
        },
        "Quests": {

        },
    },
    2: {
        "Default Text": "Hello",
        "Conversations": {
            1: {
                "Node Title": "Anything else?",
                "Active": False,
                "Step 1": {
                    "Text": "Thanks for solving our problems",
                    "Options": {
                        1: {
                            "Text": "No Problem",
                            "Link": 5,
                            "Tags": [],
                            "End Dialog": True,
                        }
                    }
                }
            }
        },
        "Quests": {
            1: {
                "Node Title": "! We need help",
                "Active": True,
                "Step 1": {
                    "Text": "Would you kindly remove these Zombies?",
                    "Options": {
                        1: {
                            "Text": "Sure!",
                            "Link": "Step 2",
                            "Tags": ["Start"],
                            "End Dialog": True,
                        },
                        2: {
                            "Text": "Hell no!",
                            "Link": "Step 1",
                            "Tags": [],
                            "End Dialog": True,
                        }
                    },
                },
                "Step 2": {
                    "Text": "What are you waiting for?",
                    "Options": {
                        1: {
                            "Text": "On it!",
                            "Link": 2,
                            "Tags": [],
                            "End Dialog": True,
                        },
                        2: {
                            "Text": "Nah ...",
                            "Link": "Step 3",
                            "Tags": [],
                            "End Dialog": False,
                        },
                    },
                },
                "Step 3": {
                    "Text": "If you change your mind, talk to me again",
                    "Options": {
                        1: {
                            "Text": "Ok",
                            "Link": 1,
                            "Tags": ["Cancel"],
                            "End Dialog": True,
                        }
                    },
                },
                "Step 4": {
                    "Text": "Great job. Here is your reward",
                    "Options": {
                        1: {
                            "Text": "Thanks!",
                            "Link": 5,
                            "Tags": ["Close"],
                            "End Dialog": True,
                        },
                    },
                },
            },
        },
    },
}


data = json.dumps(NPC_id)

with open("conversations_alpha.json", 'w') as fp:
    fp.write(data)

# Old data

# NPC_id = {
#     1: {
#         "Default Text": "Hello Traveler",
#         "Dialog ID": {
#             1: {
#                 "Quest_ID": 3,
#                 "Text": "It's dangerous to go alone, take this",
#                 "Options": {
#                     1: {
#                         "Text": "Thanks",
#                         "Link": 3,
#                         "Tags": ["Close"],
#                         "End Dialog": True
#                     },
#                     2: {
#                         "Text": "What is this?",
#                         "Link": 2,
#                         "Tags": [],
#                         "End Dialog": False
#                     }
#                 }
#             },
#             2: {
#                 "Quest_ID": 3,
#                 "Text": "This healthpack will restore some life when used.",
#                 "Options": {
#                     1: {
#                         "Text": "Thanks",
#                         "Link": 3,
#                         "Tags": ["Close"],
#                         "End Dialog": True
#                     }
#                 }
#             },
#             3: {
#                 "Quest_ID": 3,
#                 "Text": "You already have my healthpack, back off man",
#                 "Options": {
#                     1: {
#                         "Text": ". . .",
#                         "Link": 3,
#                         "Tags": [],
#                         "End Dialog": True
#                     }
#                 }
#             }
#         }
#     },
#     2: {
#         "Default Text": "Hello",
#         "Dialog ID": {
#             1: {
#                 "Quest_ID": 1,
#                 "Text": "Would you kindly remove these Zombies?",
#                 "Options": {
#                     1: {
#                         "Text": "Sure!",
#                         "Link": 2,
#                         "Tags": ["Start"],
#                         "End Dialog": True,
#                     },
#                     2: {
#                         "Text": "Hell no!",
#                         "Link": 1,
#                         "Tags": [],
#                         "End Dialog": True,
#                     }
#                 }
#             },
#             2: {
#                 "Quest_ID": 1,
#                 "Text": "What are you waiting for?",
#                 "Options": {
#                     1: {
#                         "Text": "On it!",
#                         "Link": 2,
#                         "Tags": [],
#                         "End Dialog": True,
#                     },
#                     2: {
#                         "Text": "Nah ...",
#                         "Link": 3,
#                         "Tags": [],
#                         "End Dialog": False,
#                     }
#                 }
#             },
#             3: {
#                 "Quest_ID": 1,
#                 "Text": "If you change your mind, talk to me again",
#                 "Options": {
#                     1: {
#                         "Text": "Ok",
#                         "Link": 1,
#                         "Tags": ["Cancel"],
#                         "End Dialog": True,
#                     }
#                 }
#             },
#             4: {
#                 "Quest_ID": 1,
#                 "Text": "Great job. Here is your reward",
#                 "Options": {
#                     1: {
#                         "Text": "Thanks!",
#                         "Link": 5,
#                         "Tags": ["Close"],
#                         "End Dialog": True,
#                     }
#                 }
#             },
#             5: {
#                 "Quest_ID": None,
#                 "Text": "Thanks for solving our problem",
#                 "Options": {
#                     1: {
#                         "Text": "No Problem",
#                         "Link": 5,
#                         "Tags": [],
#                         "End Dialog": True,
#
#                     }
#                 }
#             }
#         }
#     }
# }


NPC_id = {
    1: {
        "Dialog ID": {
            1: {
                "Quest_ID": None,
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
                "Quest_ID": None,
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
                "Quest_ID": None,
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
    },
    2: {
        "Dialog ID": {
            1: {
                "Quest_ID": 0,
                "Text": "Would you kindly remove these Zombies?",
                "Options": {
                    1: {
                        "Text": "Sure!",
                        "Link": 2,
                        "Tags": ["Start 1"],
                        "End Dialog": True,
                    },
                    2: {
                        "Text": "Hell no!",
                        "Link": 1,
                        "Tags": [],
                        "End Dialog": True,
                    }
                }
            },
            2: {
                "Quest_ID": 0,
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
                        "Link": 3,
                        "Tags": ["Cancel 1"],
                        "End Dialog": False,
                    }
                }
            },
            3: {
                "Quest_ID": 0,
                "Text": "If you change your mind, talk to me again",
                "Options": {
                    "Text": "Ok",
                    "Link": 1,
                    "Tags": [],
                    "End Dialog": True,

                }
            },
            4: {
                "Quest_ID": 0,
                "Text": "Great job. Here is your reward",
                "Options": {
                    1: {
                        "Text": "Thanks!",
                        "Link": 5,
                        "Tags": ["Complete 1"],
                        "End Dialog": True,
                    }
                }
            },
            5: {
                "Quest_ID": None,
                "Text": "Thanks for solving our problem",
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
    }
}

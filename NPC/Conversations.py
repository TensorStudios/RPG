npc_conversations = {
    "id": {
        1: {
            "initial": {
                "text": "It is dangerous to go alone, take this.",
                "options": {
                    "Thanks": ["close", "health"],
                    "What is this?": ["explain", "d_2"]
                }
            },
            "d_2": {
                "text": "This healthpack will restore some life when used.",
                "options": {
                    "Thanks": ["close", "health"]
                }
            },
            "d_3": {
                "text": "You already have my health pack, back off man",
                "options": {
                    "...": ["close"]
                }
            }
        }
    }
}

list_of_actions = [
    "close",
    "health",
    "explain"
]

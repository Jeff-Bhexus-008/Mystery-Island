LOCATIONS = {
    "Beach": ["Jungle"],
    "Jungle": ["Beach", "Cave"],
    "Cave": ["Jungle", "Old Bridge"],
    "Old Bridge": ["Cave", "Lighthouse"],
    "Lighthouse": ["Old Bridge"]
}

ITEMS = {
    "Jungle": "rope",
    "Cave": "lantern"
}


def new_game(name):
    return {
        "name": name,
        "location": "Beach",
        "energy": 5,
        "inventory": [],
        "game_over": False,
        "won": False,
        "quit": False
    }


def available_actions(player):
    actions = []

    for destination in LOCATIONS[player["location"]]:
        actions.append("Go to " + destination)

    item = ITEMS.get(player["location"])

    if item and item not in player["inventory"]:
        actions.append("Take " + item)

    actions.append("Check inventory")

    if player["location"] == "Lighthouse":
        actions.append("Light beacon")

    actions.append("Help")
    actions.append("Quit")

    return actions


def apply_action(player, action):
    action = action.strip().lower()

    if player["game_over"]:
        return "The game has already ended."

    if action.startswith("go to "):
        destination = action[6:].title()

        if destination not in LOCATIONS[player["location"]]:
            return "You cannot go there from here."

        if destination in ["Old Bridge", "Lighthouse"]:
            if "rope" not in player["inventory"]:
                return "You need a rope to cross the bridge."

        if player["energy"] <= 0:
            player["game_over"] = True
            return "You have run out of energy. Game over!"

        player["location"] = destination
        player["energy"] -= 1

        if player["energy"] == 0:
            player["game_over"] = True
            return "You used your last energy point. Game over!"

        return "You moved to " + destination + "."

    if action.startswith("take "):
        item = action[5:]

        if ITEMS.get(player["location"]) != item:
            return "That item is not available here."

        if item in player["inventory"]:
            return "You already have that item."

        player["inventory"].append(item)
        return "You collected the " + item + "!"

    if action == "check inventory":
        if player["inventory"]:
            return "You have: " + ", ".join(player["inventory"])

        return "Your inventory is empty."

    if action == "light beacon":
        if player["location"] != "Lighthouse":
            return "You must reach the Lighthouse first."

        if "lantern" not in player["inventory"]:
            return "You need a lantern to light the beacon."

        player["won"] = True
        player["game_over"] = True
        return "You restored the beacon! A rescue boat is coming!"

    if action == "help":
        return (
            "Explore the island, collect the rope and lantern, "
            "cross the bridge, and light the lighthouse beacon. "
            "You lose if your energy reaches zero."
        )

    if action in ["quit", "exit", "q"]:
        player["game_over"] = True
        player["quit"] = True
        return "You left the island adventure."
    return "Invalid action. Please choose an available option."


def is_win(player):
    return player["won"]


def is_loss(player):
    return player["game_over"] and not player["won"]
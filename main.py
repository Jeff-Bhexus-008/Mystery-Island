from game import new_game, available_actions, apply_action, is_win, is_loss


def play_game():
    print("\n" + "=" * 40)
    print("       MYSTERY ISLAND")
    print("       THE LOST LIGHTHOUSE")
    print("=" * 40)

    print("\nYour mission:")
    print("Explore the island and restore the lighthouse beacon.")
    print("Collect a rope and a lantern.")
    print("Be careful! You have only 5 energy points.")

    name = input("\nEnter your name: ").strip()

    if not name:
        name = "Adventurer"

    player = new_game(name)

    print(f"\nWelcome, {player['name']}!")
    print("Your adventure begins on the Beach.")

    while not player["game_over"]:
        print("\n" + "-" * 40)
        print("Location:", player["location"])
        print("Energy:", player["energy"])
        print("Inventory:", player["inventory"] or "Empty")

        actions = available_actions(player)

        print("\nWhat would you like to do?")

        for number, action in enumerate(actions, start=1):
            print(f"{number}. {action}")

        choice = input("\nChoose an option: ").strip()

        if choice.lower() in ["q", "quit", "exit"]:
            action = "quit"

        elif choice.isdigit() and 1 <= int(choice) <= len(actions):
            action = actions[int(choice) - 1]

        else:
            print("Invalid choice. Please try again.")
            continue

        message = apply_action(player, action)
        print("\n" + message)

    if is_win(player):
        print("\nCONGRATULATIONS! YOU ESCAPED MYSTERY ISLAND!")

    elif is_loss(player):
        print("\nYOU RAN OUT OF ENERGY. GAME OVER!")

    else:
        print("\nYou chose to leave the adventure.")
    print("Thanks for playing!")


def main():
    while True:
        play_game()

        replay = input("\nWould you like to play again? (yes/no): ")
        replay = replay.strip().lower()

        if replay not in ["yes", "y"]:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
import unittest

from game import new_game, apply_action, is_win, is_loss


class TestMysteryIsland(unittest.TestCase):

    def setUp(self):
        self.player = new_game("Jeff")

    def test_new_game(self):
        self.assertEqual(self.player["location"], "Beach")
        self.assertEqual(self.player["energy"], 5)
        self.assertEqual(self.player["inventory"], [])

    def test_invalid_action_changes_nothing(self):
        before = self.player.copy()

        apply_action(self.player, "fly to the moon")

        self.assertEqual(self.player, before)

    def test_valid_move_uses_one_energy(self):
        apply_action(self.player, "go to jungle")

        self.assertEqual(self.player["location"], "Jungle")
        self.assertEqual(self.player["energy"], 4)

    def test_wrong_direction_is_rejected(self):
        apply_action(self.player, "go to cave")

        self.assertEqual(self.player["location"], "Beach")
        self.assertEqual(self.player["energy"], 5)

    def test_rope_can_be_collected_once(self):
        apply_action(self.player, "go to jungle")
        apply_action(self.player, "take rope")
        apply_action(self.player, "take rope")

        self.assertEqual(self.player["inventory"].count("rope"), 1)

    def test_bridge_requires_rope(self):
        apply_action(self.player, "go to jungle")
        apply_action(self.player, "go to cave")

        message = apply_action(self.player, "go to old bridge")

        self.assertEqual(self.player["location"], "Cave")
        self.assertEqual(self.player["energy"], 3)
        self.assertIn("rope", message)

    def test_lighthouse_requires_lantern(self):
        apply_action(self.player, "go to jungle")
        apply_action(self.player, "take rope")
        apply_action(self.player, "go to cave")
        apply_action(self.player, "go to old bridge")
        apply_action(self.player, "go to lighthouse")

        message = apply_action(self.player, "light beacon")

        self.assertFalse(is_win(self.player))
        self.assertIn("lantern", message)

    def test_correct_path_wins(self):
        apply_action(self.player, "go to jungle")
        apply_action(self.player, "take rope")
        apply_action(self.player, "go to cave")
        apply_action(self.player, "take lantern")
        apply_action(self.player, "go to old bridge")
        apply_action(self.player, "go to lighthouse")
        apply_action(self.player, "light beacon")

        self.assertTrue(is_win(self.player))
        self.assertEqual(self.player["energy"], 1)

    def test_running_out_of_energy_causes_loss(self):
        apply_action(self.player, "go to jungle")
        apply_action(self.player, "go to beach")
        apply_action(self.player, "go to jungle")
        apply_action(self.player, "go to beach")
        apply_action(self.player, "go to jungle")

        self.assertEqual(self.player["energy"], 0)
        self.assertTrue(is_loss(self.player))

    def test_new_game_resets_player(self):
        self.player["energy"] = 1
        self.player["inventory"].append("rope")

        self.player = new_game("Jeff")

        self.assertEqual(self.player["energy"], 5)
        self.assertEqual(self.player["location"], "Beach")
        self.assertEqual(self.player["inventory"], [])
        self.assertFalse(self.player["game_over"])


if __name__ == "__main__":
    unittest.main()
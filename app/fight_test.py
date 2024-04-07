import unittest
from app.fighters import default_fighters
from app.fight import fight
from app.fighters import Fighter, MoreThanOneFighterException, FighterNonFoundException, select_fighters


class TestFight(unittest.TestCase):
    def setUp(self):
        self.set = default_fighters
        self.theone = self.set[0]

    def test_fight_set_not_altered(self):
        winner = fight(self.theone, self.set)
        self.assertIn(winner, self.set)
        self.assertIn(self.theone, self.set)

    def test_fighter_as_string(self):
        self.assertIn("🥟", str(self.theone))


class TestSelectFighters(unittest.TestCase):
    def setUp(self):
        self.dumpling = Fighter("Dumpling", "", 1, "")
        self.kebab = Fighter("Kebab", "", 1, "")
        self.fighters = [self.dumpling, self.kebab]

    def test_select_fighters_single_match(self):
        message = "I choose dumpling" #FIXME
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.dumpling)

    def test_select_fighters_multiple_matches(self):
        message = "I choose dumpling and kebab"
        with self.assertRaises(MoreThanOneFighterException):
            select_fighters(message, self.fighters)

    def test_select_fighters_no_match(self):
        message = "I choose burger"
        with self.assertRaises(FighterNonFoundException):
            select_fighters(message, self.fighters)
        

if __name__ == '__main__':
    unittest.main()


if __name__ == "__main__":
    unittest.main()

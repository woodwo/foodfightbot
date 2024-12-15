import unittest
from app.fight import create_fighter, fight
from app.models import Fighter
from app.selector import (
    MoreThanOneFighterException,
    FighterNonFoundException,
    select_fighters,
)


class TestFight(unittest.TestCase):
    def setUp(self):
        self.set = [
            create_fighter("Boxer", "🥊", 10, "A boxer fighter for testing"),
            create_fighter("Karate", "🥋", 20, "A karate fighter for testing"),
        ]
        self.theone = self.set[0]

    def test_fight_set_not_altered(self):
        [winner, _] = fight(self.theone, self.set)
        self.assertIn(winner.name, [f.name for f in self.set])
        self.assertIn(self.theone.name, [f.name for f in self.set])

    def test_fighter_as_string(self):
        self.assertIn("🥊", str(self.theone))


class TestSelectFighters(unittest.TestCase):
    def setUp(self):
        self.dumpling = create_fighter("Dumplings", "", 1, "")
        self.kebab = create_fighter("Kebab", "", 1, "")
        self.burger = create_fighter("Burger", "", 1, "")
        self.nuggets = create_fighter("Nuggets", "", 1, "")
        self.fighters = [self.dumpling, self.kebab, self.burger, self.nuggets]

    def test_select_fighters_single_match_remove_punctuation(self):
        message = "Yaay Go Kebab, go"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.kebab)

    def test_select_fighters_single_match_in_the_string(self):
        message = "Yaay Go Kebab go"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.kebab)

    def test_select_fighters_single_match_eol(self):
        message = "I choose kebab"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.kebab)

    def test_select_fighters_single_match_sol(self):
        message = "Kebab is my fighter"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.kebab)

    def test_select_fighters_single_match_lowercase(self):
        message = "kebab"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.kebab)

    def test_select_fighters_single_match_emoj(self):
        message = "It's a dumpling 😃"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.dumpling)

    def test_select_fighters_single_match_case(self):
        message = "Kebab"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.kebab)

    def test_select_fighters_single_match_case_phonetic1(self):
        message = "kebap"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.kebab)

    def test_select_fighters_single_match_case_phonetic2(self):
        message = "kepab"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.kebab)

    def test_select_fighters_multiple_matches(self):
        message = "I choose dumpling and kebab"
        with self.assertRaises(MoreThanOneFighterException):
            select_fighters(message, self.fighters)

    def test_select_fighters_no_match(self):
        message = "I choose omelette"
        with self.assertRaises(FighterNonFoundException):
            select_fighters(message, self.fighters)

    def test_select_fighters_match_plural_from_message(self):
        message = "kebabs"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.kebab)

    def test_select_fighters_match_plural_from_fighters(self):
        message = "dumpling"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.dumpling)

    def test_select_fighters_should_not_match_burger_with_nuggets(self):
        message = "burger"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.burger)

    def test_select_fighters_no_false_positives(self):
        message = "I want nuggets"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.nuggets)

    def test_select_fighters_similar_names(self):
        message = "burger"
        selected_fighter = select_fighters(message, self.fighters)
        self.assertEqual(selected_fighter, self.burger)


class TestRemoveFighters(unittest.TestCase):
    """To show how remove() works"""

    def setUp(self):
        self.dumpling = create_fighter("Dumplings", "", 1, "")
        self.kebab = create_fighter("Kebab", "", 1, "")
        self.fighters = [self.dumpling, self.kebab]

    def test_method_remove(self):
        self.fighters.remove(self.kebab)
        self.assertIn(self.dumpling, self.fighters)
        self.assertNotIn(self.kebab, self.fighters)

    def test_method_remove_assert(self):
        with self.assertRaises(ValueError):
            self.fighters.remove(create_fighter("Dumplings", "", 1, ""))
        self.assertIn(self.dumpling, self.fighters)


if __name__ == "__main__":
    unittest.main()

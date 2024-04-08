import unittest
from app.fight import create_fighter, fight
from app.models import Fighter
from app.selector import MoreThanOneFighterException, FighterNonFoundException, select_fighters


class TestFight(unittest.TestCase):
    def setUp(self):
        self.set = [create_fighter("Boxer", "🥊", 10, "A boxer fighter for testing"), create_fighter("Karate", "🥋", 20, "A karate fighter for testing")]
        self.theone = self.set[0]

    def test_fight_set_not_altered(self):
        [winner, _] = fight(self.theone, self.set)
        self.assertIn(winner, self.set)
        self.assertIn(self.theone, self.set)

    def test_fighter_as_string(self):
        self.assertIn("🥊", str(self.theone))


class TestSelectFighters(unittest.TestCase):
    def setUp(self):
        self.dumpling = create_fighter("Dumpling", "", 1, "")
        self.kebab = create_fighter("Kebab", "", 1, "")
        self.fighters = [self.dumpling, self.kebab]

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
        message = "kibap"
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
        message = "I choose burger"
        with self.assertRaises(FighterNonFoundException):
            select_fighters(message, self.fighters)
        

if __name__ == '__main__':
    unittest.main()

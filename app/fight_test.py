import unittest
from app.fighters import fighters
from app.fight import fight

class TestFight(unittest.TestCase):
    def setUp(self):
        self.set = fighters
        self.theone = self.set[0]

    def test_fight(self):
        winner = fight(self.theone, self.set)
        self.assertIn(winner, self.set)
        self.assertIn(self.theone, self.set)

if __name__ == '__main__':
    unittest.main()
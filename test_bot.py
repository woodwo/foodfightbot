import unittest
from unittest.mock import MagicMock, patch
from bot import Fighter, UserFighter, FightResult, User
import unittest
from unittest.mock import MagicMock
from bot import Bot, FIGHTER

class TestBot(unittest.TestCase):
    def setUp(self):
        self.update = MagicMock()
        self.context = MagicMock()

    def test_fighter_selection_no_fighters(self):
        update = self.update
        context = self.context

        update.message.from_user.id = 123
        update.message.from_user.first_name = "John"
        update.message.text = "Fighter 1"

        session = MagicMock()
        session.query.return_value.all.return_value = []
        session.query.return_value.join.return_value.filter.return_value.all.return_value = []

        with patch("bot.Session", return_value=session):
            result = fighter_selection(update, context)

        self.assertEqual(result, FIGHTER)
        update.message.reply_text.assert_called_with("No fighters found. Please redo /start command.")

    def test_fighter_selection_exceed_calories_limit(self):
        update = self.update
        context = self.context

        update.message.from_user.id = 123
        update.message.from_user.first_name = "John"
        update.message.text = "Fighter 1"

        session = MagicMock()
        session.query.return_value.all.return_value = [Fighter(id=1, name="Fighter 1", attack_power=2000)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [Fighter(id=1, name="Fighter 1", attack_power=2000)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [FightResult(id=1, user_id=123, fighter_id=1, opponent_id=2, is_user_win=True)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [FightResult(id=1, user_id=123, fighter_id=1, opponent_id=2, is_user_win=True)]

        with patch("bot.Session", return_value=session):
            result = fighter_selection(update, context)

        self.assertEqual(result, FIGHTER)
        update.message.reply_text.assert_called_with("You've selected Fighter 1 [icon] that cost 2000 calories. Seems you have reached your daily calories limit of 2500, today you already made 2000. Please choose a fighter with less attack power.")

    def test_fighter_selection_fighter_not_found(self):
        update = self.update
        context = self.context

        update.message.from_user.id = 123
        update.message.from_user.first_name = "John"
        update.message.text = "Fighter 3"

        session = MagicMock()
        session.query.return_value.all.return_value = [Fighter(id=1, name="Fighter 1", attack_power=1000), Fighter(id=2, name="Fighter 2", attack_power=1500)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [Fighter(id=1, name="Fighter 1", attack_power=1000), Fighter(id=2, name="Fighter 2", attack_power=1500)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [FightResult(id=1, user_id=123, fighter_id=1, opponent_id=2, is_user_win=True)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [FightResult(id=1, user_id=123, fighter_id=1, opponent_id=2, is_user_win=True)]

        with patch("bot.Session", return_value=session):
            result = fighter_selection(update, context)

        self.assertEqual(result, FIGHTER)
        update.message.reply_text.assert_called_with("Fighter not found. Please choose a valid fighter.")

    def test_fighter_selection_multiple_fighters(self):
        update = self.update
        context = self.context

        update.message.from_user.id = 123
        update.message.from_user.first_name = "John"
        update.message.text = "Fighter 1"

        session = MagicMock()
        session.query.return_value.all.return_value = [Fighter(id=1, name="Fighter 1", attack_power=1000), Fighter(id=2, name="Fighter 2", attack_power=1500)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [Fighter(id=1, name="Fighter 1", attack_power=1000), Fighter(id=2, name="Fighter 2", attack_power=1500)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [FightResult(id=1, user_id=123, fighter_id=1, opponent_id=2, is_user_win=True)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [FightResult(id=1, user_id=123, fighter_id=1, opponent_id=2, is_user_win=True)]

        with patch("bot.Session", return_value=session):
            result = fighter_selection(update, context)

        self.assertEqual(result, FIGHTER)
        update.message.reply_text.assert_called_with("Please choose only one fighter. Found: Fighter 1, Fighter 2. You mean only one, right? :)")

    def test_fighter_selection_success(self):
        update = self.update
        context = self.context

        update.message.from_user.id = 123
        update.message.from_user.first_name = "John"
        update.message.text = "Fighter 1"

        session = MagicMock()
        session.query.return_value.all.return_value = [Fighter(id=1, name="Fighter 1", attack_power=1000), Fighter(id=2, name="Fighter 2", attack_power=1500)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [Fighter(id=1, name="Fighter 1", attack_power=1000), Fighter(id=2, name="Fighter 2", attack_power=1500)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [FightResult(id=1, user_id=123, fighter_id=1, opponent_id=2, is_user_win=True)]
        session.query.return_value.join.return_value.filter.return_value.all.return_value = [FightResult(id=1, user_id=123, fighter_id=1, opponent_id=2, is_user_win=True)]

        with patch("bot.Session", return_value=session):
            result = fighter_selection(update, context)

        self.assertEqual(result, FIGHTER)
        update.message.reply_text.assert_called_with("Fighter 1 [icon] vs. Fighter 2 [icon]!")
        update.message.reply_text.assert_called_with("Fight started...")
        update.message.reply_text.assert_called_with("Fight ended")
        update.message.reply_text.assert_called_with("The winner is...")
        update.message.reply_text.assert_called_with("Congratulations, you are the winner!")


class BotTestCase(unittest.TestCase):
    def setUp(self):
        self.bot = Bot()

    def test_fighter_selection_no_fighters_found(self):
        update = MagicMock()
        context = MagicMock()
        update.message.from_user.id = 1
        update.message.from_user.first_name = "John"
        update.message.text = "Fighter 1"
        self.bot.Session = MagicMock()
        session = self.bot.Session.return_value
        session.query.return_value.all.return_value = []
        result = self.bot.fighter_selection(update, context)
        self.assertEqual(result, self.bot.FIGHTER)
        update.message.reply_text.assert_called_with("No fighters found. Please redo /start command.")

    def test_fighter_selection_exceeds_daily_calories_limit(self):
        update = MagicMock()
        context = MagicMock()
        update.message.from_user.id = 1
        update.message.from_user.first_name = "John"
        update.message.text = "Fighter 1"
        self.bot.Session = MagicMock()
        session = self.bot.Session.return_value
        session.query.return_value.all.return_value = [MagicMock(attack_power=2000)]
        session.query.return_value.filter.return_value.all.return_value = [MagicMock(attack_power=100)]
        result = self.bot.fighter_selection(update, context)
        self.assertEqual(result, self.bot.FIGHTER)
        expected_reply = "You've selected Fighter 1 [icon] that cost 100 calories. Seems you have reached your daily calories limit of 2500, today you already made 2100. Please choose a fighter with less attack power."
        update.message.reply_text.assert_called_with(expected_reply)

    # Add more test cases for other scenarios

if __name__ == "__main__":
    unittest.main()
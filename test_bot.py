import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from bot import Fighter, FoodFightBot, UserFighter, FightResult, User
import unittest
from unittest.mock import MagicMock


class TestBot(unittest.TestCase):
    def setUp(self):
        self.update = MagicMock()
        self.context = MagicMock()
        self.bot = FoodFightBot("emptytoken")

    def test_fighter_selection_no_fighters(self):
        update = self.update
        context = self.context

        update.message.from_user.id = 123
        update.message.from_user.first_name = "John"
        update.message.text = "Fighter 1"
        update.message.reply_text = AsyncMock()

        session = MagicMock()
        session.query.return_value.all.return_value = []
        session.query.return_value.join.return_value.filter.return_value.all.return_value = []

        with patch("bot.Session", return_value=session):
            result = asyncio.run(self.bot.fighter_selection(update, context))

        update.message.reply_text.assert_called_with("No fighters found. Please redo /start command.")


if __name__ == "__main__":
    unittest.main()
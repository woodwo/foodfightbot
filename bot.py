import os
import telebot
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from helpers.error import error_handler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'TOKEN' with your actual bot token
bot = telebot.TeleBot(os.getenv("TOKEN"))


FIGHTER, FIGHT, RESULTS = range(3)
# start -description
# /fight - choose your fighter
# fighter selected - start random fight, delay
# results


class FoodFightBot:
    def __init__(self, token):
        self.token = token
        # TODO here we will read fighters description from db

    def run(self):
        application = Application.builder().token(self.token).build()

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                FIGHTER: [
                    MessageHandler(
                        filters.Regex("^Fighter.+$"),
                        self.fighter_selection,
                    )
                ],
                FIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.fight)],
                RESULTS: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.fight_results),
                ],
            },
            fallbacks=[
                CommandHandler("cancel", self.cancel),
                CommandHandler("stop", self.cancel),
                CommandHandler("exit", self.cancel),
            ],
            name="conversation",
        )

        application.add_handler(conv_handler)
        # ...and the error handler
        application.add_error_handler(error_handler)
        application.run_polling()

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancels and ends the conversation."""
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
        await update.message.reply_text(
            "Bye! I hope we can talk again some day.",
        )

        return ConversationHandler.END

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Starts the conversation and asks the user to select a fighter."""
        await update.message.reply_text(
            "Choose your fighter",
        )

        return FIGHTER
    
    async def fighter_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Stores the selected fighter and starts the fight."""
        context.user_data["fighter"] = update.message.text
        await update.message.reply_text(
            "Fight started",
        )

        return FIGHT
    
    async def fight(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Simulates a fight and shows the results."""
        await update.message.reply_text(
            "Fight results",
        )

        return RESULTS
    
    async def fight_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Shows the results of the fight and ends the conversation."""
        await update.message.reply_text(
            "Fight ended",
        )

        return ConversationHandler.END
    
if __name__ == "__main__":
    import os
    import sys

    # Retrieve the token from the environment variable
    token = os.environ.get("TOKEN")

    # Check if the token is available
    if token is None:
        print("Token not found in the environment variable.")
        sys.exit(1)

    bot = FoodFightBot(token)
    bot.run()
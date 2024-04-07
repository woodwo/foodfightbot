import asyncio
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
from app.fight import fight
from app.fighters import default_fighters, select_fighters, MoreThanOneFighterException, FighterNonFoundException
from helpers.error import error_handler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'TOKEN' with your actual bot token
bot = telebot.TeleBot(os.getenv("TOKEN"))


FIGHTER = range(1)
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
                        # filters.Regex("^Fighter.+$"),
                        filters.TEXT & ~filters.COMMAND, 
                        self.fighter_selection,
                    )
                ],
                # FIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.fight)],
                # RESULTS: [
                #     MessageHandler(filters.TEXT & ~filters.COMMAND, self.fight_results),
                # ],
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
        user = update.message.from_user
        logger.info("User %s choosing the fighter.", user.first_name)
        await update.message.reply_text(
            f"Choose your fighter:\n",
        )

        for f in default_fighters:
            await update.message.reply_text(
                f"{str(f)}",
            )

        return FIGHTER
    
    async def fighter_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Stores the selected fighter and starts the fight."""
        user = update.message.from_user
        logger.info("User %s want fighter %s in message.", user.first_name, update.message.text)

        try:
            fighter = select_fighters(update.message.text, default_fighters)
        except FighterNonFoundException:
            await update.message.reply_text("Fighter not found. Please choose a valid fighter.")
            return FIGHTER
        except MoreThanOneFighterException as e:
            await update.message.reply_text(f"Please choose only one fighter. Found: {e.message} You mean only one, right? :)")
            return FIGHTER
        
        fighter_name = update.message.text.lower() #TODO the whole message, split it to chunks

        for fighter in default_fighters:
            if fighter_name in fighter.name.lower():
                # context.user_data["fighter"] = fighter

                winner, opponent = fight(fighter, default_fighters)
                await update.message.reply_text(f"{fighter.name} [{fighter.icon}] vs. {opponent.name} [{opponent.icon}]!")
                await update.message.reply_text(f"Fight started...")

                # FIXME here is also a fight method decompose me
                # await update.chat_action("typing")
                await asyncio.sleep(3)
                await update.message.reply_text("Fight ended")
                await update.message.reply_text("The winner is...")
                # await update.chat_action("typing")
                await asyncio.sleep(3)
                await update.message.reply_text(f"{winner.name} [{winner.icon}]!")
                message = f"Congratulations, you are the winner!" if winner == fighter else "Sorry, you did not win this time."
                await update.message.reply_text(message)

                return ConversationHandler.END

        await update.message.reply_text("Fighter not found. Please choose a valid fighter.")
        return FIGHTER
    
    
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
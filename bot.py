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
from app.models import Fighter, User, Base
from app.selector import select_fighters, MoreThanOneFighterException, FighterNonFoundException
from helpers.error import error_handler

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///ffb.sqlite')
Base.metadata.bind = engine
Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))


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

        # create a new SQLAlchemy session TODO put a try here
        session = Session()
        # create a new User object and add it to the session
        try:
            # create a new User object and add it to the session
            new_user = User(id=user.id, name=user.first_name)
            session.add(new_user)
    
            # query the default fighters
            default_fighters = session.query(Fighter).filter_by(is_default=True).all()

            # add the default fighters to the user's fighters
            new_user.fighters = default_fighters

            session.commit()
        except IntegrityError:
            session.rollback()

        fighters = session.query(Fighter).join(User.fighters).filter(User.id == user.id).all()
        # check if at least one fighter is found
        if not fighters:
            await update.message.reply_text("No fighters found. Please redo /start command.")
            return FIGHTER

        await update.message.reply_text(
            f"Choose your fighter:\n",
        )
        
        for f in fighters:
            await update.message.reply_text(
                f"{str(f)}",
            )

        return FIGHTER
    
    async def fighter_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Stores the selected fighter and starts the fight."""
        user = update.message.from_user
        logger.info("User %s want fighter %s in message.", user.first_name, update.message.text)


        # create a new SQLAlchemy session TODO put a try here
        session = Session()
        all_fighters = session.query(Fighter).all()
        user_fighters = session.query(Fighter).join(User.fighters).filter(User.id == user.id).all()
        # check if at least one fighter is found
        if not user_fighters:
            await update.message.reply_text("No fighters found. Please redo /start command.")
            return FIGHTER

        try:
            # TODO select from user own fighters list
            fighter = select_fighters(update.message.text, user_fighters)
        except FighterNonFoundException:
            await update.message.reply_text("Fighter not found. Please choose a valid fighter.")
            return FIGHTER
        except MoreThanOneFighterException as e:
            await update.message.reply_text(f"Please choose only one fighter. Found: {e.message} You mean only one, right? :)")
            return FIGHTER
        
        # TODO here we need a unit test for opponent selection:
        # - last opponent will not be selected
        # - your fighter itself not to be selected
        opponents = all_fighters.copy()
        if "previous_opponent" in context.user_data:
            previous_opponent_name = context.user_data["previous_opponent"].name
            opponents = [opponent for opponent in opponents if opponent.name != previous_opponent_name]

        try:
            opponents.remove(fighter) # do not fight with yourself too
        except ValueError: # can be last opponent so removed before
            pass

        winner, opponent = fight(fighter, opponents)

        # save opponent by context to not fight with the same opponent second time consecutively
        context.user_data["previous_opponent"] = opponent

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

        await update.message.reply_text(f"Would you like to fight again? If so, please choose your fighter.")
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
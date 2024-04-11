import asyncio
from datetime import datetime, time
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
from app.hire import hire
from app.models import FightResult, Fighter, User, Base, UserFighter
from app.selector import select_fighters, MoreThanOneFighterException, FighterNonFoundException
from helpers.error import error_handler

from sqlalchemy import and_, create_engine, func
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
                        # TODO do fix for /start and /start again
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
        if update.message is not None:
            user = update.message.from_user
        elif update.callback_query is not None:
            user = update.callback_query.from_user
        elif update.inline_query is not None:
            user = update.inline_query.from_user
        else:
            await update.message.reply_text(
                "You User is not found. Please redo /start command.",
            )
            return ConversationHandler.END
        
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
            for fighter in default_fighters:
                user_fighter = UserFighter(user=new_user, fighter=fighter)
                session.add(user_fighter)

            session.commit()
        except IntegrityError:
            session.rollback()

        fighters = session.query(Fighter).join(UserFighter).filter(UserFighter.user_id == user.id).all()
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
        user_fighters = session.query(Fighter).join(UserFighter).filter(UserFighter.user_id == user.id).all()
        # check if at least one fighter is found
        if not user_fighters:
            await update.message.reply_text("No fighters found. Please redo /start command.")
            return FIGHTER
        
        # check user daily calories limit
        current_date = datetime.now().date()
        # query UserFighter for the current date and select fighters and their attack_power
        user_fighters_calories = session.query(Fighter.attack_power).join(
            FightResult, 
            and_(FightResult.user_id == user.id, FightResult.fighter_id == Fighter.id)  # specify how to join FightResult and Fighter
        ).filter(
            func.date(FightResult.timestamp) >= current_date
        ).all()
        # calculate the total attack power of the user's fighters
        today_calories = sum(row.attack_power for row in user_fighters_calories)
        logger.info("User %s calories today %d.", user.first_name, today_calories)

        try:
            # TODO select from user own fighters list
            fighter = select_fighters(update.message.text, user_fighters)
            # TODO fix hardcoded 2500
            if fighter.attack_power + today_calories > 2500:
                await update.message.reply_text(f"You've selected {fighter.name} [{fighter.icon}] that cost {fighter.attack_power} calories. Seems you have reached your daily calories limit of 2500, today you already made {today_calories}. Please choose a fighter with less attack power.")
                return FIGHTER
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

        # create a new FightResult object and add it to the session
        new_fight_result = FightResult(user_id=user.id, fighter_id=fighter.id, opponent_id=opponent.id, is_user_win=(winner == fighter))
        session.add(new_fight_result)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()

        # how much wins since last update
        # get the last update time of user_fighters
        last_update_time = session.query(func.max(UserFighter.timestamp)).filter(UserFighter.user_id == user.id).scalar()

        # count the wins since last update
        win_count = session.query(FightResult).filter(
            FightResult.user_id == user.id,
            FightResult.is_user_win == True,
            FightResult.timestamp > last_update_time
        ).count()
        logger.info("User %s wins since last update %d.", user.first_name, win_count)

        # update the next_win_count of the user
        user = session.query(User).get(user.id)
        if user.next_win_count <= win_count:            
            # TODO this is a logic too set it aside
            if user.next_win_count == 7:
                user.next_win_count = 11
            if user.next_win_count == 5:
                user.next_win_count = 7
            if user.next_win_count == 3:
                user.next_win_count = 5

            # Select fighters that are not related to the user yet
            candidates = session.query(Fighter).filter(~Fighter.user_fighters.any(UserFighter.user_id == user.id)).all()
            if candidates:
                new_fighter = hire(candidates)
                user_fighter = UserFighter(user=user, fighter=new_fighter)
                session.add(user_fighter)
                await update.message.reply_text(f"Congratulations! You have unlocked a new fighter: {new_fighter.name} [{new_fighter.icon}].")

            session.commit()
        # TODO this is a conversation
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


        # save opponent by context to not fight with the same opponent second time consecutively
        context.user_data["previous_opponent"] = opponent

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
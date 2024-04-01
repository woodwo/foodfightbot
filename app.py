import os
import telebot
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'YOUR_TOKEN' with your actual bot token
bot = telebot.TeleBot(os.getenv("TOKEN"))


@bot.message_handler(func=lambda message: True)
def send_answer(message):
    try:
        answer = "..."
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        logger.error("An error occurred: %s", str(e))


bot.polling()

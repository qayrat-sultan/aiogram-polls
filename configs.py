import datetime
import logging
import os

from dotenv import load_dotenv
from pymongo import MongoClient

from aiogram.utils.exceptions import BotBlocked, BotKicked, UserDeactivated

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")
ADMIN_IDS = tuple(os.getenv("ADMIN_IDS").split(","))
GROUP_ID = int(os.getenv("GROUP_ID"))


cluster = MongoClient(MONGO_URL)
collusers = cluster.bot.users
collreports = cluster.bot.reports
collquestions = cluster.bot.questions
collanswers = cluster.bot.answers

all_content_types = ["text", "sticker", "photo",
                     "voice", "document", "video", "video_note"]


formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'
logging.basicConfig(
    filename=f'logs/bot-from-{datetime.datetime.now().date()}.log',
    filemode='w',
    format=formatter,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.WARNING
)


async def on_startup(dp):
    print("Bot are started!")
    for i in ADMIN_IDS:
        try:
            await dp.bot.send_message(i, "Bot are start!")
        except (BotKicked, BotBlocked, UserDeactivated):
            pass


async def on_shutdown(dp):
    logging.warning("Shutting down..")
    for i in ADMIN_IDS:
        try:
            await dp.bot.send_message(i, "Bot are shutting down!")
        except (BotKicked, BotBlocked, UserDeactivated):
            pass
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bye!")

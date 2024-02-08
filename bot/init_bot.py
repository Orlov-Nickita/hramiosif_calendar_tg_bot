from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import os

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]


def init_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())

    return bot, dp

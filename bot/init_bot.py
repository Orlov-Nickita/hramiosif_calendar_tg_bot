from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import BotCommand
import os

from dotenv import load_dotenv

load_dotenv()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/keyboard ", description="Открыть клавиатуру"),
    ]
    await bot.set_my_commands(commands)


def init_bot():
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())

    return bot, dp

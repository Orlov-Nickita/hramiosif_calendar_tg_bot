from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import BotCommand

from loader import BOT_TOKEN


def get_bot():
    bot = Bot(token=BOT_TOKEN)

    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/keyboard ", description="Открыть клавиатуру"),
    ]

    bot.set_my_commands(commands)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())

    return bot, dp

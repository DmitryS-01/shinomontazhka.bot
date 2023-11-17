import asyncio
import logging
import sys

from config import *


from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.methods import DeleteWebhook


dp = Dispatcher()
USERS = list()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\nя - бот конча")


@dp.message()
async def lame_message_handler(message: types.Message) -> None:

    # id пользователя и текст его сообщения
    user_message = message.text
    user_id = message.from_user.id

    try:
        if user_id == bogdan:
            name = "@" + x if (x := message.from_user.username) else "учитель"
            await message.reply(f"пошел нахуй {name}")
        elif user_id not in USERS:
            if message.chat.id == shinomontazhka:
                print(message.chat.id)
                USERS.append(user_id)
                if user_id == vovan:
                    await message.reply("привет, вован")
                else:
                    await message.reply("ты не вован(((")
            else:
                await message.answer("ты никто и звать тебя никак")
        print(f"{message.from_user.id} написал: {message.text}")

    except Exception as e:
        print(f"тварь на {message.from_user.id} / {message.from_user.full_name} че то сломала:\n{e}")


async def main() -> None:
    bot = Bot(bot_token, parse_mode=ParseMode.HTML)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

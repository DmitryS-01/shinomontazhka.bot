import asyncio
import logging
import sys
import asyncio
from datetime import *
from random import choice

from config import *

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.methods import DeleteWebhook


dp = Dispatcher()
USERS = list()
KIZARU = ["ДА Я ХОДЯЧАЯ ЭНЦИКЛОПЕДИЯ ХИП ХОПА НАХУЙ",
          "НОУ РОЯЛТИ НОУ ЛОЯЛТИ",
          "ПОМНЮ ВРЕМЕНА КОГДА НЕ БЫЛО ЛЕГО...",
          "ЗАЕБАЛО ЖДАТЬ ДРОП....",
          "ПОЦАНЫ блять НУ ПОЖАЛУЙСТА РАЗВИВАЙТЕСЬ"]


async def tsitatka():
    global LAST_ONE

    while True:
        if LAST_ONE + timedelta(seconds=5) < datetime.utcnow():
            try:
                await bot.send_message(chat_id=shinomontazhka, text=choice(KIZARU))
                LAST_ONE = datetime.utcnow()
            except Exception as e:
                print(f"ошибка при отправке цитатки:\n{e}")
        else:
            await asyncio.sleep(kizaru_kd)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\nя - бот конча")


@dp.message()
async def lame_message_handler(message: types.Message) -> None:
    # id пользователя и текст его сообщения
    text = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        if chat_id == shinomontazhka:
            if user_id not in USERS:
                USERS.append(user_id)
                if user_id == vovan:
                    await message.reply("привет, вован")
                else:
                    await message.reply("ты не вован(((")
        elif chat_id == test:
            await message.answer("подтвердите пересылку в другой чат в консоли (надо энтер нажать)")
            chat = shinomontazhka
            if input(f"подтвердите пересылку в {chat} сообщения:\n{text}\n") == "":
                await message.send_copy(chat_id=chat)
                await message.reply("УСПЕХ!")
            else:
                await message.reply("отменено.")
        else:
            await message.answer("ты никто и звать тебя никак")
        print(f"{message.from_user.id} написал: {message.text}")

    except Exception as e:
        print(f"тварь на {message.from_user.id} / {message.from_user.full_name} че то сломала:\n{e}")


async def main() -> None:
    global bot

    bot = Bot(bot_token, parse_mode=ParseMode.HTML)
    await bot(DeleteWebhook(drop_pending_updates=True))
    asyncio.create_task(tsitatka())
    await dp.start_polling(bot)


if __name__ == "__main__":
    LAST_ONE = datetime.utcnow()

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())

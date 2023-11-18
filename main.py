import logging
import sys
import asyncio
from datetime import *
from random import choice
import openai


from config import *
from gpt import gpt_response_creation

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.methods import DeleteWebhook

#TODO фуннции при включении ботика и его оффе

openai.api_key = open_ai_api_key
dp = Dispatcher()
PRIVET_VOVAN_FLAG = True
KIZARU = ["ДА Я - ходячая энциклопедия хеп хопа нахуй",
          "НОУ РОЯЛТИ НОУ ЛОЯЛТИ",
          "помню времена, когда не было лего...",
          "ЗАЕБАЛО ЖДАТЬ ДРОП....",
          "ПОЦАНЫ блять НУ ПОЖАЛУЙСТА развиваАаАайтесь",
          "е, е, е, Е, еыеаывпвы",
          "весь репчик - это квадраты",
          "фит с алишером, похуй, кто нафидит",
          "ЛЕТО И АРБАЛЕТЫ, ща вагнера подъедут...",
          "БЛЯ УУУУУУ"]



# очередь на отправку запроса в OpenAI
QUEUE = tuple()
# номер сообщения
NUM = 1


async def tsitatka():
    global LAST_ONE

    while True:
        if LAST_ONE + timedelta(seconds=5) < datetime.utcnow():
            try:
                await bot.send_message(chat_id=shinomontazhka,
                                       text=f"как говорил великий:\n\"{choice(KIZARU)}\"",
                                       disable_notification=True)
                LAST_ONE = datetime.utcnow()
            except Exception as e:
                print(f"ошибка при отправке цитатки:\n{e}")
        else:
            await asyncio.sleep(kizaru_kd)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\n\nБЛЯ УУУУУУУУУ")


@dp.message()
async def lame_message_handler(message: types.Message) -> None:
    global PRIVET_VOVAN_FLAG

    # id пользователя и текст его сообщения
    text = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        if chat_id == shinomontazhka:
            if user_id == vovan and PRIVET_VOVAN_FLAG:
                await message.reply("привет, вован")
                PRIVET_VOVAN_FLAG = False
            if bot_name in text:
                global NUM, QUEUE, LAST_USE_TIME
                try:
                    # встали в очередь
                    pos, NUM = NUM, NUM + 1
                    QUEUE += (pos,)
                    please_wait = (QUEUE.index(pos) != 0 or
                                   LAST_USE_TIME + timedelta(seconds=open_ai_kd) > datetime.utcnow())
                    if please_wait:
                        await message.reply("Твой запрос в очереди на обработку!")
                    # ожидание очереди
                    while please_wait:
                        await asyncio.sleep(1)
                    # получаем ответ от модели
                    bot_answer = await gpt_response_creation(text.replace(bot_name, 'bot'))
                    await message.reply(bot_answer)
                finally:
                    # двигаем очередь
                    QUEUE, LAST_USE_TIME = QUEUE[1:], datetime.utcnow()

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
        print(f"{user_id} написал: {text}")

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
    LAST_USE_TIME = datetime.utcnow()
    asyncio.run(main())

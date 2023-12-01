import logging
import time
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from config import TOKEN

from database import DataBase



logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


db = DataBase()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.first_name:
        name = message.from_user.first_name
    else:
        name = 'неизвестно'

    db.create_user(message.from_user.id,message.from_user.username, name)

    photo = open("media/start.jpg", 'rb')
    caption = """Международная КиберШкола программирования для детей KiberOne приветствует вас 

Мастер-класс проходит по адресу:
📍Адмиралтейский район, Парфёновская ул., 14, корп. 1 (этаж 1)

✅ Ваш ребенок создаст свой первый мультфильм и запрограммирует своего героя в игре Майнкрафт 🖥️

✅ Длительность занятия 120 минут. Всё необходимое предоставим. Ничего брать с собой не нужно.

Чтобы записаться на бесплатный мастер-класс, выберите возраст вашего ребенка👇
"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("6-9 лет", "9-12 лет", "12-14 лет")

    await bot.send_photo(message.from_user.id, photo, caption=caption, reply_markup=markup)


@dp.message_handler(lambda message: message.text in ["6-9 лет", "9-12 лет", "12-14 лет"])
async def get_age(message: types.Message):
    db.add_age(message.text, message.from_user.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text="Отправить номер телефона", request_contact=True))
    await message.answer(
        "Укажите номер телефона. Наш администратор отправит вам расписание мастер-классов на ближайшую неделю и согласует точное время",
        reply_markup=markup)


@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message):
    db.add_phone(message.contact.phone_number, message.from_user.id)

    message_text = """Спасибо!

Скоро наш администратор свяжется с вами и согласует дату и время мастер-класса!

До встречи на уроке! 🤗"""
    markup = types.ReplyKeyboardRemove()
    await message.answer(message_text, reply_markup=markup)
    await send_lead(message)


async def send_lead(message: types.Message):
    user_data = db.get_user(message.from_user.id)
    lead_text = f"Имя: {user_data['name']}\nВозраст: {user_data['age']}\nТелефон: +{user_data['phone']}\nUsername: @{user_data['username']}"
    db.delete_user(message.from_user.id)
    await bot.send_message(-1002072461379, lead_text)


async def send_reminder(bot):
    users = db.get_user_ids_and_time()
    for user in users:
        dt_object = datetime.utcfromtimestamp(user[1])
        if (dt_object + timedelta(days=1) < datetime.now()):

            db.update_time(user[0])
            await bot.send_message(int(user[0]), "❗❗❗Напоминаем❗❗❗\nВы не поностью оставили заявку!")





if __name__ == '__main__':
    from aiogram import executor


    while True:
        try:
            scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
            scheduler.add_job(send_reminder, trigger='interval', seconds=60 * 60, kwargs={'bot': bot})
            scheduler.start()
            print('sheduler started!')
            print('Bot id running...')
            executor.start_polling(dp, skip_updates=True)
        except:
            print('error in main loop!')
        finally:
            print('Bot stopped!')




import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import TOKEN, ADMINS

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

info = {}


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
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
async def get_district(message: types.Message):
    info[message.from_user.username] = [message.text]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text="Отправить номер телефона", request_contact=True))
    await message.answer(
        "Укажите номер телефона. Наш администратор отправит вам расписание мастер-классов на ближайшую неделю и согласует точное время",
        reply_markup=markup)


@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message):
    phonenumber = str(message.contact.phone_number)
    info[message.from_user.username].append(phonenumber)

    message_text = """Спасибо!

Скоро наш администратор свяжется с вами и согласует дату и время мастер-класса!

До встречи на уроке! 🤗"""
    markup = types.ReplyKeyboardRemove()
    await message.answer(message_text, reply_markup=markup)

    await send_lead(message)


async def send_lead(message: types.Message):
    for admin_id in ADMINS:
        lead_text = f"Возраст: {info[message.from_user.username][0]}\nТелефон: {info[message.from_user.username][1]}\nUsername: @{message.from_user.username}"
        await bot.send_message(admin_id, lead_text)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)

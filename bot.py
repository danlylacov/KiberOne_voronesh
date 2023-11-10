import telebot
from config import TOKEN, ADMINS
from markups import choose_district, choose_age, send_phone, send_phone_remove

bot = telebot.TeleBot(TOKEN)

info = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.from_user.id, open("media/start.jpg", 'rb'), caption=
    """Международная КиберШкола программирования для детей KiberOne приветствует вас 
    
Мастер-класс проходит по адресу:
📍Адмиралтейский район, Парфёновская ул., 14, корп. 1 (этаж 1)
  
✅ Ваш ребенок создаст свой первый мультфильм и запрограммирует своего героя в игре Майнкрафт 🖥️

✅ Длительность занятия 120 минут. Всё необходимое предоставим. Ничего брать с собой не нужно.

Чтобы записаться на бесплатный мастер-класс, выберите возраст вашего ребенка👇
    """, reply_markup=choose_age)




@bot.message_handler(content_types=["text"])
def get_district(message):
    if message.text in ["6-9 лет", "9-12 лет", "12-14 лет"]:
        info[message.from_user.username] = [message.text]
        bot.send_message(message.from_user.id,
                         """Укажите номер телефона.
Наш администратор отправит вам расписание мастер-классов на ближайшую неделю и согласует точное время""",
                         reply_markup=send_phone)




@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        phonenumber = str(message.contact.phone_number)
        info[message.from_user.username].append(phonenumber)



        mesg = bot.send_message(message.chat.id, """Спасибо!

Скоро наш администратор свяжется с вами и согласует дату и время мастер-класса!

До встречи на уроке! 🤗""",
                         reply_markup=send_phone_remove())


        send_lead(message)


def send_lead(message):
    for id in ADMINS:
        bot.send_message(id, f"Возраст: {info[message.from_user.username][0]}\nТелефон: {info[message.from_user.username][1]}\n Username: @{message.from_user.username}")



bot.polling(none_stop=True)
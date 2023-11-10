import telebot
from config import TOKEN, ADMINS
from markups import choose_district, choose_age, send_phone, send_phone_remove

bot = telebot.TeleBot(TOKEN)

info = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.from_user.id, open("media/start.jpg", 'rb'), caption=
    """КиберШкола для детей KiberOne Санкт-Петербург приветствует вас 🤗
На этой неделе мы проводим бесплатный мастер-класс по программированию для детей 6-14 лет 💻
    
✅ Ваш ребенок создаст свой первый мультфильм и запрограммирует своего героя в игре Майнкрафт 🖥️

✅ Расскажем, как избавить ребенка от игромании и научить компьютерной грамотности, чтобы подготовить к успешному будущему

✅ Длительность занятия 60 минут. Все необходимое предоставим. Ничего брать с собой не нужно.

Где проходят мастер-классы:
    📍Адмиралтейский район, Парфёновская ул., 14, корп. 1 (этаж 1)
    📍Всеволожск, ул. Доктора Сотникова, 1, микрорайон Южный

Чтобы записаться на бесплатный мастер-класс, выберите удобный вам район 👇
    """, reply_markup=choose_district)



@bot.message_handler(content_types=["text"])
def get_district(message):
    if message.text =="Адмиралтейский" or message.text =="Адмиралтейский":
        info[message.from_user.username] = [message.text]
        bot.send_message(message.from_user.id,
                         "Укажите возраст вашего ребенка, чтобы мы подобрали для него оптимальную группу на мастер-класс👇",
                         reply_markup=choose_age)
    if message.text in ["6-9 лет", "9-12 лет", "12-14 лет"]:
        info[message.from_user.username].append(message.text)
        bot.send_message(message.from_user.id,
                         """Спасибо! Остался последний шаг😊
                         
Укажите номер телефона.
Наш администратор отправит вам расписание мастер-классов на ближайшую неделю и согласует точное время 🤗""",
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
        bot.send_message(id, f"Район: {info[message.from_user.username][0]}\nВозраст: {info[message.from_user.username][1]}\nТелефон: {info[message.from_user.username][2]}")



bot.polling(none_stop=True)
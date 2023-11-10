from telebot import types

choose_district = types.ReplyKeyboardMarkup(resize_keyboard=True)
choose_district.add("Адмиралтейский", "Всеволожский")


choose_age = types.ReplyKeyboardMarkup(resize_keyboard=True)
choose_age.add("6-9 лет", "9-12 лет", "12-14 лет")


send_phone = types.ReplyKeyboardMarkup(resize_keyboard=True)
send_phone.add(types.KeyboardButton(text="Отправить номер телефона", request_contact=True))

def send_phone_remove():
    return types.ReplyKeyboardRemove()



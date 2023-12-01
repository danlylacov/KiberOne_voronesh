import datetime
import sqlite3
import time


class DataBase():
    def __init__(self):
        self._db = sqlite3.connect('bot.db')
        self._cur = self._db.cursor()
        self._cur.execute("CREATE TABLE IF NOT EXISTS user("
                         "id INTEGER PRIMARY KEY NOT NULL,"
                         "userId INTEGER NOT NULL,"
                        "name STRING,"
                         "username STRING,"
                         "age STRING,"
                         "phone STRING,"
                         "time REAL"
                         ");")
        self._db.commit()


    def create_user(self, user_id, username, name):
        self._cur.execute("INSERT INTO user(userId, username, name, age, phone, time) VALUES (?, ?, ?,  NULL, NULL, ?)", (user_id, username, name, time.time()))
        self._db.commit()


    def add_age(self, age, user_id):
        self._cur.execute("UPDATE user SET age = ? WHERE userId = ?;", (age, user_id))
        self._db.commit()


    def add_phone(self, phone, user_id):
        self._cur.execute("UPDATE user SET phone = ? WHERE userId = ?;", (phone, user_id))
        self._db.commit()


    def get_user(self, user_id):
        user = self._cur.execute('SELECT username, name, age, phone FROM user WHERE userId = ?', (user_id,)).fetchone()
        return {'username' : user[0], 'name' : user[1], 'age' : user[2], 'phone' : user[3]}


    def delete_user(self, user_id):
        self._cur.execute('DELETE FROM user WHERE userId = ?', (user_id,))
        self._db.commit()


    def get_user_ids_and_time(self):
        users = self._cur.execute('SELECT userId, time FROM user').fetchall()
        return users

    def update_time(self, user_id):
        self._cur.execute('UPDATE user SET time = ? WHERE userId = ?', (time.time(), user_id,))
        self._db.commit()


db = DataBase()
db.get_user_ids_and_time()







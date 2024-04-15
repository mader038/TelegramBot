import sqlite3
from formules import is_leap_year
from translate import Translator
import requests

bd_name = 'birthdates.db'

months_for_data = {
    'January': 'Январь 🎄',
    'February': 'Февраль ❄',
    'March': 'Март 🌷',
    'April': 'Апрель 💨',
    'May': 'Май 🌿',
    'June': 'Июнь 🌊',
    'July': 'Июль 🍓',
    'August': 'Август ☀',
    'September': 'Сентябрь 📚',
    'October': 'Октябрь 🥶',
    'November': 'Ноябрь 🧤',
    'December': 'Декабрь 🍊'
}

months_data = {
    'January': 'Января',
    'February': 'Февраля',
    'March': 'Марта',
    'April': 'Апреля',
    'May': 'Мая',
    'June': 'Июня',
    'July': 'Июля',
    'August': 'Августа',
    'September': 'Сентября',
    'October': 'Октября',
    'November': 'Ноября',
    'December': 'Декабря'
}

months_days = {
    'January': 31,
    'February': 28,
    'March': 31,
    'April': 30,
    'May': 31,
    'June': 30,
    'July': 31,
    'August': 31,
    'September': 30,
    'October': 31,
    'November': 30,
    'December': 31
}


def check_date_birth(day, month, year):
    if is_leap_year(int(year)) and str(month) == 'February':
        if int(day) > int(months_days.get(str(month))) + 1:
            return False
        else:
            return True
    else:
        if int(day) > int(months_days.get(str(month))):
            return False
        else:
            return True


def checker_people(id):
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    checker = cur.execute("""SELECT * FROM people WHERE userid = ?""", (id,)).fetchone()
    if checker == None:
        return True
    else:
        return False


def deleter_friend(id, choose):
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    result = cur.execute("""SELECT * from users WHERE inviter = ? AND id = ?""", (id, choose,)).fetchall()
    for elem in result:
        if int(elem[0]) == choose:
            count = cur.execute("""DELETE FROM users WHERE id = ?""", (choose,))
            con.commit()
            return True
        else:
            continue
    return False


def return_all(id):
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    result = cur.execute("""SELECT * from users WHERE inviter = ?""", (id,)).fetchall()
    return result


def birth_now_months(id, month):
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    result = cur.execute("""SELECT * from users WHERE inviter = ? AND month = ?""", (id, month,)).fetchall()
    return result


def owner_birth(id):
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    result = cur.execute("""SELECT * from people WHERE userid = ?""", (id,)).fetchone()
    return result[5:8]


def search_birth(day, month, invite):
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    result = cur.execute("""SELECT * from users WHERE inviter = ? AND day = ? AND month = ?""",
                         (invite, day, month,)).fetchall()
    return result


def all_users():
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    result = cur.execute("""SELECT * from users""").fetchall()
    return result


def all_people():
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    result = cur.execute("""SELECT * from people""").fetchall()
    return result


def translate_text(text, target_language='ru'):
    translator = Translator(to_lang=target_language)
    translated_text = translator.translate(text)
    return translated_text


def get_holidays(year, month, day):
    url = "https://calendarific.com/api/v2/holidays"
    params = {
        "api_key": 'qWs9IHHpJDEkc69S9xvbNxJtmlmKaQyB',
        "country": 'RU',
        "year": year,
        "month": month,
        "day": day
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['response']['holidays']
    else:
        print("Ошибка при запросе:", response.status_code)
        return None

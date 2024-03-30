import sqlite3

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


def checker_people(id):
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    checker = cur.execute("""SELECT * FROM people WHERE userid = ?""", (id,)).fetchone()
    if checker == None:
        return True
    else:
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

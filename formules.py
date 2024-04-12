import datetime
from natasha import MorphVocab

morph_vocab = MorphVocab()


def month_to_number(month_name):  # Из месяца в число ( January -> 1 )
    month = datetime.datetime.strptime(month_name, "%B").month
    return month


def number_to_month(month_number):  # Из числа в месяц ( 1 -> January )
    month_name = datetime.date(2022, month_number, 2).strftime('%B')
    return month_name


def calc_age(year, month, day):  # Калькулятор возраста
    now = datetime.datetime.now().date()
    old = datetime.date(year, month, day)
    return (now - old).days // 365


def is_leap_year(year):  # Проверка на високосность года
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False


def days_until_birthday(year, month, day):  # Подсчёт дней до дня рождения
    today = datetime.date.today()
    birthday = datetime.date(year, month, day)

    if birthday < today:
        birthday = birthday.replace(year=today.year + 1)

    days_to_birthday = (birthday - today).days
    if days_to_birthday > 366:
        if is_leap_year(today.year):
            return days_to_birthday - 365
        else:
            return days_to_birthday - 366
    else:
        return days_to_birthday


def birth_nearests(days):
    calc = datetime.datetime.today() + datetime.timedelta(days=days)
    return str(calc.date()).split('-')

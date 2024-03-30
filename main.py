import datetime
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, KeyboardButton, \
    ReplyKeyboardMarkup
import databaseBot
from databaseBot import checker_people, return_all, birth_now_months, owner_birth, search_birth
from formules import month_to_number, number_to_month, calc_age, days_until_birthday, birth_nearests

BOT_TOKEN = '6832196238:AAHOMT7xy4omFntn2k-pjn6-M4A8Q3NO3Xs'

admins = [1022869374]

storage = MemoryStorage()

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=storage)

command1 = KeyboardButton(text='🎉 Дни рождения в этом месяце')
command2 = KeyboardButton(text='🍾 Ближайший день рождения')
command3 = KeyboardButton(text='🎊 Все дни рождения')
command4 = KeyboardButton(text='Когда мой день рождения? 🤔')
command5 = KeyboardButton(text='Добавить день рождение друга 💋')
command6 = KeyboardButton(text='Удалить друга из списка 😕')
command7 = KeyboardButton(text='🔗 Помощь')

keyboard_all = ReplyKeyboardMarkup(keyboard=[[command1, command4],
                                             [command2, command5],
                                             [command3, command6],
                                             [command7]],
                                   resize_keyboard=True)


@dp.message(CommandStart())  # Хендлер срабатывающий на команду /start
async def process_start_command(message: Message):
    if checker_people(message.from_user.id):
        print(f'Уоп, новый юзер {message.from_user.username} {message.from_user.first_name} {message.from_user.id}')
        register = InlineKeyboardButton(
            text='Зарегестрироваться! 🔥',
            callback_data='register_pressed'
        )
        regist = InlineKeyboardMarkup(
            inline_keyboard=[[register]]
        )
        await message.answer(
            text='Привет!! Я твой универсальный помощник по дням рождениям!\n'
                 'Прежде чем мы начнём с тобой работать, я попрошу тебя зарегестрироваться. 😝\n'
                 'От тебя почти ничего не требуется! Просто нажмите кнопочку ниже) ⬇️',
            reply_markup=regist
        )
    else:
        returned_user = InlineKeyboardButton(
            text='В меню! 🥳',
            callback_data='returns_pressed'
        )
        returned = InlineKeyboardMarkup(
            inline_keyboard=[[returned_user]]
        )
        await message.answer(
            text='С возвращением! Вижу ты уже когда то был зарегестрирован!\n'
                 'Нажми на кнопочку ниже чтобы начать пользоваться моими навыками! 😉',
            reply_markup=returned
        )


@dp.callback_query(F.data == 'returns_pressed')
async def help2(callback: CallbackQuery):
    help_bot = InlineKeyboardButton(
        text='🔗 Помощь',
        callback_data='help_pressed'
    )
    menu_button = InlineKeyboardMarkup(
        inline_keyboard=[[help_bot]]
    )
    await callback.message.answer(
        text='Вжууух! ‍🌫️',
        reply_markup=keyboard_all
    )
    await callback.message.answer(
        text='Вы попали в меню!\n'
             'Просто выбери нужную тебе команду\n'
             'И я тут же тебе отвечу. 😉',
        reply_markup=menu_button
    )


@dp.callback_query(F.data == 'help_pressed')
async def help2(callback: CallbackQuery):
    await callback.message.answer(
        text='Привет 👋, вот мои команды!!\n'
             '1. /births_in_now_months - Дни рождения в текущем месяце.\n'
             '2. /births_nearest - Ближайший день рождения.\n'
             '3. /every_births - Все дни рождения друзей.\n'
             '4. /my_births - Сколько осталось до твоего дня рождения.\n'
             '5. /delete_friend - Удалить друга из списка.\n\n'
             'Если что, под клавиатурой есть кнопки, ты всегда можешь функционировать с ними! ❤\n\n'
             '🚨 Чтобы вам не выводило, что у вас пусто среди друзей, то просто добавьте их!\n'
             '/add_births - Добавь друга в свой список!',
        reply_markup=keyboard_all
    )


@dp.message(Command(commands='help'))
@dp.message(F.text == '🔗 Помощь')
async def help(message: Message):
    await message.answer(
        text='Привет 👋, вот мои команды!!\n'
             '1. /births_in_now_months - Дни рождения в текущем месяце.\n'
             '2. /births_nearest - Ближайший день рождения.\n'
             '3. /every_births - Все дни рождения друзей.\n'
             '4. /my_births - Сколько осталось до твоего дня рождения.\n'
             '5. /delete_friend - Удалить друга из списка.\n\n'
             'Если что, под клавиатурой есть кнопки, ты всегда можешь функционировать с ними! ❤\n\n'
             '🚨 Чтобы вам не выводило, что у вас пусто среди друзей, то просто добавьте их!\n'
             '/add_births - Добавь друга в свой список!',
        reply_markup=keyboard_all
    )


@dp.message(Command(commands='births_in_now_months'))
@dp.message(F.text == '🎉 Дни рождения в этом месяце')
async def birth_in_now_months(message: Message):
    result = birth_now_months(message.from_user.id, number_to_month(datetime.date.today().month))
    text = f'{databaseBot.months_for_data.get(number_to_month(datetime.date.today().month))}\n'
    if result == list():
        text += f'Похоже тут ничего нет..'
        await message.answer(text)
    else:
        for elem in result:
            text += f'• {elem[1]} {elem[2]}, {elem[4]} {databaseBot.months_data.get(elem[5])}' \
                    f', {calc_age(elem[6], month_to_number(elem[5]), elem[4])} лет\n'
        await message.answer(text)


@dp.message(Command(commands='every_births'))
@dp.message(F.text == '🎊 Все дни рождения')
async def every_births(message: Message):
    for mounth_num in range(1, 13):
        result = birth_now_months(message.from_user.id, number_to_month(mounth_num))
        text = f'{databaseBot.months_for_data.get(number_to_month(mounth_num))}\n'
        if result == list():
            text += f'Похоже тут ничего нет..'
            await message.answer(text)
        else:
            for elem in result:
                text += f'• {elem[1]} {elem[2]}, {elem[4]} {databaseBot.months_data.get(elem[5])}' \
                        f', {calc_age(elem[6], month_to_number(elem[5]), elem[4])} лет\n'
            await message.answer(text)


@dp.message(Command(commands='my_births'))
@dp.message(F.text == 'Когда мой день рождения? 🤔')
async def every_births(message: Message):
    id_user = message.from_user.id
    if checker_people(id_user):
        await message.answer(
            f'Похоже вы не зарегестрировались..\n'
            f'Напишите /start и пройдете регистрацию.'
        )
    else:
        await message.answer(
            f'До вашего дня рождения осталось '
            f'{days_until_birthday(owner_birth(id_user)[2], month_to_number(owner_birth(id_user)[1]), owner_birth(id_user)[0])}'
            f' суток! 🥰')


@dp.message(Command(commands='births_nearest'))
@dp.message(F.text == '🍾 Ближайший день рождения')
async def birth_nearest(message: Message):
    days = list()
    gender = ''
    friends = return_all(message.from_user.id)
    for elem in friends:
        days.append(days_until_birthday(elem[6], month_to_number(elem[5]), elem[4]))
    if days != list():
        calculator = birth_nearests(min(days))
        search = search_birth(calculator[2], number_to_month(int(calculator[1])), message.from_user.id)
        for people in search:
            if people[3] == 'male':
                gender = 'его'
            else:
                gender = 'ее'
            await message.answer(
                f'Ближайший день рождения, будет у {people[1]} {people[2]}!\n'
                f'Дата {gender} дня рождения: {people[4]} {databaseBot.months_data.get(people[5])} {people[6]} года.\n'
                f'До этой даты осталось {min(days)} суток!'
            )
    else:
        await message.answer(
            f'Похоже ваш список пуст.. 😞\n'
            f'Добавьте друзей с помощью команды /add_births 😁'
        )


@dp.message(Command(commands='delete_friend'))
@dp.message(F.text == 'Удалить друга из списка 😕')
async def delete_birth(message: Message):
    await message.answer(
        text='Приносим свои извинения.. Данная функция ещё не доступна. 😞'
    )


if __name__ == '__main__':
    dp.run_polling(bot)

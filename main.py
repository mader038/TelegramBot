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
from databaseBot import checker_people, return_all, birth_now_months, owner_birth, search_birth, check_date_birth, \
    deleter_friend, all_users, all_people, get_holidays, translate_text
from formules import month_to_number, number_to_month, calc_age, days_until_birthday, birth_nearests

BOT_TOKEN = '6832196238:AAHOMT7xy4omFntn2k-pjn6-M4A8Q3NO3Xs'

admins_id = [1022869374]

storage = MemoryStorage()

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=storage)

command1 = KeyboardButton(text='🎉 Дни рождения в этом месяце', resize_keyboard=True)
command2 = KeyboardButton(text='🍾 Ближайший день рождения', resize_keyboard=True)
command3 = KeyboardButton(text='🎊 Все дни рождения', resize_keyboard=True)
command4 = KeyboardButton(text='Когда мой день рождения? 🤔', resize_keyboard=True)
command5 = KeyboardButton(text='Добавить день рождение друга 💋', resize_keyboard=True)
command6 = KeyboardButton(text='Удалить друга из списка 😕', resize_keyboard=True)
command9 = KeyboardButton(text='🥳 Праздники сегодня', resize_keyboard=True)
command0 = KeyboardButton(text='Ближайший праздник 🤩', resize_keyboard=True)
command7 = KeyboardButton(text='🔗 Помощь', resize_keyboard=True)

keyboard_all = ReplyKeyboardMarkup(keyboard=[[command1, command4],
                                             [command2, command9, command0, command5],
                                             [command3, command6],
                                             [command7]],
                                   resize_keyboard=True)


class FSMFillForm(StatesGroup):
    fill_firstname = State()  # Состояние ожидания ввода имени
    fill_lastname = State()  # Состояние ожидания ввода фамилии
    fill_gender = State()  # Состояние ожидания выбора пола
    fill_age = State()  # Состояние ожидания ввода возраста
    fill_day = State()  # Состояние ожидания ввода дня
    fill_month = State()  # Состояние ожидания выбора месяца
    fill_year = State()  # Состояние ожидания ввода года


class registerFSM(StatesGroup):
    fill_day_birth = State()  # Состояние ожидания ввода дня
    fill_month_birth = State()  # Состояние ожидания выбора месяца
    fill_year_birth = State()  # Состояние ожидания ввода года


class deleterFSM(StatesGroup):
    fill_id_friend = State()  # Состояние ожидания ввода id


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
    admin_function = InlineKeyboardButton(
        text='🚨 Админ-панель',
        callback_data='admin_pressed'
    )
    if callback.from_user.id in admins_id:
        menu_button = InlineKeyboardMarkup(
            inline_keyboard=[[help_bot],
                             [admin_function]]
        )
    else:
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


@dp.callback_query(F.data == 'admin_pressed')
async def admin_panel(callback: CallbackQuery):
    user_button = InlineKeyboardButton(
        text='🟢 Все пользователи (user)',
        callback_data='us_pressed'
    )
    people_button = InlineKeyboardButton(
        text='🔴 Все пользователи (people)',
        callback_data='pe_pressed'
    )
    admin_buttons = InlineKeyboardMarkup(
        inline_keyboard=[[user_button],
                         [people_button]]
    )
    if callback.from_user.id in admins_id:
        await callback.message.answer(
            text=f'Здравствуйте, {callback.from_user.username}, выберите дей-ие 😉',
            reply_markup=admin_buttons
        )
    else:
        await callback.message.reply(text='Извините, моя твоя не понимать')


@dp.callback_query(F.data == 'us_pressed')
async def us_table(callback: CallbackQuery):
    if callback.from_user.id in admins_id:
        result = all_users()
        text = ''
        for elem in result:
            text += f'{elem[0]}:  {elem[1]}, {elem[2]}, {elem[3]}, {elem[4]} {elem[5]} {elem[6]}, {elem[7]}\n'
        await callback.message.answer(text)
    else:
        await callback.message.reply(text='Извините, моя твоя не понимать')


@dp.callback_query(F.data == 'pe_pressed')
async def pe_table(callback: CallbackQuery):
    if callback.from_user.id in admins_id:
        result = all_people()
        text = ''
        for elem in result:
            text += f'{elem[0]}:  {elem[1]}, {elem[3]}, {elem[4]}\n'
        await callback.message.answer(text)
    else:
        await callback.message.reply(text='Извините, моя твоя не понимать')


@dp.callback_query(F.data == 'help_pressed')
async def help2(callback: CallbackQuery):
    await callback.message.answer(
        text='Привет 👋, вот мои команды!!\n'
             '1. /births_in_now_months - Дни рождения в текущем месяце.\n'
             '2. /births_nearest - Ближайший день рождения.\n'
             '3. /every_births - Все дни рождения друзей.\n'
             '4. /my_births - Сколько осталось до твоего дня рождения.\n'
             '5. /delete_friend - Удалить друга из списка.\n'
             '6. /holidays - Праздники сегодня.\n'
             '7. /holidays_nearest - Ближайший праздник.\n\n'
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
             '5. /delete_friend - Удалить друга из списка.\n'
             '6. /holidays - Праздники сегодня.\n'
             '7. /holidays_nearest - Ближайший праздник.\n\n'
             'Если что, под клавиатурой есть кнопки, ты всегда можешь функционировать с ними! ❤\n\n'
             '🚨 Чтобы вам не выводило, что у вас пусто среди друзей, то просто добавьте их!\n'
             '/add_births - Добавь друга в свой список!',
        reply_markup=keyboard_all
    )


@dp.message(Command(commands='holidays'))
@dp.message(F.text == '🥳 Праздники сегодня')
async def holiday_today(message: Message):
    holidays = get_holidays(datetime.datetime.today().year, int(datetime.datetime.today().month),
                            datetime.datetime.today().day)
    if holidays:
        text = f"Список праздников на {datetime.datetime.today().date()}:\n"
        for holiday in holidays:
            text += f"- {translate_text(holiday['name'])}\n"
        await message.answer(text)
    else:
        await message.answer("Сегодня в России нету праздников. 😞")


@dp.message(Command(commands='holidays_nearest'))
@dp.message(F.text == 'Ближайший праздник 🤩')
async def holiday_nearest(message: Message):
    await message.answer('Пожалуйста, подождите, выполняется поиск...')
    flag = True
    start = datetime.datetime.today().date()
    count = 1
    while flag:
        holidays = get_holidays(start.year, int(start.month), start.day)
        if holidays:
            text = f"Список праздников на {start}:\n"
            for holiday in holidays:
                text += f"- {translate_text(holiday['name'])}\n"
            await message.answer(text)
            break
        else:
            start += datetime.timedelta(days=count)
            count += 1


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
            f'д. 🥰')


@dp.message(Command(commands='births_nearest'))
@dp.message(F.text == '🍾 Ближайший день рождения')
async def birth_nearest(message: Message):
    gender = ''
    friends = return_all(message.from_user.id)
    days = list()
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
async def delete_birth(message: Message, state: FSMContext):
    friends = ''
    if return_all(message.from_user.id) != list():
        await message.answer('Вы действительно хотите удалить друга? Хорошо, вот ваши друзья:')
        for elem in return_all(message.from_user.id):
            friends += f'ID: {elem[0]} - {elem[1]} {elem[2]} ({elem[4]}.{month_to_number(elem[5])}.{elem[6]})\n'
        await message.answer(friends)
        await message.answer('Хорошо, а теперь пожалуйста введите ID вашего друга!\n'
                             'Если вы передумали, то используйте /cancel')
        await state.set_state(deleterFSM.fill_id_friend)
    else:
        await message.answer(
            f'Похоже ваш список пуст.. 😞\n'
            f'Добавьте друзей с помощью команды /add_births 😁'
        )


# Дальше идут машины состояний.


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из машины состояний\n\n'
             'Чтобы снова перейти к заполнению анкеты - '
             'отправьте команду /add_births или /delete_friend'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


#  Этот хендлер ловит id друга, чтобы удалить его из бд.
@dp.message(StateFilter(deleterFSM.fill_id_friend),
            lambda x: x.text.isdigit())
async def process_delete(message: Message, state: FSMContext):
    id_text = int(message.text)
    if deleter_friend(message.from_user.id, id_text):
        await message.answer('Друг успешно удалён!')
    else:
        await message.answer('Возможно неверный ID, пожалуйста, попробуйте заново! 🤕\n'
                             'Для этого используйте команду /delete_friend')
    await state.clear()


@dp.message(StateFilter(deleterFSM.fill_id_friend))
async def warning_not_day(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на ID\n\n'
             'Пожалуйста, введите ID в цифрах до дефиса.\n\n'
             'Если вы хотите прервать заполнение - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего.\n\n'
             'Чтобы перейти к добавлению дня рождения - '
             'отправьте команду /add_births'
    )


@dp.callback_query(F.data == 'register_pressed')
async def process_fillform_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пожалуйста, введите ДЕНЬ вашего рождения.')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(registerFSM.fill_day_birth)


# Этот хэндлер будет срабатывать, если отправлен день
# и переводить в состояние выбора месяца
@dp.message(StateFilter(registerFSM.fill_day_birth),
            lambda x: x.text.isdigit() and 1 <= int(x.text) <= 31)
async def process_day_senter(message: Message, state: FSMContext):
    await state.update_data(day_own=message.text)
    # Создаем объекты инлайн-кнопок
    january_button = InlineKeyboardButton(
        text='Январь',
        callback_data='January'
    )
    february_button = InlineKeyboardButton(
        text='Февраль',
        callback_data='February'
    )
    march_button = InlineKeyboardButton(
        text='Март',
        callback_data='March'
    )
    april_button = InlineKeyboardButton(
        text='Апрель',
        callback_data='April'
    )
    may_button = InlineKeyboardButton(
        text='Май',
        callback_data='May'
    )
    june_button = InlineKeyboardButton(
        text='Июнь',
        callback_data='June'
    )
    july_button = InlineKeyboardButton(
        text='Июль',
        callback_data='July'
    )
    august_button = InlineKeyboardButton(
        text='Август',
        callback_data='August'
    )
    september_button = InlineKeyboardButton(
        text='Сентябрь',
        callback_data='September'
    )
    october_button = InlineKeyboardButton(
        text='Октябрь',
        callback_data='October'
    )
    november_button = InlineKeyboardButton(
        text='Ноябрь',
        callback_data='November'
    )
    decemver_button = InlineKeyboardButton(
        text='Декабрь',
        callback_data='December'
    )
    # Добавляем кнопки в клавиатуру
    keyboard: list[list[InlineKeyboardButton]] = [
        [january_button, february_button],
        [march_button, april_button],
        [may_button, june_button],
        [july_button, august_button],
        [september_button, october_button],
        [november_button, decemver_button]
    ]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Спасибо!\n\nУкажите месяц',
        reply_markup=markup
    )
    # Устанавливаем состояние ожидания выбора месяца
    await state.set_state(registerFSM.fill_month_birth)


# Этот хэндлер будет срабатывать, если во время отправки дня
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(registerFSM.fill_day_birth))
async def warning_not_day(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на день\n\n'
             'Пожалуйста, введите ДЕНЬ (не месяц, не год)\n\n'
             'Если вы хотите прервать заполнение - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать, если выбран месяц
# и переводить в состояние года
@dp.callback_query(StateFilter(registerFSM.fill_month_birth),
                   F.data.in_(['January', 'February', 'March', 'April', 'May', 'June',
                               'July', 'August', 'September', 'October', 'November', 'December']))
async def process_months_presser(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные об образовании по ключу "months"
    await state.update_data(month_own=callback.data)
    await callback.message.delete()
    # Редактируем предыдущее сообщение с кнопками, отправляя
    # новый текст и новую клавиатуру
    await callback.message.answer(
        text='Спасибо! А теперь введите год вашего рождения'
    )
    # Устанавливаем состояние ожидания выбора года
    await state.set_state(registerFSM.fill_year_birth)


# Этот хэндлер будет срабатывать, если во время выбора месяца
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(registerFSM.fill_month_birth))
async def warning_not_education(message: Message):
    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками при выборе месяца\n\n'
             'Если вы хотите прервать заполнение анкеты - отправьте '
             'команду /cancel'
    )


# Этот хэндлер будет срабатывать на год
@dp.message(StateFilter(registerFSM.fill_year_birth),
            lambda x: x.text.isdigit() and 1900 <= int(x.text) <= 2024)
async def process_day_sent(message: Message, state: FSMContext):
    await state.update_data(year_own=message.text)
    if check_date_birth(int((await state.get_data()).get('day_own')), str((await state.get_data()).get('month_own')),
                        int((await state.get_data()).get('year_own'))):
        con = sqlite3.connect('birthdates.db')

        cur = con.cursor()

        count = cur.execute("""INSERT INTO people (userid, nameuser, name, dayy, monthh, year)
                VALUES (?, ?, ?, ?, ?, ?);""", (str(message.from_user.id),
                                                str(message.from_user.first_name),
                                                str(message.from_user.username),
                                                (await state.get_data()).get('day_own'),
                                                (await state.get_data()).get('month_own'),
                                                (await state.get_data()).get('year_own')))
        con.commit()
        con.close()
        returned_user = InlineKeyboardButton(
            text='В меню! 🥳',
            callback_data='returns_pressed'
        )
        returned = InlineKeyboardMarkup(
            inline_keyboard=[[returned_user]]
        )
        await message.answer(
            text='Вы успешно зарегестрировались!',
            reply_markup=returned
        )
    else:
        register = InlineKeyboardButton(
            text='Зарегестрироваться! 🔥',
            callback_data='register_pressed'
        )
        regist = InlineKeyboardMarkup(
            inline_keyboard=[[register]]
        )
        await message.answer(text='Похоже вы ввели неккоректную дату, пожалуйста, попробуйте заново! 🫢',
                             reply_markup=regist)
    await state.clear()


# Этот хэндлер будет срабатывать, если во время согласия на получение
# новостей будет введено/отправлено что-то некорректное
@dp.message(StateFilter(registerFSM.fill_year_birth))
async def warning_not_year(message: Message):
    await message.answer(
        text='Пожалуйста, введите ГОД!\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать на команду /add_births
# и переводить бота в состояние ожидания ввода имени
@dp.message(Command(commands='add_births'), StateFilter(default_state))
@dp.message(F.text == 'Добавить день рождение друга 💋')
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите имя друга')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_firstname)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода фамилии
@dp.message(StateFilter(FSMFillForm.fill_firstname), F.text.isalpha())
async def process_firstname_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "firstname"
    await state.update_data(firstname=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите фамилию друга')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_lastname)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_firstname))
async def warning_not_firstname(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на имя\n\n'
             'Пожалуйста, введите имя друга\n\n'
             'Если вы хотите прервать заполнение - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать, если введен корректная фамилия
# и переводить в состояние выбора пола
@dp.message(StateFilter(FSMFillForm.fill_lastname), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "lastname"
    await state.update_data(lastname=message.text)
    # Создаем объекты инлайн-кнопок
    male_button = InlineKeyboardButton(
        text='Мужской ♂',
        callback_data='male'
    )
    female_button = InlineKeyboardButton(
        text='Женский ♀',
        callback_data='female'
    )
    keyboard: list[list[InlineKeyboardButton]] = [[male_button, female_button]]  # Добавляем кнопки в клавиатуру
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)  # Создаем объект инлайн-клавиатуры
    await message.answer(
        text='Спасибо!\n\nУкажите пол друга',
        reply_markup=markup
    )
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_gender)


# Этот хэндлер будет срабатывать, если во время ввода фамилии
# будет введено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_lastname))
async def warning_not_lastname(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на фамилию\n\n'
             'Пожалуйста, введите фамилию друга\n\n'
             'Если вы хотите прервать заполнение - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать на нажатие кнопки при
# выборе пола и переводить в состояние ввода дня
@dp.callback_query(StateFilter(FSMFillForm.fill_gender),
                   F.data.in_(['male', 'female']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище, по ключу "gender"
    await state.update_data(gender=callback.data)
    # Удаляем сообщение с кнопками
    await callback.message.delete()
    await callback.message.answer(
        text='Спасибо! А теперь введите ДЕНЬ рождения вашего друга'
    )
    # Устанавливаем состояние ожидания заполнения дня
    await state.set_state(FSMFillForm.fill_day)


# Этот хэндлер будет срабатывать, если во время выбора пола
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_gender))
async def warning_not_gender(message: Message):
    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             'при выборе пола\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать, если отправлен день
# и переводить в состояние выбора месяца
@dp.message(StateFilter(FSMFillForm.fill_day),
            lambda x: x.text.isdigit() and 1 <= int(x.text) <= 31)
async def process_day_sent(message: Message, state: FSMContext):
    await state.update_data(days=message.text)
    # Создаем объекты инлайн-кнопок
    january_button = InlineKeyboardButton(
        text='Январь',
        callback_data='January'
    )
    february_button = InlineKeyboardButton(
        text='Февраль',
        callback_data='February'
    )
    march_button = InlineKeyboardButton(
        text='Март',
        callback_data='March'
    )
    april_button = InlineKeyboardButton(
        text='Апрель',
        callback_data='April'
    )
    may_button = InlineKeyboardButton(
        text='Май',
        callback_data='May'
    )
    june_button = InlineKeyboardButton(
        text='Июнь',
        callback_data='June'
    )
    july_button = InlineKeyboardButton(
        text='Июль',
        callback_data='July'
    )
    august_button = InlineKeyboardButton(
        text='Август',
        callback_data='August'
    )
    september_button = InlineKeyboardButton(
        text='Сентябрь',
        callback_data='September'
    )
    october_button = InlineKeyboardButton(
        text='Октябрь',
        callback_data='October'
    )
    november_button = InlineKeyboardButton(
        text='Ноябрь',
        callback_data='November'
    )
    decemver_button = InlineKeyboardButton(
        text='Декабрь',
        callback_data='December'
    )
    # Добавляем кнопки в клавиатуру
    keyboard: list[list[InlineKeyboardButton]] = [
        [january_button, february_button],
        [march_button, april_button],
        [may_button, june_button],
        [july_button, august_button],
        [september_button, october_button],
        [november_button, decemver_button]
    ]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Спасибо!\n\nУкажите месяц',
        reply_markup=markup
    )
    # Устанавливаем состояние ожидания выбора месяца
    await state.set_state(FSMFillForm.fill_month)


# Этот хэндлер будет срабатывать, если во время отправки дня
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_day))
async def warning_not_day(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на день\n\n'
             'Пожалуйста, введите ДЕНЬ (не месяц, не год)\n\n'
             'Если вы хотите прервать заполнение - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать, если выбран месяц
# и переводить в состояние года
@dp.callback_query(StateFilter(FSMFillForm.fill_month),
                   F.data.in_(['January', 'February', 'March', 'April', 'May', 'June',
                               'July', 'August', 'September', 'October', 'November', 'December']))
async def process_education_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные об образовании по ключу "months"
    await state.update_data(months=callback.data)
    await callback.message.delete()
    # Редактируем предыдущее сообщение с кнопками, отправляя
    # новый текст и новую клавиатуру
    await callback.message.answer(
        text='Спасибо! А теперь введите год рождения вашего друга'
    )
    # Устанавливаем состояние ожидания выбора получать новости или нет
    await state.set_state(FSMFillForm.fill_year)


# Этот хэндлер будет срабатывать, если во время выбора месяца
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_month))
async def warning_not_education(message: Message):
    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками при выборе месяца\n\n'
             'Если вы хотите прервать заполнение анкеты - отправьте '
             'команду /cancel'
    )


# Этот хэндлер будет срабатывать на год
@dp.message(StateFilter(FSMFillForm.fill_year),
            lambda x: x.text.isdigit() and 1900 <= int(x.text) <= 2024)
async def process_day_sent(message: Message, state: FSMContext):
    await state.update_data(years=message.text)
    # Завершаем машину состояний
    if check_date_birth((await state.get_data()).get('days'), (await state.get_data()).get('months'),
                        (await state.get_data()).get('years')):
        con = sqlite3.connect('birthdates.db')

        cur = con.cursor()

        count = cur.execute("""INSERT INTO users (firstname, lastname, gender, day, month, year, inviter)
                VALUES (?, ?, ?, ?, ?, ?, ?);""", ((await state.get_data()).get('firstname'),
                                                   (await state.get_data()).get('lastname'),
                                                   (await state.get_data()).get('gender'),
                                                   (await state.get_data()).get('days'),
                                                   (await state.get_data()).get('months'),
                                                   (await state.get_data()).get('years'),
                                                   str(message.from_user.id)))
        con.commit()
        await message.answer(
            text='Друг успешно добавлен!'
        )
    else:
        await message.answer('Похоже, вы ввели неккоректную дату, пожалуйста, попробойте заново! 🤕')
    await state.clear()


# Этот хэндлер будет срабатывать, если во время согласия на получение
# новостей будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_year))
async def warning_not_year(message: Message):
    await message.answer(
        text='Пожалуйста, введите ГОД!\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@dp.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, моя твоя не понимать')


if __name__ == '__main__':
    dp.run_polling(bot)

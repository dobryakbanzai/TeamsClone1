import telebot
from telebot import types
from config import *
from teamsClone.view_web.views import *
from teamsClone.views import *
import re

blocks = ["А", "Б", "В", "Г", "Д", "И", "К"]

bot = telebot.TeleBot(TOKEN_BOT)

channel_id = CHANNEL_ID

block = "_"
cab = "_"
id_experiment = 0
issue_msg_id = "_"
closing = False

# teacher
group = None # обязательно
title = None # обязательно
description = None # обязательно
startDL = None # обязательно
stopDL = None  # обязательно
file_task_bytes = [] # не обязательно
file_name = None # не обязательно
file_task = None
# Состояния чата
states = {}
date_pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')

# student
task_id = None
teacher_id = None
task = None

@bot.message_handler(commands=['test'])
def test_command(message):
    get_homework_by_task_id(1)

@bot.message_handler(commands=['addHomeWork'])
def add_home_work(message):
    global states, group, title, description, startDL, stopDL, file_task_bytes, file_name, file_task

    user_tg_id = message.from_user.id
    # user = get_user_tg_id(user_tg_id)
    # user_id = user.id
    # user_group_id = user.group_id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    print(teacher_id,
          task)
    if teacher_id is None: # +
        teacher_list = get_all_teacher()
        for name in teacher_list:
            button_text = f"{name.get('id')}: {name.get('name')}"
            markup.add(types.KeyboardButton(button_text))
        bot.send_message(message.chat.id,
                         text="Выберите Вашего преподавателя из списка".format(message.from_user),
                         reply_markup=markup)
        states[message.chat.id] = "get_teacher"
    elif task is None:
        get_task_from_user(2, 1)
        print(get_task_from_user)
    elif group is None:
        groups = get_unique_groups()
        for name in groups:
            button_text = name.get('name')
            markup.add(types.KeyboardButton(button_text))
        bot.send_message(message.chat.id,
                         text="Выберите из списка группу или введите сами".format(message.from_user),
                         reply_markup=markup)
        states[message.chat.id] = "group"
    elif title is None:
        bot.send_message(message.chat.id, 'Напишите заголовок для задания')
        states[message.chat.id] = "title"
    elif description is None:
        bot.send_message(message.chat.id, 'Напишите описание для задания')
        states[message.chat.id] = "description"
    elif startDL is None:
        bot.send_message(message.chat.id, 'Напишите начальный срок для задания в формате ДД-ММ-ГГГГ')
        states[message.chat.id] = "startDL"
    elif stopDL is None:
        bot.send_message(message.chat.id, 'Напишите конечный срок для задания в формате ДД-ММ-ГГГГ')
        states[message.chat.id] = "stopDL"
    elif file_task is None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Вы хотите отправить файл?", reply_markup=markup)

        states[message.chat.id] = "file_task"

    if file_task is not None and stopDL is not None and startDL is not None and title is not None and group is not None:
        add_task(
            user_tg_id,
            group,
            title,
            description,
            startDL,
            stopDL,
            file_task_bytes,
            file_name
        )
        bot.send_message(message.chat.id, text="Домашнее задание добавлена", reply_markup=markup)
        group = None
        title = None
        description = None
        startDL = None
        stopDL = None
        file_task_bytes = []
        file_name = None
        file_task = None


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "get_teacher", content_types=['text'])
def input_group(message):
    global teacher_id
    teacher_id = message.text.split(':')[0].strip()
    add_home_work(message)


@bot.message_handler(commands=['createHomeWork'])
def create_home_work(message):
    global states, group, title, description, startDL, stopDL, file_task_bytes, file_name, file_task
    # Make sure 'states' is defined somewhere in your code

    user_tg_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if not is_user_teacher(user_tg_id):
        bot.send_message(message.chat.id,
                         'У Вас нет прав для этой функции. Запросите добавление Вашего аккаунта у деканата!')
        start(message)
        return

    if group is None:
        groups = get_unique_groups()
        for name in groups:
            button_text = name.get('name')
            markup.add(types.KeyboardButton(button_text))
        bot.send_message(message.chat.id,
                         text="Выберите из списка группу или введите сами".format(message.from_user),
                         reply_markup=markup)
        states[message.chat.id] = "group"
    elif title is None:
        bot.send_message(message.chat.id, 'Напишите заголовок для задания')
        states[message.chat.id] = "title"
    elif description is None:
        bot.send_message(message.chat.id, 'Напишите описание для задания')
        states[message.chat.id] = "description"
    elif startDL is None:
        bot.send_message(message.chat.id, 'Напишите начальный срок для задания в формате ДД-ММ-ГГГГ')
        states[message.chat.id] = "startDL"
    elif stopDL is None:
        bot.send_message(message.chat.id, 'Напишите конечный срок для задания в формате ДД-ММ-ГГГГ')
        states[message.chat.id] = "stopDL"
    elif file_task is None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Вы хотите отправить файл?", reply_markup=markup)

        states[message.chat.id] = "file_task"

    if file_task is not None and stopDL is not None and startDL is not None and title is not None and group is not None:
        user_id = get_user_tg_id(user_tg_id)
        add_task(
            user_tg_id,
            group,
            title,
            description,
            startDL,
            stopDL,
            file_task_bytes,
            file_name,
            user_id
        )
        bot.send_message(message.chat.id, text="Домашнее задание добавлена", reply_markup=markup)
        group = None
        title = None
        description = None
        startDL = None
        stopDL = None
        file_task_bytes = []
        file_name = None
        file_task = None


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "file_task", content_types=['text'])
def check_file(message):
    global file_task
    if message.text.lower() == "да":
        bot.send_message(message.chat.id, text="Прикрепите файл")
        states[message.chat.id] = "file_task"
    else:
        states[message.chat.id] = None
        file_task = "-"
        create_home_work(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "file_task", content_types=['document'])
def handle_document(message):
    global file_task_bytes, file_name, file_task
    file_info = bot.get_file(message.document.file_id)
    file_task_bytes = bot.download_file(file_info.file_path)
    file_name = message.document.file_name
    file_task = "-"
    create_home_work(message)
def input_group(message):
    global stopDL, states
    stopDL = message.text.lower()
    if check_date_format(stopDL):
        bot.send_message(message.chat.id, text="Дата добавлена")
        states[message.chat.id] = None
        create_home_work(message)
    else:
        # ошибку можно прокинуть свою
        bot.send_message(message.chat.id, 'Дата написана в неверном формате')


def check_date_format(date_string):
    return bool(date_pattern.match(date_string))


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "startDL", content_types=['text'])
def input_group(message):
    global startDL, states
    startDL = message.text.lower()
    if check_date_format(startDL):
        bot.send_message(message.chat.id, text="Дата добавлена")
        states[message.chat.id] = None
        create_home_work(message)
    else:
        # ошибку можно прокинуть свою
        bot.send_message(message.chat.id, 'Дата написана в неверном формате')


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "title", content_types=['text'])
def input_group(message):
    global title, states
    title = message.text.lower()
    if title is not None and title.strip() != "":
        bot.send_message(message.chat.id, text="Заголовок добавлен")
        states[message.chat.id] = None
        create_home_work(message)
    else:
        # ошибку можно прокинуть свою
        bot.send_message(message.chat.id, 'Строка пустая или добавлена')


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "description", content_types=['text'])
def input_group(message):
    global description, states
    description = message.text.lower()
    if description is not None and description.strip() != "":
        bot.send_message(message.chat.id, text="Описание добавлен")
        states[message.chat.id] = None
        create_home_work(message)
    else:
        # ошибку можно прокинуть свою
        bot.send_message(message.chat.id, 'Строка пустая или добавлена')


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "group", content_types=['text'])
def input_group(message):
    global group, states
    groups = get_unique_groups()
    group = message.text.lower()
    if any(group in x['name'] for x in groups):
        bot.send_message(message.chat.id, f'Выбрана группа: {group}')
        # Завершаем состояние
        states[message.chat.id] = None
        create_home_work(message)
    else:
        bot.send_message(message.chat.id, 'Такой группы не существует. Введите повторно')


# Начало работы
@bot.message_handler(commands=['start'])
def start(message):
    # Инициализация кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("➕ Добавить заявку")
    btn2 = types.KeyboardButton("❓ Информация о боте")
    btn3 = types.KeyboardButton("Команды")
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id,
                     text="Вас приветствует бот для ".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global block
    global cab
    global closing
    global issue_msg_id

    # Добавление заявки
    if message.text == "➕ Добавить заявку":

        # bot.delete_message(message.chat.id, message.id-2)
        # bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        # bot.edit_message_text("заявка должна быть не менее 10 символов", message.chat.id, message.id-2)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btns = []

        for e in blocks:
            btns.append(types.KeyboardButton(e))
        btns.append(types.KeyboardButton("Назад"))

        markup.add(*btns)

        bot.send_message(message.chat.id, text="Выберите блок", reply_markup=markup)

    # информация о боте
    elif message.text == "❓ Информация о боте":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Назад")
        markup.add(back)
        bot.send_message(message.chat.id, text="Данный бот создан, чтобы помочь преподавателям "
                                               "принимать домашние задания студентов",
                         reply_markup=markup)  # информация о боте
    elif message.text == "Команды":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Назад")
        markup.add(back)
        bot.send_message(message.chat.id,
                         text="Если вы преподаватель подайте заявку на добавление вашего Telegrem аккаунта в базу данных. "
                              "Тогда вы сможете добавлять домашние задания через бота с помощью команды /createHomeWork \n"
                              "Для студентов доступно: \n"
                              "/addHomeWork Прикрепить домашнее задание \n"
                              "/checkInfHomeWork Просмотр информации по предмету \n"
                              "/checkCurrentDeadline Просмотр актуальных дедлайнов", reply_markup=markup)


    # Обработка блоков
    # -----------------------------------------------------
    elif message.text == "А":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "Б":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "В":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "Г":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "Д":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "И":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "К":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)
    # -----------------------------------------------------

    # кнопка назад
    elif message.text == "Назад":

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("➕ Добавить заявку")
        button2 = types.KeyboardButton("❓ Информация о боте")
        markup.add(button1, button2)
        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, text="Главное меню", reply_markup=markup)

    # ----------------------------------------------------------------------------

    else:

        if block == '_' and cab == '_':

            # Закрытие заявки
            if closing:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = types.KeyboardButton("➕ Добавить заявку")
                button2 = types.KeyboardButton("❓ Информация о боте")
                markup.add(button1, button2)

                # bot.send_message(message.chat.id,
                #                  text=f"☑Заявка {issue_msg_id} закрыта\nРешение: {message.text}".format(
                #                      message.from_user), reply_markup=markup)

                # content = db.getContent(issue_msg_id)

                # id_experiment = db.getBotAcceptId(issue_msg_id)

                # bot.edit_message_text(
                #     f"☑️заявка #{issue_msg_id} закрыта - {message.from_user.username}\n--{content}--\nРешение:{message.text}",
                #       message.chat.id, id_experiment)
                #
                # bot.edit_message_text(
                #     f"☑️заявка #{issue_msg_id} закрыта - {message.from_user.username}\n--{content}--\nРешение:{message.text}",
                #       channel_id, issue_msg_id)

                closing = False

                bot.delete_message(message.chat.id, message.id - 1)
                bot.delete_message(message.chat.id, message.id)

                # db.closeApplications(issue_msg_id, message.from_user.id, message.text)

                issue_msg_id = issue_msg_id.replace(issue_msg_id, "_")


            # Обработка неизвестных команд
            else:
                bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")

        # Создание новой заявки
        elif block != '_' and cab == '_':

            # Ввод номера кабинета
            bot.delete_message(message.chat.id, message.id - 1)
            bot.delete_message(message.chat.id, message.id)

            # Проверка номера кабинета
            if message.text.isdigit():
                cab = cab.replace(cab, message.text)
                bot.send_message(message.chat.id, text="Опишите проблему")
            else:
                bot.send_message(message.chat.id,
                                 f"Не правильный формат номера кабинета кабинета, должны содержаться только числа")
        else:
            # Ввод описания проблемы
            bot.delete_message(message.chat.id, message.id - 1)
            bot.delete_message(message.chat.id, message.id)

            # Возвращение к изначальному меню
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("➕ Добавить заявку")
            button2 = types.KeyboardButton("❓ Информация о боте")
            markup.add(button1, button2)

            # Формирование кабинета
            room = block + cab

            # Отправка в чат АСУ
            # ---------------------------------------
            markup2 = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton(text="Принять", callback_data="accept")
            markup2.add(btn1)
            issuer_msg_id = bot.send_message(channel_id,
                                             'Н',
                                             reply_markup=markup2).id

            bot.edit_message_text(
                f'⚠️Новая заявка #{issuer_msg_id}\nАвтор:{message.from_user.username}\nСодержание:{message.text}',
                channel_id,
                issuer_msg_id, reply_markup=markup2)
            # ---------------------------------

            bot.send_message(message.chat.id, f"заявка #{issuer_msg_id} добавлена", reply_markup=markup)

            # db.createNewIssue(channel_id, message.chat.id, message.id, issuer_msg_id, room, message.text)

            cab = cab.replace(cab, "_")
            block = block.replace(block, "_")


@bot.callback_query_handler(func=lambda callback: callback.data == 'accept')
def accept_ticket(callback):
    content = callback.message.text.split("Содержание:")[1]

    bot.edit_message_text(
        f"🟨заявка #{callback.message.id} в работе - {callback.from_user.username}\nСодержание: {content}",
        channel_id, callback.message.id)

    markup2 = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Закрыть", callback_data=f"close-{callback.message.id}")
    markup2.add(btn1)

    id = bot.send_message(chat_id=callback.from_user.id,
                          text=f"🟨 Вы приняли заявку #{callback.message.id}\nСодержание: {content}",
                          reply_markup=markup2).id

    # bot.forward_message(callback.from_user.id, channel_id, callback.message.id)

    # db.acceptIssue(callback.message.id, callback.from_user.id, id)
    # type_answer = callback.data.split("@")[0].split(":")[1]

    # answers = {
    #     "accept": "Принимай трейд",
    #     "not_enough_cases": "Мало кейсов"
    # }
    # text = answers[type_answer]
    # bot.send_message(chat_id=callback.from_user.id, text="Это сообщение должен был написать бот тому, кто принял")


@bot.callback_query_handler(func=lambda callback: 'close' in callback.data)
def closingIssueHandler(callback):
    global issue_msg_id
    global closing
    global id_experiment

    issue_msg_id = issue_msg_id.replace(issue_msg_id, callback.data.split("-")[1])

    print(issue_msg_id)

    closing = True
    # a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(chat_id=callback.from_user.id, text="Напишите решение")
    return


def start_bot():
    # bot.polling(none_stop=True)
    print('start')
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    print('stop')

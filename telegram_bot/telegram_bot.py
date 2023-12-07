import telebot
from telebot import types
from config import *
from teamsClone.view_web.views import *
from teamsClone.views import *
import re
from io import BytesIO

bot = telebot.TeleBot(TOKEN_BOT)

# teacher
group = None  # обязательно
title = None  # обязательно
description = None  # обязательно
startDL = None  # обязательно
stopDL = None  # обязательно
file_task_bytes = []  # не обязательно
file_name = None  # не обязательно
file_task = None
# Состояния чата
states = {}
date_pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')

# student
user_id = None
group_id = None
task_id = None
teacher_id = None
teacher_name = None
task = None
time_delivery = None
subject = None

# create_student
user_name = None
login = None
password = None
group_name = None
subject_name = None
teacher_name = None


@bot.message_handler(commands=['getSentHomeworkAssignments'])
def get_sent_homework_assignments(message):
    user_tg_id = message.from_user.id
    user = get_user_by_tg_id(user_tg_id)
    homework_list = Homework.objects.filter(student=user)
    result_string = ""
    for homework in homework_list:
        result_string += f"Заголовок: {homework.title}\n"
        result_string += f"Описание: {homework.description}\n"
        result_string += f"Задание: {homework.task.title}\n"  # Предполагается, что задание также имеет поле 'title'
        result_string += f"Время сдачи: {homework.time_delivery}\n"

        result_string += f"Преподаватель: {homework.task.teacher.name}\n"  # Предполагается, что модель Task имеет поле 'teacher'
        result_string += f"Предмет: {homework.task.subject.name}\n"  # Предполагается, что модель Task имеет поле 'subject'

        result_string += f"Задание: {homework.task.title}\n"
        result_string += f"Время сдачи: {homework.time_delivery}\n"
        result_string += "\n"

        bot.send_message(message.chat.id, text=result_string)
        if homework.file_name is not None:
            file_byte_io = BytesIO(homework.file_byte)
            file_byte_io.name = homework.file_name
            bot.send_document(message.chat.id, file_byte_io)


@bot.message_handler(commands=['getVerifiedHomeworks'])
def get_verified_homeworks(message):
    user_tg_id = message.from_user.id
    user = get_user_by_tg_id(user_tg_id)
    verified_homeworks = get_verified_homeworks_by_user(user)
    result_verified = ""
    for homework in verified_homeworks:
        # Формируем строку с описанием принятых задач
        result_verified += f"ID: {homework.id}\n"
        result_verified += f"Студент: {homework.student.name}\n"
        result_verified += f"Заголовок: {homework.title}\n"
        result_verified += f"Описание: {homework.description}\n"
        result_verified += f"Задание: {homework.task.title}\n"
        result_verified += f"Файл: {homework.file_name}\n"
        result_verified += f"Проверено: Да\n" if homework.is_verified else "Проверено: Нет\n"
        result_verified += f"Срок сдачи: {homework.time_delivery}\n"
        result_verified += "\n"

        bot.send_message(message.chat.id, text=result_verified)
        if homework.file_name is not None:
            file_byte_io = BytesIO(homework.file_byte)
            file_byte_io.name = homework.file_name
            bot.send_document(message.chat.id, file_byte_io)


@bot.message_handler(commands=['getUnverifiedHomeworks'])
def get_unverified_homeworks(message):
    user_tg_id = message.from_user.id
    user = get_user_by_tg_id(user_tg_id)
    unverified_homeworks = get_unverified_homeworks_by_user(user)
    result_unverified = ""
    for homework in unverified_homeworks:
        # Формируем строку с описанием принятых задач
        result_unverified += f"ID: {homework.id}\n"
        result_unverified += f"Студент: {homework.student.name}\n"
        result_unverified += f"Заголовок: {homework.title}\n"
        result_unverified += f"Описание: {homework.description}\n"
        result_unverified += f"Задание: {homework.task.title}\n"
        result_unverified += f"Файл: {homework.file_name}\n"
        result_unverified += f"Проверено: Да\n" if homework.is_verified else "Проверено: Нет\n"
        result_unverified += f"Срок сдачи: {homework.time_delivery}\n"
        result_unverified += "\n"

        bot.send_message(message.chat.id, text=result_unverified)
        if homework.file_name is not None:
            file_byte_io = BytesIO(homework.file_byte)
            file_byte_io.name = homework.file_name
            bot.send_document(message.chat.id, file_byte_io)


@bot.message_handler(commands=['createUser'])
def create_student(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    if user_name is None:
        bot.send_message(message.chat.id, 'Введите Ваше имя.')
        states[message.chat.id] = "get_name"
    elif login is None:
        bot.send_message(message.chat.id, 'Введите Ваш login.')
        states[message.chat.id] = "get_login"
    elif password is None:
        bot.send_message(message.chat.id, 'Введите Ваш password.')
        states[message.chat.id] = "get_password"
    elif group_name is None:
        bot.send_message(message.chat.id, 'Введите Ваш group_name.')
        states[message.chat.id] = "get_group_name"
    elif subject_name is None:
        bot.send_message(message.chat.id, 'Введите Ваш subject_name.')
        states[message.chat.id] = "get_subject_name"
    elif teacher_name is None:
        bot.send_message(message.chat.id, 'Введите ФИО Вашего преподавателя')
        states[message.chat.id] = "get_teacher_name"

    if (user_name is not None and login is not None and password is not None and group_name is not None
        and subject_name) is not None and teacher_name is not None:
        user = create_user_with_checks(
            user_name,
            login,
            password,
            message.from_user.id,
            False,
            group_name,
            subject_name
        )
        if user:
            bot.send_message(message.chat.id, 'Пользователь создан.')
            states[message.chat.id] = None
            start(message)

        else:
            bot.send_message(message.chat.id, 'Ошибка при создании пользователя.')
            create_student(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "get_name", content_types=['text'])
def get_name(message):
    global user_name
    user_name = message.text
    states[message.chat.id] = None
    create_student(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "get_login", content_types=['text'])
def get_login(message):
    global login
    login = message.text
    states[message.chat.id] = None
    create_student(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "get_password", content_types=['text'])
def get_name(message):
    global password
    password = message.text
    states[message.chat.id] = None
    create_student(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "get_group_name", content_types=['text'])
def get_name(message):
    global group_name
    group_name = message.text
    if not group_exists(group_name):
        bot.send_message(message.chat.id, 'Такая группа не существует!')
    else:
        states[message.chat.id] = None
        create_student(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "get_subject_name", content_types=['text'])
def get_name(message):
    global subject_name
    subject_name = message.text
    if not subject_exists(subject_name):
        bot.send_message(message.chat.id, 'Такого предмета не существует!')
    else:
        states[message.chat.id] = None
        create_student(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "get_teacher_name", content_types=['text'])
def get_teacher_name(message):
    global teacher_name
    teacher_name = message.text
    if not subject_exists(teacher_name):
        bot.send_message(message.chat.id, 'Такого предмета не существует!')
    else:
        states[message.chat.id] = None
        create_student(message)


@bot.message_handler(commands=['checkCurrentDeadline'])
def check_actual_homework(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    user_tg_id = message.from_user.id
    # user = get_user_by_tg_id(user_tg_id)
    task_list = get_actual_tasks_for_group(get_group_id_by_telegram_id(user_tg_id))
    if task_list:
        bot.send_message(message.chat.id, text="Актуальные задания:".format(message.from_user), reply_markup=markup)
        for task_content in task_list:
            name_subject = get_subject(task_content.subject_id)

            message_text = (
                f"ID: {task_content.id} \n"
                f"Заголовок: {task_content.title}\n"
                f"Описание: {task_content.description}\n"
                f"Преподаватель: {teacher_name}\n"
                f"Название предмета: {name_subject}"
            )
            bot.send_message(message.chat.id, text=message_text.format(message.from_user), reply_markup=markup)
            if task_content.file_name is not None:
                file_byte_io = BytesIO(task_content.file_byte)
                file_byte_io.name = task_content.file_name
                bot.send_document(message.chat.id, file_byte_io)
    else:
        bot.send_message(message.chat.id, text="У Вас нет актуальных заданий:".format(message.from_user),
                         reply_markup=markup)


@bot.message_handler(commands=['addHomeWork'])
def add_homework(message):
    global states, group, title, description, startDL, stopDL, file_task_bytes, file_name, file_task, \
        time_delivery, task_id, teacher_id, teacher_name, task, time_delivery

    user_tg_id = message.from_user.id
    user = get_user_by_tg_id(user_tg_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if teacher_id is None:
        teacher_list = get_all_teacher()
        for name in teacher_list:
            button_text = f"{name.get('id')}: {name.get('name')}"
            markup.add(types.KeyboardButton(button_text))
        bot.send_message(message.chat.id,
                         text="Выберите Вашего преподавателя из списка".format(message.from_user),
                         reply_markup=markup)
        states[message.chat.id] = "get_teacher"
    elif task is None:
        markup = types.ReplyKeyboardRemove(selective=False)
        task_list = get_task_from_user(user.id, user.group_id, teacher_id)
        for task_content in task_list:
            name_subject = get_subject(task_content.subject_id)

            message_text = (f"ID: {task_content.id} \n"
                            f"Заголовок: {task_content.title}\n"
                            f"Описание: {task_content.description}\n"
                            f"Преподаватель: {teacher_name}\n"
                            f"Название предмета: {name_subject}")
            bot.send_message(message.chat.id,
                             text=message_text.format(message.from_user),
                             reply_markup=markup)
            if not task_content.file_name is None:
                file_byte_io = BytesIO(task_content.file_byte)
                file_byte_io.name = task_content.file_name

                bot.send_document(message.chat.id, file_byte_io)
        bot.send_message(message.chat.id,
                         text="Напишите ID задания, которые собираетесь сдать?".format(message.from_user),
                         reply_markup=markup)
        states[message.chat.id] = "get_task"
        # print(get_task_from_user)
    elif title is None:
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, 'Напишите заголовок для задания')
        states[message.chat.id] = "title_homework"
    elif description is None:
        bot.send_message(message.chat.id, 'Напишите описание для задания')
        states[message.chat.id] = "description_homework"
    elif file_task is None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Вы хотите отправить файл?", reply_markup=markup)

        states[message.chat.id] = "file_task_homework"
    if (file_task is not None and teacher_id is not None and task is not None and title is not None
            and description is not None and file_task is not None):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        add_homework_in_db(
            user,
            title,
            description,
            task_id,
            file_name,
            file_task_bytes
        )
        bot.send_message(message.chat.id, text="Домашнее задание добавлено", reply_markup=markup)
        title = None
        description = None
        file_task_bytes = []
        file_name = None
        file_task = None
        task_id = None
        teacher_id = None
        teacher_name = None
        task = None
        time_delivery = None

        states[message.chat.id] = None
        start(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "get_task", content_types=['text'])
def input_task(message):
    global task_id, task
    try:
        task_id = int(message.text)
        task = get_task_by_id(task_id)
        if task is None:
            bot.send_message(message.chat.id, 'Неверно введенный id задания')
        else:
            states[message.chat.id] = None
            task = "-"
            add_homework(message)
    except ValueError:
        bot.send_message(message.chat.id, 'Неверно введенный id задания. Пожалуйста, введите целое число.')


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "get_teacher", content_types=['text'])
def input_group(message):
    global teacher_id, teacher_name
    teacher_id = message.text.split(':')[0].strip()
    teacher_name = message.text.split(': ')[1].strip()
    add_homework(message)


@bot.message_handler(commands=['createHomeWork'])
def create_home_work(message):
    global states, group, title, description, startDL, stopDL, file_task_bytes, file_name, file_task, user_id, group_id
    # Make sure 'states' is defined somewhere in your code
    user_tg_id = message.from_user.id
    user_id = get_user_tg_id(user_tg_id)
    if not is_user_teacher(user_tg_id):
        bot.send_message(message.chat.id,
                         'У Вас нет прав для этой функции.')
        start(message)
        return

    if group is None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        groups = get_unique_groups()
        for name in groups:
            button_text = name.get('name')
            markup.add(types.KeyboardButton(button_text))
        bot.send_message(message.chat.id,
                         text="Выберите из списка группу или введите сами".format(message.from_user),
                         reply_markup=markup)
        states[message.chat.id] = "group"
    elif subject is None:
        group_id = get_group_id_by_name(group)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        subjects = get_subjects_by_teacher_and_group(user_id, group_id)

        for name in subjects:
            button_text = name.name
            markup.add(types.KeyboardButton(button_text))
        bot.send_message(message.chat.id,
                         text="Выберите из списка Ваш предмет".format(message.from_user),
                         reply_markup=markup)
        states[message.chat.id] = "subject"
    elif title is None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'Напишите заголовок для задания', reply_markup=markup)
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        add_task(
            user_id,
            group,
            title,
            description,
            startDL,
            stopDL,
            file_task_bytes,
            file_name,
            user_id,
            subject
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
        states[message.chat.id] = None


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "file_task", content_types=['text'])
def check_file(message):
    global file_task
    if message.text.lower() == "да":
        bot.send_message(message.chat.id, text="Прикрепите zip файл")
        states[message.chat.id] = "file_task"
    else:
        states[message.chat.id] = None
        file_task = "-"
        create_home_work(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "file_task_homework", content_types=['text'])
def check_file(message):
    global file_task
    if message.text.lower() == "да":
        bot.send_message(message.chat.id, text="Прикрепите zip файл")
        states[message.chat.id] = "file_task_homework"
    else:
        states[message.chat.id] = None
        file_task = "-"
        add_homework(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "file_task", content_types=['document'])
def handle_document(message):
    global file_task_bytes, file_name, file_task
    file_info = bot.get_file(message.document.file_id)
    file_task_bytes = bot.download_file(file_info.file_path)
    file_name = message.document.file_name
    file_task = "-"
    create_home_work(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "file_task_homework",
                     content_types=['document'])
def handle_document(message):
    global file_task_bytes, file_name, file_task
    file_info = bot.get_file(message.document.file_id)
    file_task_bytes = bot.download_file(file_info.file_path)
    file_name = message.document.file_name
    file_task = "-"
    add_homework(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "stopDL", content_types=['text'])
def input_group(message):
    global stopDL, states
    stopDL = message.text.lower()
    if check_date_format(stopDL):
        bot.send_message(message.chat.id, text=f"Дата окончания дедлайна {stopDL} добавлена")
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
        bot.send_message(message.chat.id, text=f"Дата начала дедлайна {startDL} добавлена")
        states[message.chat.id] = None
        create_home_work(message)
    else:
        # ошибку можно прокинуть свою
        bot.send_message(message.chat.id, 'Дата написана в неверном формате')


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "title_homework", content_types=['text'])
def input_group(message):
    global title, states
    title = message.text.lower()
    if title is not None and title.strip() != "":
        bot.send_message(message.chat.id, text="Заголовок добавлен")
        states[message.chat.id] = None
        add_homework(message)
    else:
        # ошибку можно прокинуть свою
        bot.send_message(message.chat.id, 'Строка пустая или добавлена')


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


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "description_homework", content_types=['text'])
def input_group(message):
    global description, states
    description = message.text.lower()
    if description is not None and description.strip() != "":
        bot.send_message(message.chat.id, text="Описание добавлен")
        states[message.chat.id] = None
        add_homework(message)
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


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "subject", content_types=['text'])
def input_group(message):
    global subject, states
    subjects = get_subjects_by_teacher_and_group(user_id, group_id)
    subject = message.text
    print(subject)
    if any(subject in x.name for x in subjects):
        bot.send_message(message.chat.id, f'Выбран предмет: {subject}')
        # Завершаем состояние
        states[message.chat.id] = None
        create_home_work(message)
    else:
        bot.send_message(message.chat.id, 'Такого предмета не существует. Введите повторно')


# Начало работы
@bot.message_handler(commands=['start'])
def start(message):
    # Инициализация кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton("❓ Информация о боте")
    btn3 = types.KeyboardButton("Команды")
    markup.add(btn2, btn3)

    bot.send_message(message.chat.id,
                     text="Вас приветствует бот помощник по сдаче и добавлению домашних заданий".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    # Добавление заявки

    if message.text == "❓ Информация о боте":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Назад")
        markup.add(back)
        bot.send_message(message.chat.id, text="Данный бот создан, чтобы помочь преподавателям "
                                               "принимать домашние задания студентов",
                         reply_markup=markup)  # информация о боте
    elif message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton("❓ Информация о боте")
        btn3 = types.KeyboardButton("Команды")
        markup.add(btn2, btn3)

        bot.send_message(message.chat.id,
                         text="Вас приветствует бот помощник по сдаче и добавлению домашних заданий".format(
                             message.from_user), reply_markup=markup)
    elif message.text == "Команды":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Назад")
        markup.add(back)
        bot.send_message(message.chat.id,
                         text="Если вы преподаватель подайте заявку на добавление вашего Telegrem аккаунта в базу данных."
                              "Тогда вы сможете добавлять домашние задания через бота с помощью команды \n"
                              "/createHomeWork \n"
                              "Для студентов доступно: \n"
                              "/addHomeWork Прикрепить домашнее задание \n"
                              "/checkCurrentDeadline Просмотр информации по предмету \n"
                              "/createUser Просмотр актуальных дедлайнов \n"
                              "/getUnverifiedHomeworks Просмотр  не принятых заданий \n"
                              "/getVerifiedHomeworks Просмотр принятых заданий \n"
                              "/createUser Создать студента"
                         , reply_markup=markup)


def start_bot():
    # bot.polling(none_stop=True)
    print('start')
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    print('stop')

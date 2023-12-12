from datetime import datetime

from django.db.models import Q
from django.utils import timezone

from .models import Subject, Task, Users, Group, GroupTask, Homework, SubjectGroup, SubjectTeacher
from .serializers import UsersSerializer, SubjectSerializer, \
    GroupNameSerializer


# READ


def get_unique_groups():
    unique_groups = Group.objects.values('name').distinct()
    serialize_unique_groups = GroupNameSerializer(unique_groups, many=True).data
    return serialize_unique_groups


from django.db import connection


def get_groups_by_teacher_and_subject(teacher_id, subject_id):
    groups = Group.objects.filter(
        subjectgroup__teacher_id=teacher_id,
        subjectgroup__subject_id=subject_id
    ).distinct()

    return groups


def get_teacher_studing_groups(teacher_name):
    teacher_name = "amir"
    # Создайте запрос и извлеките SQL-запрос и параметры
    query = Group.objects.filter(
        subjectgroup__teacher__name=teacher_name
    ).distinct()
    sql, params = query.query.sql_with_params()

    print(sql, params)

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        result = cursor.fetchall()

    print(result)
    return query


def get_task_by_id(task_id):
    try:
        task = Task.objects.get(id=task_id)
        return task
    except Task.DoesNotExist:
        return None


def is_user_teacher(telegram_id):
    try:
        user = Users.objects.get(telegram_id=telegram_id)
        return user.is_teacher
    except Users.DoesNotExist:
        return False


def get_user_tg_id(telegram_id):
    try:
        user = Users.objects.get(telegram_id=telegram_id)
        return user.id
    except Users.DoesNotExist:
        return None


def get_user_id(telegram_id):
    try:
        user = Users.objects.get(telegram_id=telegram_id)
        return user.id
    except Users.DoesNotExist:
        return None


def get_user_name(user_id):
    try:
        user = Users.objects.get(id=user_id)
        return user.name
    except Users.DoesNotExist:
        return None


def get_user_id_by_name(user_name):
    try:
        user = Users.objects.get(name=user_name)
        return user.id
    except Users.DoesNotExist:
        return None


def get_subject_id_by_teacher_and_group(teacher_id, group_id):
    try:
        subject_id = SubjectTeacher.objects.filter(
            teacher__id=teacher_id,
            teacher__is_teacher=True,
            teacher__group__id=group_id
        ).values('subject__id').first()['subject__id']

        return subject_id
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_user_by_tg_id(telegram_id):
    try:
        user = Users.objects.get(telegram_id=telegram_id)
        return user
    except Users.DoesNotExist:
        return None


def get_group_id_by_telegram_id(telegram_id):
    try:
        user = Users.objects.get(telegram_id=telegram_id)
        return user.group_id
    except Users.DoesNotExist:
        return None


def get_actual_tasks_for_group(group_id):
    current_date = date.today()

    actual_tasks = Task.objects.filter(
        Q(grouptask__group_id=group_id) &
        (Q(grouptask__start_deadline__lte=current_date) & Q(grouptask__stop_deadline__gte=current_date))
    ).distinct()

    print("Query:", actual_tasks.query)  # Вывести сформированный SQL-запрос для отладки

    for task in actual_tasks:
        print(f"Task ID: {task.id}, Title: {task.title}, Description: {task.description}")

    return actual_tasks


def get_is_verified_homeworks_by_user(user, is_verified):
    return Homework.objects.filter(student=user, is_verified=is_verified)


def get_group_by_name(group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group
    except Group.DoesNotExist:
        return None


def get_all_teacher():
    try:
        teacher_list = Users.objects.filter(is_teacher=True)
        serialize_teacher = UsersSerializer(teacher_list, many=True).data
        return serialize_teacher
    except Users.DoesNotExist:
        return None


def get_subject(subject_id):
    try:
        subject = Subject.objects.filter(id=subject_id)
        serialize_subject = SubjectSerializer(subject, many=True).data
        return serialize_subject
    except Subject.DoesNotExist:
        return None


def get_task_from_user(student_id, group_id, teacher_id):
    try:
        current_datetime = timezone.now()
        group_tasks = GroupTask.objects.filter(group_id=group_id)
        task_list = []

        for group_task in group_tasks:
            task_id = group_task.task_id
            task_content = Task.objects.filter(id=task_id, teacher_id=teacher_id).first()

            if task_content:
                stop_deadline_date_str = str(group_task.stop_deadline)
                stop_deadline_date = datetime.strptime(stop_deadline_date_str, "%Y-%m-%d").date()
                stop_deadline_datetime = timezone.make_aware(datetime.combine(stop_deadline_date, datetime.min.time()))

                if current_datetime < stop_deadline_datetime:
                    task_list.append(task_content)

        return task_list
    except Task.DoesNotExist:
        return None


from datetime import date


def get_actual_tasks_for_group(group_id):
    # Получаем текущую дату
    current_date = date.today()

    # Ищем задания, у которых срок сдачи еще не наступил
    # и задания, у которых срок сдачи еще не прошел
    actual_tasks = Task.objects.filter(
        Q(grouptask__group_id=group_id) &
        (Q(grouptask__start_deadline__lte=current_date) & Q(grouptask__stop_deadline__gte=current_date))
    ).distinct()

    return actual_tasks


def get_subjects_by_teacher(teacher_id):
    subjects = Subject.objects.filter(subjectteacher__teacher_id=teacher_id).distinct()
    return subjects


def get_subjects_by_teacher_and_group(teacher_id, group_id):
    # Получаем предметы, связанные с преподавателем
    teacher_subjects = SubjectTeacher.objects.filter(teacher__id=teacher_id).values_list('subject_id', flat=True)

    # Получаем предметы, связанные с группой
    group_subjects = SubjectGroup.objects.filter(group__id=group_id).values_list('subject_id', flat=True)

    # Получаем общий список предметов для преподавателя и группы
    subjects_ids = set(teacher_subjects) & set(group_subjects)

    # Получаем объекты предметов по их идентификаторам
    subjects = Subject.objects.filter(id__in=subjects_ids)

    return subjects


def add_task(user_tg_id, group, title, description, startDL, stopDL, file_task_bytes, file_name, user_id, subject):
    # Задаем фиксированную дату
    start = datetime.strptime(startDL, "%d-%m-%Y").date()
    stop = datetime.strptime(stopDL, "%d-%m-%Y").date()

    existing_group = Group.objects.get(name=group)
    existing_subject = Subject.objects.get(name=subject)
    # Create a new task instance

    new_task = Task(
        title=title,
        description=description,
        file_name=file_name,
        file_byte=bytes(file_task_bytes),
        teacher_id=user_id,
        subject_id=existing_subject.id
    )

    new_task.save()

    new_group_task = GroupTask(
        task=new_task,
        group=existing_group,
        start_deadline=start,  # Replace with the actual start deadline
        stop_deadline=stop  # Replace with the actual stop deadline
    )

    new_group_task.save()


def add_homework_in_db(student, title, description, task_id, file_name, file_byte):
    try:
        GroupTask.objects.get(task_id=task_id)
    except GroupTask.DoesNotExist:
        raise ValueError("Задание не найдено в GroupTask")

    hm = None
    try:
        hm = Homework.objects.get(student_id=student.id, task_id=task_id)
    except:
        hm = None
    if hm:
        hm.title = title
        hm.description = description
        hm.file_name = file_name
        hm.file_byte = file_byte
        hm.is_verified = None
        hm.time_delivery = datetime.now().date()
        hm.save()
    else:
        print(file_name)
        print(file_byte)
        homework = Homework.objects.create(
            student_id=student.id,
            title=title,
            description=description,
            task_id=task_id,
            file_name=file_name,
            file_byte=file_byte,
            is_verified=None,
            time_delivery=datetime.now().date()
        )


from django.core.exceptions import ObjectDoesNotExist


def create_user_with_checks(name, login, password, telegram_id, is_teacher, group_name, subject_name, teacher_name):
    try:
        # Проверка существования группы
        group = Group.objects.get(name=group_name)

        # Проверка существования пользователя (преподавателя)
        teacher = Users.objects.get(name=teacher_name, is_teacher=True)

        # Проверка существования предмета
        subject = Subject.objects.get(name=subject_name)

        # Создание пользователя
        user = Users.objects.create(
            name=name,
            login=login,
            password=password,
            telegram_id=telegram_id,
            is_teacher=is_teacher,
            group=group
        )

        # Если пользователь - студент, связываем его с предметом
        if not is_teacher:
            SubjectGroup.objects.create(
                group=group,
                subject=subject,
                url_online_education=None  # Здесь вы можете указать ссылку на онлайн-обучение, если это необходимо
            )

        return user

    except ObjectDoesNotExist as e:
        print(f"Error: {e}")
        return None


def group_exists(group_name):
    try:
        Group.objects.get(name=group_name)
        return True
    except ObjectDoesNotExist:
        return False


def subject_exists(subject_name):
    try:
        Subject.objects.get(name=subject_name)
        return True
    except ObjectDoesNotExist:
        return False


def get_subject_id_by_name(subject_name):
    try:
        subject = Subject.objects.get(name=subject_name)
        return subject
    except ObjectDoesNotExist:
        return None


def check_teacher_subject_group(teacher_name, subject_id, group_id):
    # Проверка существования преподавателя с указанным именем
    teacher_exists = Users.objects.filter(name=teacher_name, is_teacher=True).exists()

    if teacher_exists:
        # Проверка, что преподаватель ведет указанный предмет для данной группы
        teacher_id = Users.objects.get(name=teacher_name, is_teacher=True).id
        subject_teacher_exists = SubjectTeacher.objects.filter(
            teacher_id=teacher_id, subject_id=subject_id).exists()

        if subject_teacher_exists:
            # Проверка, что группа связана с указанным предметом
            group_subject_exists = SubjectGroup.objects.filter(
                group_id=group_id, subject_id=subject_id).exists()

            return group_subject_exists

    return None


def teacher_exists_for_subject(teacher_name, teacher_login, subject_name):
    try:
        teacher = Users.objects.get(name=teacher_name, login=teacher_login, is_teacher=True)
        subject = Subject.objects.get(name=subject_name)
        SubjectTeacher.objects.get(teacher=teacher, subject=subject)
        return True
    except ObjectDoesNotExist:
        return False


def get_teacher_id_by_name_and_subject(teacher_name, subject_name):
    try:
        teacher_id = SubjectTeacher.objects.filter(
            teacher__name=teacher_name,
            subject__name=subject_name
        ).values_list('teacher__id', flat=True).first()

        if teacher_id:
            return teacher_id
        else:
            print(f"Teacher '{teacher_name}' for subject '{subject_name}' not found.")
            return None

    except ObjectDoesNotExist as e:
        print(f"Error: {e}")
        return None


def get_group_id_by_name(group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group.id
    except Subject.DoesNotExist:
        return None

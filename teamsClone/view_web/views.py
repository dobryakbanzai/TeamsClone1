from django.http import JsonResponse

from ..models import Subject, Task, Users, Group, GroupTask, SubjectTeacher, SubjectGroup, Homework
from ..serializers import UsersSerializer, SubjectSerializer, \
    TaskSerializer, GroupNameSerializer, HomeworkSerializer
from django.db.models import Q, Count
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404


# SERIALIZERS
def serialize_users(users):
    serializer = UsersSerializer(users, many=True)
    return serializer.data


def serialize_subject(subject):
    serializer = SubjectSerializer(subject)
    return serializer.data


def serialize_task(task):
    serializer = TaskSerializer(task)
    return serializer.data

def add_teacher(name, login, password, telegram_id, point, group_id):
    # Проверка на существование пользователя с аналогичным логином и паролем
    if Users.objects.filter(login=login, password=password).exists():
        return {'success': False, 'message': 'Пользователь с таким логином и паролем уже существует.'}

    # Создание нового пользователя
    new_teacher = Users(
        name=name,
        login=login,
        password=password,
        telegram_id=telegram_id,
        is_teacher=True,
        group=Group.objects.get(pk=group_id) if group_id else None
    )
    new_teacher.save()

    return {'success': True, 'message': 'Преподаватель успешно добавлен.'}

# 6 разбиваю его на несколько запросов
# 1. получение всех заданий по предмету и препода get_list_tasks_by_subject_id(subject_id,teacher_id)
# 2. получение всех домашек по определенному заданию get_homework_by_task_id(task_id)
# 3. изменение статуса(is_verified) дз True - принято,  False - не принято None - не проверено
#  update_homework_status(is_verified, homework_id)
def get_homework_by_task_id(task_id):
    # Получаем задачу по task_id
    task = Task.objects.get(id=task_id)

    # Получаем все домашние задания для данной задачи
    homework_list = Homework.objects.filter(task_id=task_id)

    homework_list_new = HomeworkSerializer(homework_list, many=True)
    # Создаем список для ответа
    homework_data = []
    for homework in homework_list:
        homework_data.append(homework)

    # Выводим данные о домашних заданиях в консоль для отладки
    print(homework_list_new.data)

    return homework_list


def update_homework_status(is_verified, homework_id):
    # Находим объект домашнего задания по ID
    homework = get_object_or_404(Homework, pk=homework_id)

    # Обновляем статус is_verified
    homework.is_verified = is_verified
    homework.save()


def get_list_tasks_by_subject_id(subject_id, teacher_id):
    # Получаем все задания для данного предмета и преподавателя
    tasks = Task.objects.filter(subject_id=subject_id, teacher_id=teacher_id)

    serializer = TaskSerializer(tasks, many=True)
    # tasks_list = []
    # for task in tasks:
    #     tasks_list.append(task)

    return serializer.data


def isTeacherRegistred(login, password):
    try:
        user = Users.objects.get(login=login)
        if user.password == password:
            return True, user
        else:
            return False, "InvalidPassword"
    except Users.DoesNotExist:
        return False, "InvalidLogin"


def getInformationByStudent(teacher_id, subject_id):
    info = {
        'subject_info': get_subject_info(teacher_id, subject_id),
        'student_in_course': get_student_in_course(subject_id, teacher_id),
        'sdannix_work': get_sdannix_work(subject_id, teacher_id)
    }
    return info


def get_subject_info(teacher_id, subject_id):
    # Получаем информацию о предмете (subject)
    subject_info = (
        Subject.objects
        .filter(id=subject_id)
        .values('id', 'name')
        .first()
    )

    if subject_info:
        # Получаем информацию о группах для данного предмета
        groups_info = (
            SubjectGroup.objects
            .filter(subject_id=subject_id)
            .values('group__name', 'url_online_education')
        )

        # Получаем информацию о преподавателях для данного предмета
        teachers_info = (
            SubjectTeacher.objects
            .filter(subject_id=subject_id, teacher_id=teacher_id)
            .values('teacher__name')
        )

        # Добавляем информацию о группах, преподавателях и URL в результат
        subject_info['groups'] = list(groups_info)
        subject_info['teachers'] = list(teachers_info)

    return subject_info


# варинант получения всей инфы о предмете
def get_all_student_from_course(subject_id):
    # Retrieve subject information along with related data
    subject_info = (
        Subject.objects.filter(id=subject_id)
        .values('id', 'name')
        .first()
    )

    if subject_info:
        # Retrieve distinct group names for the subject
        group_names = (
            SubjectGroup.objects
            .filter(subject_id=subject_id)
            .values('group__name')
            .distinct()
        )
        subject_info['group_names'] = [group['group__name'] for group in group_names]

        # Retrieve distinct teacher names for the subject
        teacher_names = (
            SubjectTeacher.objects
            .filter(subject_id=subject_id)
            .values('teacher__name')
            .distinct()
        )
        subject_info['teacher_names'] = [teacher['teacher__name'] for teacher in teacher_names]

        # Retrieve distinct URL online educations for the subject
        url_online_educations = (
            SubjectGroup.objects
            .filter(subject_id=subject_id)
            .values('url_online_education')
            .distinct()
        )
        subject_info['url_online_educations'] = [
            url['url_online_education'] for url in url_online_educations
        ]

    print(subject_info)


def get_student_in_course(subject_id, teacher_id):
    students_with_subject = Users.objects.filter(
        is_teacher=False,  # Выбираем только студентов, а не преподавателей
        group__subjectgroup__subject__subjectteacher__teacher_id=teacher_id,
        group__subjectgroup__subject_id=subject_id
    ).distinct()

    # for student in students_with_subject:
    #     print(student.name)
    return students_with_subject


def get_sdannix_work(subject_id, teacher_id):
    # Добавляем статус выполненных заданий к имени каждого студента
    students_with_subject = Users.objects.filter(
        is_teacher=False,
        group__subjectgroup__subject__subjectteacher__teacher_id=teacher_id,
        group__subjectgroup__subject_id=subject_id
    ).distinct().annotate(
        completed_tasks=Count('homework', filter=Q(homework__is_verified=True)),
        total_tasks=Count('homework')
    )

    # for student in students_with_subject:
    #     print(
    #         f"Студент: {student.name}, Завершено заданий: {student.completed_tasks}, Всего заданий: {student.total_tasks}")
    return students_with_subject


def get_all_courses(teacher_id):
    # Get the list of subjects taught by the teacher
    subjects_taught = SubjectTeacher.objects.filter(teacher_id=teacher_id).values_list('subject__name',
                                                                                       flat=True).distinct()

    # Get the list of groups that study under the teacher
    groups_studied = SubjectGroup.objects.filter(subject__subjectteacher__teacher_id=teacher_id).values_list(
        'group__name', flat=True).distinct()

    result = {
        'subjects': subjects_taught,
        'groups': groups_studied
    }

    return result

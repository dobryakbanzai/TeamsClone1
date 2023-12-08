from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from teamsClone.models import Users, Subject, Group, SubjectGroup, SubjectTeacher
from teamsClone.view_web import views as dbp


def sign_in(request, error=None):
    user = request.user
    if user.is_authenticated:
        logout(request)

    return render(request, "login.html", {'error': error})


def sign_up(request):
    return render(request, "registration.html")


def regist_view(request):
    username = request.POST['username']
    password = request.POST['password']
    flname = request.POST['flname']

    result_ad = dbp.add_teacher(name=flname, login=username, password=password, telegram_id=None, point=None,
                                group_id=None)

    if result_ad['success']:
        teach_reg = dbp.isTeacherRegistred(login=username, password=password)
        t_r = teach_reg[1]

        user = User.objects.create_user(last_name=t_r.id, first_name=flname, username=username, password=password)
        user.save()

    return redirect('firsterrorpage', error=result_ad['message'])


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # user = User.objects.create_user(username, "lennon@thebeatles.com", password)

        user1 = authenticate(request, username=username, password=password)
        # user.save()

        if user1 is not None:
            login(request, user1)
            # Пользователь успешно авторизован, перенаправьте его на защищенную страницу
            return redirect('mainpage')
        else:
            # Неверные данные логина или пароля, покажите ошибку
            return redirect('firsterrorpage', error="Invalid login")
    else:
        return redirect('firstpage', error=None)


@login_required
def all_groups(request):
    groups = dbp.get_all_courses(int(request.user.last_name))
    return render(request, "GroupView.html", {'groups': groups})


@csrf_exempt
def exit_from_sys(request):
    # Выполните необходимые операции при выходе
    # Например, вы можете очистить сессию или выполнить другие задачи по очистке
    # ...

    return redirect('/')  # Перенаправление на желаемую страницу после успешного выхода


@login_required
def stud_view(request):
    student = {"name": "Bob", "group": "09-951"}
    tasks = [
        {"id": 1, "name": "task1", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 2, "name": "task2", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 3, "name": "task3", "status": "completed", "file": {"url": "#"}, "submission_date": "12-12-2023"},
        {"id": 4, "name": "task4", "status": "not-completed", "file": {"url": "#"}, "submission_date": "12-12-2023"}
    ]

    return render(request, "StudentPage.html", {"student": student, "tasks": tasks})


@login_required
def group_page(request):
    group = {"id": 1, "num": "09-915", "subject": "Python и его библиотеки"}
    students = [
        {"id": 1, "name": "Biba", "taskcomplete": [
            {"num": 1, "status": True},
            {"num": 2, "status": False},
            {"num": 3, "status": True},
            {"num": 4, "status": True},
            {"num": 5, "status": True},
            {"num": 6, "status": True},
            {"num": 7, "status": True},
            {"num": 8, "status": False}
        ]},
        {"id": 2, "name": "Boba", "taskcomplete": [
            {"num": 1, "status": True},
            {"num": 2, "status": True},
            {"num": 3, "status": True},
            {"num": 4, "status": False}
        ]},
        {"id": 3, "name": "Zhizha", "taskcomplete": [
            {"num": 1, "status": True},
            {"num": 2, "status": False},
            {"num": 3, "status": False},
            {"num": 4, "status": False}
        ]}
    ]

    return render(request, "GroupPage.html", {'group': group, 'students': students})


@login_required
def addGroup(request):
    groups = Group.objects.all()
    subjects = Subject.objects.filter(subjectteacher__teacher__id=int(request.user.last_name))
    return render(request, "AddNewGroup.html", {'groups': groups, 'subjects': subjects})


@login_required
def addingGroup(request):
    url = request.POST['resource']
    group_id = request.POST['group']
    subject_id = request.POST['subject']
    teacher_id = int(request.user.last_name)

    if SubjectGroup.objects.filter(group_id=group_id, subject_id=subject_id, teacher_id=teacher_id).exists():
        return redirect('mainpage')

    sg = SubjectGroup(
        url_online_education=url,
        group_id=group_id,
        subject_id=subject_id,
        teacher_id=teacher_id
    )
    sg.save()
    return redirect('mainpage')


@login_required
def createNewSubject(request):
    return render(request, "CreateNewSubject.html")

@login_required
def creatingNewSubject(request):
    name = request.POST['subject']
    teacher_id = int(request.user.last_name)

    if Subject.objects.filter(name=name, subjectteacher__teacher__id=teacher_id).exists():
        return redirect('mainpage')

    ns = Subject(
        name=name
    )
    ns.save()
    nst = SubjectTeacher(
        subject_id=ns.id,
        teacher_id=teacher_id
    )
    nst.save()

    return redirect('mainpage')

@login_required
def addnewacademicgroup(request):
    return render(request, "AddNewAcademicGroup.html")


def addingnewacademicgroup(request):
    name = request.POST['group']

    if Group.objects.filter(name=name).exists():
        return redirect('mainpage')

    ng = Group(
        name=name
    )
    ng.save()

    return redirect('mainpage')
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from teamsClone.models import Users


def sign_in(request):
    return render(request, "login.html")


def sign_up(request):
    return render(request, "registration.html")


def all_groups(request):
    groups = [
        {"num": "09-915", "name": "Python и его библиотеки"},
        {"num": "09-925", "name": "ML - Алгоритмы"},
        {"num": "09-935", "name": "C ++"}
        # Добавьте остальные группы по аналогии
    ]
    return render(request, "GroupView.html", {'groups': groups})



@csrf_exempt
def exit_from_sys(request):
    # Выполните необходимые операции при выходе
    # Например, вы можете очистить сессию или выполнить другие задачи по очистке
    # ...

    return redirect('/')  # Перенаправление на желаемую страницу после успешного выхода


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

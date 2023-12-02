from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def sign_in(request):
    return render(request, "login.html")

def sign_up(request):
    return render(request, "registration.html")

def all_groups(request):
    groups = ['Группа 1', 'Группа 2', 'Группа 3', 'Залупа']
    return render(request, "GroupView.html", {'groups': groups})

@csrf_exempt
def exit_from_sys(request):
    # Выполните необходимые операции при выходе
    # Например, вы можете очистить сессию или выполнить другие задачи по очистке
    # ...

    return redirect('/')  # Перенаправление на желаемую страницу после успешного выхода
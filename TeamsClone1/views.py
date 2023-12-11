from django.contrib import messages
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from teamsClone.models import Users, Subject, Group, SubjectGroup, SubjectTeacher, Task, Homework, GroupTask
from teamsClone.view_web import views as dbp
import datetime
from django.http import HttpResponse
from io import BytesIO
import re


def is_latin_and_symbols(text):
    pattern = r'^[a-zA-Z\s\W]+$'
    result = re.match(pattern, text)
    return result is not None


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


        user1 = authenticate(request, username=username, password=password)


        if user1 is not None:
            login(request, user1)

            return redirect('mainpage')
        else:

            return redirect('firsterrorpage', error="Invalid login")
    else:
        return redirect('firstpage', error=None)


@login_required
def all_groups(request):
    groups = dbp.get_all_courses(int(request.user.last_name))
    return render(request, "GroupView.html", {'groups': groups})


@csrf_exempt
def exit_from_sys(request):

    return redirect('/')


@login_required
def stud_view(request, stud, subj):
    student = Users.objects.get(id=stud)
    group = Group.objects.get(id=student.group_id)
    subject = Subject.objects.get(id=subj)

    tasks = Task.objects.filter(teacher_id=int(request.user.last_name), subject_id=subject.id)
    taskAndHomework = []

    for task in tasks:
        try:
            homework = Homework.objects.get(student_id=stud, task_id=task.id)
        except:
            homework = None
        try:
            gt = GroupTask.objects.get(task_id=task.id, group_id=group.id)
        except:
            gt = None
        taskAndHomework.append({'task': task, 'homework': homework, 'gt': gt})

    return render(request, "StudentPage.html",
                  {"student": student, "tasks": taskAndHomework, 'group': group, 'subject': subject})


@login_required
def refresh_homework_status(request):
    group = request.POST['group']
    stud_id = request.POST['stud']
    subject = request.POST['subject']
    homework_ids = request.POST.getlist('homework_id')
    is_verified_values = request.POST.getlist('is_verified')

    print(homework_ids, is_verified_values)

    for homework_id, is_verified in zip(homework_ids, is_verified_values):

        if homework_id != '':
            homework = Homework.objects.get(id=int(homework_id))
            if is_verified == 'True':
                homework.is_verified = True
            else:
                homework.is_verified = False
            homework.save()

    return redirect('grouppage', group=group, subject=subject)


@login_required
def group_page(request, group, subject):
    groupO = Group.objects.get(id=group)

    subjectO = Subject.objects.get(id=subject)

    students = Users.objects.filter(group_id=group, is_teacher=False)

    tasks = Task.objects.filter(subject_id=subjectO.id, teacher_id=int(request.user.last_name),
                                grouptask__group_id=groupO.id)

    studAndTasks = []

    for student in students:
        studTaskPack = []
        i = 1
        for task in tasks:
            try:
                hw = Homework.objects.get(task_id=task.id, student_id=student.id)
            except:
                hw = None
            status = ""

            if hw is None:
                deadline = GroupTask.objects.get(group_id=groupO.id, task_id=task.id).stop_deadline
                if deadline < datetime.date.today():
                    status = "R"
                else:
                    status = "G"
            else:
                deadline = GroupTask.objects.get(group_id=groupO.id, task_id=task.id).stop_deadline
                if hw.is_verified:
                    if deadline < hw.time_delivery:
                        status = "P"
                    else:
                        status = "Z"
                else:
                    if deadline < hw.time_delivery:
                        status = "O"
                    else:
                        status = "Y"

            studTaskPack.append({'num': i, 'status': status})
            i += 1
        studAndTasks.append({'student': student, 'taskcomplete': studTaskPack})



    return render(request, "GroupPage.html", {'group': groupO, 'subject': subjectO, 'students': studAndTasks})


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


@login_required
def addingnewacademicgroup(request):
    name = request.POST['group']

    if Group.objects.filter(name=name).exists():
        return redirect('mainpage')

    ng = Group(
        name=name
    )
    ng.save()

    return redirect('mainpage')


@login_required
def allGroupTask(request, group, subject):
    tasks = Task.objects.filter(subject_id=subject, teacher_id=int(request.user.last_name),
                                grouptask__group_id=group)

    return render(request, "AllGroupTasks.html", {'group': group, 'subject': subject, 'tasks': tasks})


def createNewTask(request, group, subject):
    return render(request, "CreateNewTask.html",
                  {'group': group, 'subject': subject, 'teacher': int(request.user.last_name)})


def creatingNewTask(request):
    title = request.POST['title']
    description = request.POST['description']
    file = request.FILES['file']
    group = request.POST['group']
    subject = request.POST['subject']
    teacher = request.POST['teacher']
    start = request.POST['s1d']
    dead = request.POST['s2d']
    file_name = file.name
    file_data = file.read()

    if not is_latin_and_symbols(file_name):
        messages.warning(request, 'Предупреждение: необходимо избегать использования кириллицы в названиях файлов.')
        return redirect('alltask', group=group, subject=subject)

    task = Task(
        title=title,
        description=description,
        file_name=file_name,
        file_byte=file_data,
        teacher_id=teacher,
        subject_id=subject
    )
    task.save()

    gt = GroupTask(
        group_id=group,
        task_id=task.id,
        start_deadline=start,
        stop_deadline=dead
    )

    gt.save()

    return redirect('alltask', group=group, subject=subject)


def downloadfile(request, taskid):
    ts = Task.objects.get(id=taskid)

    response = HttpResponse(ts.file_byte, content_type='application/')
    response['Content-Disposition'] = f'inline; filename=' + ts.file_name

    return response


def downloadhwfile(request, hwid):
    hw = Homework.objects.get(id=hwid)

    response = HttpResponse(hw.file_byte, content_type='application/zip')
    response['Content-Disposition'] = f'inline; filename=' + hw.file_name

    return response

from .models import Subject, Task, Users, Group, GroupTask
from .serializers import UsersSerializer, SubjectSerializer, \
    TaskSerializer, GroupNameSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Q

from datetime import datetime, time


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


# CREATE
@api_view(['POST'])
def create_user_serialized(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        user = Users.objects.create(**serializer.validated_data)
        serialized_user = UsersSerializer(user).data
        return Response(serialized_user, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_subject_serialized(request):
    serializer = SubjectSerializer(data=request.data)
    if serializer.is_valid():
        subject = Subject.objects.create(**serializer.validated_data)
        serialized_subject = SubjectSerializer(subject).data
        return Response(serialized_subject, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_task_serialized(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        task = Task.objects.create(**serializer.validated_data)
        serialized_task = TaskSerializer(task).data
        return Response(serialized_task, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# READ
@api_view(['GET'])
def get_all_users_serialized(request):
    users = Users.objects.all()
    serialized_users = UsersSerializer(users, many=True).data
    return Response({'users': serialized_users})


def get_unique_groups():
    unique_groups = Group.objects.values('name').distinct()
    serialize_unique_groups = GroupNameSerializer(unique_groups, many=True).data
    return serialize_unique_groups


@api_view(['GET'])
def get_all_subjects_serialized(request):
    subjects = Subject.objects.all()
    serialized_subjects = SubjectSerializer(subjects, many=True).data
    return Response({'subjects': serialized_subjects})


@api_view(['GET'])
def get_all_tasks_serialized(request):
    tasks = Task.objects.all()
    serialized_tasks = TaskSerializer(tasks, many=True).data
    return Response({'tasks': serialized_tasks})


# ... (Repeat the same pattern for other read functions)

# UPDATE
@api_view(['PUT'])
def update_user_serialized(request, user_id):
    user = get_user_by_id(user_id)
    if not user:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UsersSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        updated_user = get_user_by_id(user_id)
        serialized_user = UsersSerializer(updated_user).data
        return Response(serialized_user, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_subject_serialized(request, subject_id):
    subject = get_subject_by_id(subject_id)
    if not subject:
        return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = SubjectSerializer(instance=subject, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        updated_subject = get_subject_by_id(subject_id)
        serialized_subject = SubjectSerializer(updated_subject).data
        return Response(serialized_subject, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_task_serialized(request, task_id):
    task = get_task_by_id(task_id)
    if not task:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(instance=task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        updated_task = get_task_by_id(task_id)
        serialized_task = TaskSerializer(updated_task).data
        return Response(serialized_task, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ... (Repeat the same pattern for other update functions)

# DELETE
@api_view(['DELETE'])
def delete_user_serialized(request, user_id):
    user = get_user_by_id(user_id)
    if not user:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    deleted_user = user
    user.delete()
    serialized_user = UsersSerializer(deleted_user).data
    return Response(serialized_user, status=status.HTTP_204_NO_CONTENT)


# GET BY ID
@api_view(['GET'])
def get_user_by_id_serialized(request, user_id):
    user = get_user_by_id(user_id)
    if not user:
        return JsonResponse({'error': 'Us   er not found'}, status=404)
    serializer = UsersSerializer(user)
    return JsonResponse(serializer.data)


def get_user_by_id(user_id):
    try:
        user = Users.objects.get(id=user_id)
        return user
    except Users.DoesNotExist:
        return None


@api_view(['GET'])
def get_subject_by_id_serialized(request, subject_id):
    subject = get_subject_by_id(subject_id)
    if not subject:
        return JsonResponse({'error': 'Subject not found'}, status=404)
    serialized_subject = SubjectSerializer(subject).data
    return JsonResponse(serialized_subject)


def get_subject_by_id(subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
        return subject
    except Subject.DoesNotExist:
        return None


@api_view(['GET'])
def get_task_by_id_serialized(request, task_id):
    task = get_task_by_id(task_id)
    if not task:
        return JsonResponse({'error': 'Task not found'}, status=404)
    serialized_task = TaskSerializer(task).data
    return JsonResponse(serialized_task)


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


def get_task_from_user(student_id, group_id):
    try:
        group_tasks = GroupTask.objects.filter(group_id=group_id)
        task_list = []

        # Получаем содержимое в таблице Task по каждому task_id
        for group_task in group_tasks:
            task_id = group_task.task_id
            task_content = Task.objects.get(id=task_id)
            task_list.append(task_content)
            print(f"Task ID: {task_content.id}, Title: {task_content.title}, Description: {task_content.description}")

        return task_list
    except Task.DoesNotExist:
        return None

def add_task(user_tg_id, group, title, description, startDL, stopDL, file_task_bytes, file_name, user_id):
    # Задаем фиксированную дату
    startDL = datetime.strptime(startDL, "%d-%m-%Y")
    stopDL = datetime.strptime(stopDL, "%d-%m-%Y")

    # Получаем текущее время
    current_time = datetime.now().time()

    # Создаем новый объект datetime с фиксированной датой и текущим временем
    combined_startDL = datetime.combine(startDL.date(), current_time)
    combined_stopDL = datetime.combine(stopDL.date(), current_time)

    # Извлекаем время из объединенного объекта datetime
    start_deadline = combined_startDL.time()
    stop_deadline = combined_stopDL.time()
    existing_group = Group.objects.get(name=group)
    # Create a new task instance

    new_task = Task(
        title=title,
        description=description,
        file_name=file_name,
        file_byte=bytes(file_task_bytes),
        teacher_id=user_id
    )

    new_task.save()

    new_group_task = GroupTask(
        task=new_task,
        group=existing_group,
        start_deadline=start_deadline,  # Replace with the actual start deadline
        stop_deadline=stop_deadline  # Replace with the actual stop deadline
    )

    new_group_task.save()
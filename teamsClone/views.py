from .models import InformationSubject, Subject, Task, File, Users
from .serializers import UsersSerializer, InformationSubjectSerializer, SubjectSerializer, FileSerializer, \
    TaskSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import connection


# SERIALIZERS
def serialize_users(users):
    serializer = UsersSerializer(users, many=True)
    return serializer.data


def serialize_information_subject(info_subject):
    serializer = InformationSubjectSerializer(info_subject)
    return serializer.data


def serialize_subject(subject):
    serializer = SubjectSerializer(subject)
    return serializer.data


def serialize_file(file_obj):
    serializer = FileSerializer(file_obj)
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
def create_information_subject_serialized(request):
    serializer = InformationSubjectSerializer(data=request.data)
    if serializer.is_valid():
        info_subject = InformationSubject.objects.create(**serializer.validated_data)
        serialized_info_subject = InformationSubjectSerializer(info_subject).data
        return Response(serialized_info_subject, status=status.HTTP_201_CREATED)
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
def create_file_serialized(request):
    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
        file_obj = File.objects.create(**serializer.validated_data)
        serialized_file = FileSerializer(file_obj).data
        return Response(serialized_file, status=status.HTTP_201_CREATED)
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


@api_view(['GET'])
def get_all_information_subjects_serialized(request):
    info_subjects = InformationSubject.objects.all()
    serialized_info_subjects = InformationSubjectSerializer(info_subjects, many=True).data
    return Response({'information_subjects': serialized_info_subjects})


@api_view(['GET'])
def get_all_subjects_serialized(request):
    subjects = Subject.objects.all()
    serialized_subjects = SubjectSerializer(subjects, many=True).data
    return Response({'subjects': serialized_subjects})


@api_view(['GET'])
def get_all_files_serialized(request):
    files = File.objects.all()
    serialized_files = FileSerializer(files, many=True).data
    return Response({'files': serialized_files})


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
def update_information_subject_serialized(request, info_subject_id):
    info_subject = get_information_subject_by_id(info_subject_id)
    if not info_subject:
        return Response({'error': 'InformationSubject not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = InformationSubjectSerializer(instance=info_subject, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        updated_info_subject = get_information_subject_by_id(info_subject_id)
        serialized_info_subject = InformationSubjectSerializer(updated_info_subject).data
        return Response(serialized_info_subject, status=status.HTTP_200_OK)
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
def update_file_serialized(request, file_id):
    file_obj = get_file_by_id(file_id)
    if not file_obj:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = FileSerializer(instance=file_obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        updated_file = get_file_by_id(file_id)
        serialized_file = FileSerializer(updated_file).data
        return Response(serialized_file, status=status.HTTP_200_OK)
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


@api_view(['DELETE'])
def delete_information_subject_serialized(request, info_subject_id):
    info_subject = get_information_subject_by_id(info_subject_id)
    if not info_subject:
        return Response({'error': 'InformationSubject not found'}, status=status.HTTP_404_NOT_FOUND)

    deleted_info_subject = info_subject
    info_subject.delete()
    serialized_info_subject = InformationSubjectSerializer(deleted_info_subject).data
    return Response


@api_view(['DELETE'])
def delete_subject_serialized(request, info_subject_id):
    info_subject = get_information_subject_by_id(info_subject_id)
    if not info_subject:
        return Response({'error': 'InformationSubject not found'}, status=status.HTTP_404_NOT_FOUND)

    deleted_info_subject = info_subject
    info_subject.delete()
    serialized_info_subject = InformationSubjectSerializer(deleted_info_subject).data
    return Response


@api_view(['DELETE'])
def delete_file_serialized(request, file_id):
    file = get_information_subject_by_id(file_id)
    if not file:
        return Response({'error': 'InformationSubject not found'}, status=status.HTTP_404_NOT_FOUND)

    deleted_file = file
    file.delete()
    serialized_file = InformationSubjectSerializer(deleted_file).data
    return Response


@api_view(['DELETE'])
def delete_task_serialized(request, info_subject_id):
    info_subject = get_information_subject_by_id(info_subject_id)
    if not info_subject:
        return Response({'error': 'InformationSubject not found'}, status=status.HTTP_404_NOT_FOUND)

    deleted_info_subject = info_subject
    info_subject.delete()
    serialized_info_subject = InformationSubjectSerializer(deleted_info_subject).data
    return Response


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
def get_information_subject_by_id_serialized(request, info_subject_id):
    info_subject = get_information_subject_by_id(info_subject_id)
    if not info_subject:
        return JsonResponse({'error': 'InformationSubject not found'}, status=404)
    serialized_info_subject = InformationSubjectSerializer(info_subject).data
    return JsonResponse(serialized_info_subject)


def get_information_subject_by_id(info_subject_id):
    try:
        info_subject = InformationSubject.objects.get(id=info_subject_id)
        return info_subject
    except InformationSubject.DoesNotExist:
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
# GET BY ID
def get_file_by_id_serialized(request, file_id):
    file_obj = get_file_by_id(file_id)
    if not file_obj:
        return JsonResponse({'error': 'File not found'}, status=404)
    serialized_file = FileSerializer(file_obj).data
    return JsonResponse(serialized_file)


def get_file_by_id(file_id):
    try:
        file_obj = File.objects.get(id=file_id)
        return file_obj
    except File.DoesNotExist:
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

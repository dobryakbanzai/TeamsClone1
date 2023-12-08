from django.test import TestCase
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from teamsClone.models import Subject, Task, Users, Group, GroupTask, SubjectTeacher, SubjectGroup, Homework
from teamsClone.serializers import UsersSerializer, SubjectSerializer, TaskSerializer, GroupNameSerializer, HomeworkSerializer
from django.db.models import Q, Count
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404

from teamsClone.view_web.views import *


class MyTests(TestCase):
    def setUp(self):
        # Set up any initial data needed for the tests
        pass

    def test_add_teacher(self):
        response = add_teacher(name="John Doe", login="john.doe", password="password", telegram_id="123", point="A", group_id=1)
        self.assertEqual(response['success'], True)

    def test_get_homework_by_task_id(self):
        task = Task.objects.create(subject_id=1, teacher_id=1, description="Task description")
        homework = Homework.objects.create(task=task, user_id=1, content="Homework content")
        response = get_homework_by_task_id(task_id=task.id)
        self.assertEqual(response.count(), 1)

    def test_update_homework_status(self):
        task = Task.objects.create(subject_id=1, teacher_id=1, description="Task description")
        homework = Homework.objects.create(task=task, user_id=1, content="Homework content")
        update_homework_status(is_verified=True, homework_id=homework.id)
        updated_homework = Homework.objects.get(id=homework.id)
        self.assertEqual(updated_homework.is_verified, True)

    def test_get_list_tasks_by_subject_id(self):
        subject = Subject.objects.create(name="Test Subject")
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        task = Task.objects.create(subject=subject, teacher=teacher, description="Task description")
        response = get_list_tasks_by_subject_id(subject_id=subject.id, teacher_id=teacher.id)
        self.assertEqual(len(response), 1)

    def test_isTeacherRegistred(self):
        user = Users.objects.create(login="test_teacher", password=make_password("test_password"))
        response, user_info = isTeacherRegistred(login="test_teacher", password="test_password")
        self.assertEqual(response, True)
        self.assertEqual(user_info, user)

    def test_getInformationByStudent(self):
        subject = Subject.objects.create(name="Test Subject")
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        info = getInformationByStudent(teacher_id=teacher.id, subject_id=subject.id)
        self.assertEqual("subject_info" in info, True)
        self.assertEqual("student_in_course" in info, True)
        self.assertEqual("sdannix_work" in info, True)

    def test_get_all_student_from_course(self):
        subject = Subject.objects.create(name="Test Subject")
        get_all_student_from_course(subject_id=subject.id)  # This is a print statement, manually check the output

    def test_get_student_in_course(self):
        subject = Subject.objects.create(name="Test Subject")
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        students = get_student_in_course(subject_id=subject.id, teacher_id=teacher.id)
        self.assertEqual(students.exists(), False)  # Assuming no students exist for simplicity

    def test_get_sdannix_work(self):
        subject = Subject.objects.create(name="Test Subject")
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        get_sdannix_work(subject_id=subject.id, teacher_id=teacher.id)  # This is a print statement, manually check the output

    def test_get_all_courses(self):
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        response = get_all_courses(teacher_id=teacher.id)
        self.assertEqual("subjects" in response, True)
        self.assertEqual("groups" in response, True)
# myapp/tests.py

from django.test import TestCase
from django.contrib.auth.hashers import make_password

from teamsClone.view_web.views import *


class MyTests(TestCase):
    subject = None

    def setUp(self):
        global subject
        Group.objects.create(name="Тестовая группа")
        user = Users.objects.create(name="John Doe", login="john.doe", password="password", is_teacher=False)
        task = Task.objects.create(title="Test Task", description="Task description", teacher=user)
        subject = Subject.objects.create(id=1, name="Your Subject Name")
        homework = Homework.objects.create(student=user, title="Homework Title", description="Homework description",
                                           task=task, is_verified=False, time_delivery="2023-12-31")

    def test_add_student(self):
        response = add_teacher(name="John Doe", login="john.doe", password="password", telegram_id="123", point="A",
                               group_id=1)
        self.assertEqual(response['success'], False)

    def test_get_homework_by_task_id(self):
        task = Task.objects.create(subject_id=1, teacher_id=1, description="Task description")
        user = Users.objects.create(id=1, name="John Doe", login="john.doe", password="password", is_teacher=True)

        homework = Homework.objects.create(student=user, title="Homework Title", description="Homework description",
                                           task=task, is_verified=False, time_delivery="2023-12-31")
        response = get_homework_by_task_id(task_id=task.id)
        self.assertEqual(response.count(), 1)

    def test_update_homework_status(self):
        teacher_user = Users.objects.create(name="Teacher Name", login="teacher", password="password", is_teacher=True)
        task = Task.objects.create(subject_id=1, teacher_id=teacher_user.id, description="Task description")
        student_user = Users.objects.create(name="John Doe", login="john.doe", password="password", is_teacher=False)
        homework = Homework.objects.create(task=task, student=student_user, title="Homework Title",
                                           description="Homework description", is_verified=False,
                                           time_delivery="2023-12-31")
        update_homework_status(is_verified=True, homework_id=homework.id)
        updated_homework = Homework.objects.get(id=homework.id)
        self.assertEqual(updated_homework.is_verified, True)

    def test_get_list_tasks_by_subject_id(self):
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        task = Task.objects.create(subject=subject, teacher=teacher, description="Task description")
        response = get_list_tasks_by_subject_id(subject_id=subject.id, teacher_id=teacher.id)
        self.assertEqual(len(response), 1)

    def test_isStudentRegistred_fail(self):
        user = Users.objects.create(login="test_teacher", password=make_password("test_password"), is_teacher=False)
        response, user_info = isTeacherRegistred(login="test_teacher", password="test_password")
        self.assertEqual(response, False)
        self.assertEqual(user_info, "InvalidPassword")

    def test_getInformationByStudent(self):
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        info = getInformationByStudent(teacher_id=teacher.id, subject_id=subject.id)
        self.assertEqual("subject_info" in info, True)
        self.assertEqual("student_in_course" in info, True)
        self.assertEqual("sdannix_work" in info, True)

    def test_get_all_student_from_course(self):
        get_all_student_from_course(subject_id=subject.id)  # This is a print statement, manually check the output

    def test_get_student_in_course(self):
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        students = get_student_in_course(subject_id=subject.id, teacher_id=teacher.id)
        self.assertEqual(students.exists(), False)  # Assuming no students exist for simplicity

    def test_get_sdannix_work(self):
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        get_sdannix_work(subject_id=subject.id,
                         teacher_id=teacher.id)  # This is a print statement, manually check the output

    def test_get_all_courses(self):
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        response = get_all_courses(teacher_id=teacher.id)
        self.assertEqual("subjects" in response, True)
        self.assertEqual("groups" in response, True)

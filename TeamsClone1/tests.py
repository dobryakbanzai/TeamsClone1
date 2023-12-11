from django.test import TestCase
from django.contrib.auth.hashers import make_password
from teamsClone.view_web.views import *

class MyTests(TestCase):
    def setUp(self):
        Group.objects.create(name="09-315")
        self.user = Users.objects.create(name="Василий Пупкин", login="login", password="password", is_teacher=False)
        self.task = Task.objects.create(title="Task title", description="Task description", teacher=self.user)
        self.subject = Subject.objects.create(id=1, name="Python")
        self.homework = Homework.objects.create(
            student=self.user,
            title="Homework Title",
            description="Homework description",
            task=self.task,
            is_verified=False,
            time_delivery="2023-12-31",
        )

    def test_add_student(self):
        response = add_teacher(name="Василий Пупкин", login="login", password="password", telegram_id="123", point="A", group_id=1)
        self.assertFalse(response['success'])

    def test_get_homework_by_task_id(self):
        response = get_homework_by_task_id(task_id=self.task.id)
        self.assertEqual(response.count(), 1)

    def test_update_homework_status(self):
        update_homework_status(is_verified=True, homework_id=self.homework.id)
        updated_homework = Homework.objects.get(id=self.homework.id)
        self.assertTrue(updated_homework.is_verified)

    def test_get_list_tasks_by_subject_id(self):
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        task = Task.objects.create(subject=self.subject, teacher=teacher, description="Task description")
        response = get_list_tasks_by_subject_id(subject_id=self.subject.id, teacher_id=teacher.id)
        self.assertEqual(len(response), 1)

    def test_isStudentRegistred_fail(self):
        user = Users.objects.create(login="test_teacher", password=make_password("test_password"), is_teacher=False)
        response, user_info = isTeacherRegistred(login="test_teacher", password="test_password")
        self.assertFalse(response)
        self.assertEqual(user_info, "InvalidPassword")

    def test_getInformationByStudent(self):
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        info = getInformationByStudent(teacher_id=teacher.id, subject_id=self.subject.id)
        self.assertIn("subject_info", info)
        self.assertIn("student_in_course", info)
        self.assertIn("sdannix_work", info)

    def test_get_all_student_from_course(self):
        get_all_student_from_course(subject_id=self.subject.id)

    def test_get_student_in_course(self):
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        students = get_student_in_course(subject_id=self.subject.id, teacher_id=teacher.id)
        self.assertFalse(students.exists())

    def test_get_sdannix_work(self):
        teacher = Users.objects.create(name="Teacher", is_teacher=True)
        get_sdannix_work(subject_id=self.subject.id, teacher_id=teacher.id)

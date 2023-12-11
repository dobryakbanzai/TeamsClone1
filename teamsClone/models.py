from django.db import models


# Create your models here.
# чтобы создать в бд таблицы в консоль вводим
# python manage.py makemigrations
# python manage.py migrate


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=255, null=True)
    is_teacher = models.BooleanField()
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True)


class Subject(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)


class SubjectGroup(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey('Users', on_delete=models.CASCADE, null=True)
    url_online_education = models.CharField(max_length=255, null=True)


class SubjectTeacher(models.Model):
    teacher = models.ForeignKey('Users', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=True)


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255, null=True)
    file_byte = models.BinaryField(null=True)
    teacher = models.ForeignKey('Users', on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=True)


class Homework(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey('Users', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True)
    file_name = models.CharField(max_length=255, null=True)
    file_byte = models.BinaryField(null=True)
    is_verified = models.BooleanField(null=True)
    time_delivery = models.DateField()


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)


class GroupTask(models.Model):
    id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True)
    start_deadline = models.DateField()
    stop_deadline = models.DateField()

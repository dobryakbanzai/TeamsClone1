from django.db import models


# Create your models here.
# чтобы создать в бд таблицы в консоль вводим
# python manage.py makemigrations
# python manage.py migrate
class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    point = models.IntegerField(null=True)
    is_teacher = models.BooleanField()


class InformationSubject(models.Model):
    id = models.BigAutoField(primary_key=True)
    teache_id = models.BigIntegerField()
    url_online_education = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}-{self.teache_id}"


class Subject(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    teacher_id = models.BigIntegerField()

    def __str__(self):
        return self.name


class File(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    file = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

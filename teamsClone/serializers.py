from rest_framework import serializers

from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class SubjectGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectGroup
        fields = '__all__'


class SubjectTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectTeacher
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class GroupTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupTask
        fields = '__all__'


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'file_name', 'file_byte', 'teacher', 'subject']
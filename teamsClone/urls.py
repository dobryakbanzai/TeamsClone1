"""
URL configuration for TeamsClone1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from teamsClone import views

urlpatterns = [
    # CREATE
    path('create_user/', views.create_user_serialized, name='create_user'),
    path('create_subject/', views.create_subject_serialized, name='create_subject'),
    path('create_task/', views.create_task_serialized, name='create_task'),

    # READ
    path('get_all_users/', views.get_all_users_serialized, name='get_all_users'),
    path('get_all_subjects/', views.get_all_subjects_serialized, name='get_all_subjects'),
    path('get_all_tasks/', views.get_all_tasks_serialized, name='get_all_tasks'),

    # UPDATE
    path('update_user/<int:user_id>/', views.update_user_serialized, name='update_user'),
    path('update_subject/<int:subject_id>/', views.update_subject_serialized, name='update_subject'),
    path('update_task/<int:task_id>/', views.update_task_serialized, name='update_task'),

    # DELETE
    path('delete_user/<int:user_id>/', views.delete_user_serialized, name='delete_user'),

    # GET BY ID
    path('get_user/<int:user_id>/', views.get_user_by_id_serialized, name='get_user_by_id'),
    path('get_subject/<int:subject_id>/', views.get_subject_by_id_serialized, name='get_subject_by_id'),
    path('get_task/<int:task_id>/', views.get_task_by_id_serialized, name='get_task_by_id'),
]


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
from django.urls import include, path
from . import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("restfuncs/", include("teamsClone.urls")),
    path("<str:error>", views.sign_in, name='firsterrorpage'),
    path("", views.sign_in, name='firstpage'),
    path("reg/", views.sign_up),
    path("mainpage/", views.all_groups, name='mainpage'),
    path('logout/', views.exit_from_sys, name='logout'),
    path("grouppage/<int:group>&<int:subject>", views.group_page, name='grouppage'),
    path("addnewgroup/", views.addGroup),
    path("addinggroup/", views.addingGroup, name='addinggroup'),
    path("createnewsubject/", views.createNewSubject),
    path("creatingnewsubject/", views.creatingNewSubject, name = 'creatingnewsubject'),
    path("addnewacademicgroup/", views.addnewacademicgroup),
    path("addingingnewacademicgroup/", views.addingnewacademicgroup, name = 'addingnewacademicgroup'),
    path("login/", views.login_view, name='login'),
    path("dreg/", views.regist_view, name='registrate'),
    path("stud/<int:stud>&<int:subj>", views.stud_view),
    path("alltask/<int:group>&<int:subject>", views.allGroupTask, name='alltask'),
    path("createnewtask/<int:group>&<int:subject>", views.createNewTask, name ='createnewtask'),
    path("creatingnewtask/", views.creatingNewTask, name='creatingnewtask'),
    path("download/<int:taskid>", views.downloadfile, name='download'),
    path("downloadhw/<int:hwid>", views.downloadhwfile, name='downloadhw'),
    path("refreshhw/", views.refresh_homework_status, name='refresh')
]

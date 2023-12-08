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
    path("grouppage/", views.group_page),
    path("addnewgroup/", views.addGroup),
    path("addinggroup/", views.addingGroup, name='addinggroup'),
    path("createnewsubject/", views.createNewSubject),
    path("creatingnewsubject/", views.creatingNewSubject, name = 'creatingnewsubject'),
    path("addnewacademicgroup/", views.addnewacademicgroup),
    path("addingingnewacademicgroup/", views.addingnewacademicgroup, name = 'addingnewacademicgroup'),
    path("login/", views.login_view, name='login'),
    path("dreg/", views.regist_view, name='registrate'),
    path("stud/", views.stud_view),

]

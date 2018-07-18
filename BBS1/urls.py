"""BBS1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('code/', views.code),
    path('index/',views.index,name='index'),
    path('logout/',views.logout,name='logout'),
    path('comment/',views.comment,name='comment'),
    path('',views.index),
    path('backend/', views.backend,name='backend'),
    path('backend/add_article/', views.add_article),
    path('upload/', views.upload,name='upload'),
    re_path('site/(?P<username>\w+)/',views.site,name='site'),
    re_path('(?P<username>\w+)/(?P<condition>category|tag|achrive)/(?P<params>.*)/',views.site),
    re_path('(?P<username>\w+)/artical/(?P<artical_id>\d+)',views.artical),
    path('digg/',views.digg,name='digg')


]

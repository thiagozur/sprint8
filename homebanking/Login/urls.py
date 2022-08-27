from django.contrib import admin
from django.urls import path
from . import views

app_name = 'Login'

urlpatterns = [
    path('', views.login, name='login'),
    path('newuser/', views.newuser, name='newuser'),
]


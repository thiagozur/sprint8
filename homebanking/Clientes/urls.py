from django.urls import path
from . import views

app_name = 'Cliente'

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('inversiones/', views.inversiones, name='inversiones'),
]

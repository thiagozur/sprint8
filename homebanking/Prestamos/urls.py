from django.urls import path
from . import views

app_name = 'Prestamos'

urlpatterns = [
    path('', views.prestamos, name='prestamos'),
    path('loanreq/<acc>', views.loanreq, name='loanreq'),
    path('loanend/', views.loanend, name='loanend'),
]
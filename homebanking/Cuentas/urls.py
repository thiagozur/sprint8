from django.urls import path
from . import views

app_name = 'Cuentas'

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('empty/', views.empty, name='empty'),
    path('emptynotlog/', views.emptynotlog, name='emptynotlog'),
    path('movimientos/<acc>', views.movimientos, name='movimientos'),
]

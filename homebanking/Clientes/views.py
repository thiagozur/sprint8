from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as dlogout
from .models import Cliente, TipoClientes
from Cuentas.models import Cuenta
from Tarjetas.models import Tarjetas
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/') 
def home(request):
    userobj = get_object_or_404(User, username=request.user)
    uname = userobj.first_name
    usurname = userobj.last_name
    ufullname = uname[0] + usurname
    uidt = userobj.username.split(ufullname)
    if len(uidt) == 2:
        uid = userobj.username.split(ufullname)[1]
    else:
        uid = userobj.id
    clientobj = Cliente.objects.get(customer_id = uid)
    cuentas = Cuenta.objects.filter(customer_id = clientobj.customer_id)
    tarjetas = Tarjetas.objects.filter(customerid = clientobj.customer_id)
    curtype = TipoClientes.objects.get(tipoid=clientobj.tipo).tipo
    return render(request, 'Clientes/home.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}', 'accounts' : cuentas, 'cards' : tarjetas, 'tipo' : curtype})

@login_required(login_url='/')
def logout(request):
    dlogout(request)
    return HttpResponseRedirect("/")

@login_required(login_url='/')
def inversiones(request):
    userobj = get_object_or_404(User, username=request.user)
    return render(request, 'Clientes/inversiones.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}'})
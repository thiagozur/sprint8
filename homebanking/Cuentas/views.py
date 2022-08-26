from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Cuenta, Movimientos
from Clientes.models import Cliente
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/')
def accounts(request):
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
    return render(request, 'Cuentas/accounts.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}', 'accounts' : cuentas})

@login_required(login_url='/')
def movimientos(request, acc):
    userobj = get_object_or_404(User, username=request.user)
    movimientos = Movimientos.objects.filter(account_id = acc)
    return render(request, 'Cuentas/movimientos.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}', 'mov' : movimientos})

@login_required(login_url='/')
def empty(request):
    userobj = get_object_or_404(User, username=request.user)
    return render(request, 'Cuentas/empty.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}'})

def emptynotlog(request):
    return render(request, 'Cuentas/emptynotlog.html')
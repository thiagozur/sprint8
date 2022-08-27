from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from Clientes.models import TipoClientes
from .models import Prestamo
from Clientes.models import Cliente
from django.contrib.auth.decorators import login_required
from .forms import LoanForm
from Cuentas.models import Cuenta
from datetime import datetime

# Create your views here.

@login_required(login_url='/')
def prestamos(request):
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
    prestamos = {}

    for i in cuentas:
        loanlist = Prestamo.objects.filter(account_id=i.account_id)
        prestamos[str(i)] = loanlist

    print(prestamos)
    return render(request, 'Prestamos/prestamos.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}', 'loans' : prestamos, 'accs' : cuentas})

@login_required(login_url='/')
def loanend(request):
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
    return render(request, 'Prestamos/loanend.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}', 'accounts' : cuentas})

@login_required(login_url='/')
def loanreq(request, acc):
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
    if request.method == 'POST':
        loanform = LoanForm(request.POST)
        if loanform.is_valid():
            nudata = loanform.cleaned_data
            try:
                commarem = nudata['fecha'][:-1]
                tdate = commarem.split('-')
                if len(tdate) != 3:
                    loanform = LoanForm()
                    loanform.fields['fecha'].widget.attrs['placeholder'] = 'Fecha inadecuada'
                    return render(request, 'Prestamos/loanreq.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}', 'loanform' : loanform})
                datetimeobj = datetime(int(tdate[0]), int(tdate[1]), int(tdate[2]))
                initdate = datetimeobj.strftime('%Y-%m-%d')
            except:
                loanform = LoanForm()
                loanform.fields['fecha'].widget.attrs['placeholder'] = 'Fecha inadecuada'
                return render(request, 'Prestamos/loanreq.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}', 'loanform' : loanform})
            curtype = TipoClientes.objects.get(tipoid=clientobj.tipo)
            curtype = curtype.tipo
            monto = int(nudata['monto']) * 100

            if curtype == 'Classic':
                limit = 10000000
            elif curtype == 'Gold':
                limit = 30000000
            elif curtype == 'Black':
                limit = 50000000

            displimit = f'${limit // 100}'

            if monto > limit:
                loanform = LoanForm()
                loanform.fields['monto'].widget.attrs['placeholder'] = f'Monto mayor a límite permitido ({displimit})' 
                return render(request, 'Prestamos/loanreq.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}', 'loanform' : loanform})
            else:
                curacc = Cuenta.objects.get(account_id=acc)
                curloan = Prestamo()
                curloan.loan_date = initdate
                curloan.loan_type = nudata['tipo']
                curloan.loan_total = monto
                curacc.balance += curloan.loan_total
                curloan.account_id = acc
                curloan.branch_id = clientobj.branch_id
                curacc.save()
                curloan.save()
                return render(request, 'Prestamos/success.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}'})
        else:
            loanform = LoanForm()
            for i in loanform.fields:
                loanform.fields[i].widget.attrs['placeholder'] = 'Datos inadecuados'
            return render(request, 'Prestamos/loanreq.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}', 'loanform' : loanform})
    else:
        loanform = LoanForm()
        return render(request, 'Prestamos/loanreq.html', {'name' : f'{userobj.first_name} {userobj.last_name[0]}', 'loanform' : loanform})
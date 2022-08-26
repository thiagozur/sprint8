from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import LoginForm, NewUserForm
from django.contrib.auth import authenticate, login as dlogin
from Clientes.models import Cliente, Empleado
from django.contrib.auth.models import User
from datetime import datetime
from random import randrange

# Create your views here.

def login(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                dlogin(request, user)
                url = request.GET.get('next')
                if url is not None:
                    return HttpResponseRedirect(url)
                else:
                    return HttpResponseRedirect('home/')
            else:
                loginform = LoginForm()
                loginform.fields['username'].widget.attrs['placeholder'] = 'Usuario o contraseña incorrectos'
                loginform.fields['password'].widget.attrs['placeholder'] = 'Usuario o contraseña incorrectos'
                return render(request, 'Login/login.html', {'loginform' : loginform})       
    else:
        loginform = LoginForm()
    return render(request, 'Login/login.html', {'loginform' : loginform})

def newuser(request):
    if request.method == 'POST':
        newuserform = NewUserForm(request.POST)
        if newuserform.is_valid():
            nudata = newuserform.cleaned_data
            try:
                commarem = nudata['dob'][:-1]
                tdate = commarem.split('-')
                if len(tdate) != 3:
                    newuserform = NewUserForm()
                    newuserform.fields['dob'].widget.attrs['placeholder'] = 'Fecha inadecuada'
                    return render(request, 'Login/newuser.html', {'newuserform' : newuserform})
                datetimeobj = datetime(int(tdate[0]), int(tdate[1]), int(tdate[2]))
                date = datetimeobj.strftime('%Y-%m-%d')
            except:
                newuserform = NewUserForm()
                newuserform.fields['dob'].widget.attrs['placeholder'] = 'Fecha inadecuada'
                return render(request, 'Login/newuser.html', {'newuserform' : newuserform})
            nuser = User.objects.create_user(username=nudata['username'], password=nudata['password'], email=nudata['email'], first_name=nudata['firstname'], last_name=nudata['lastname'])
            nuclient = Cliente(customer_id=nuser.id, customer_name=nuser.first_name, customer_surname=nuser.last_name, customer_dni=nudata['dni'], dob=date, branch_id=randrange(1, 100), tipo=randrange(1, 3))
            nuser.save()
            nuclient.save()
            dlogin(request, nuser)
            return HttpResponseRedirect('/home/')
        else:
            newuserform = NewUserForm()
            for i in newuserform.fields:
                newuserform.fields[i].widget.attrs['placeholder'] = 'Datos inadecuados'
            return render(request, 'Login/newuser.html', {'newuserform' : newuserform})
    else:
        newuserform = NewUserForm()
    return render(request, 'Login/newuser.html', {'newuserform' : newuserform})

#esta vista fue usada para crear los usuarios iniciales a partir de los clientes en la base de datos pero no es utilizada en el proyecto
def createclients(request):
    clients = Cliente.objects.all()
    for i in clients:
        nuser = User.objects.create_user(username = f'{i.customer_name[0]}{i.customer_surname}{i.customer_id}', password = i.customer_dni, email = f'{i.customer_name[0]}{i.customer_surname}@gmail.com', first_name = i.customer_name, last_name = i.customer_surname)
        nuser.save()
    return HttpResponse('<h1>Usuarios creados</h1>')

#esta vista fue usada para asignarle tipos de cliente a los clientes pero no es utilizada en el proyecto
def addtypes(request):
    clients = Cliente.objects.all()
    for i in clients:
        i.tipo = randrange(1, 4)
        i.save()
    return HttpResponse('<h1>Tipos añadidos</h1>')

def createmp(request):
    emps = Empleado.objects.all()
    for y, i in enumerate(emps):
        try:
            nuser = User.objects.create_user(
                username = f'{i.employee_name[0]}{i.employee_surname}{i.employee_id}',
                password = i.employee_dni,
                email = f'{i.employee_name[0]}{i.employee_surname}@gmail.com',
                first_name = i.employee_name,
                last_name = i.employee_surname
                )
            nuser.is_staff = True
            nuser.save()
        except:
            nuser = User.objects.create_user(
                username = f'{i.employee_name[0]}{i.employee_surname}{i.employee_id}{y}',
                password = i.employee_dni,
                email = f'{i.employee_name[0]}{i.employee_surname}@gmail.com',
                first_name = i.employee_name,
                last_name = i.employee_surname
                )
            nuser.is_staff = True
            nuser.save()


    return HttpResponse('<h1>Empleados creados</h1>')
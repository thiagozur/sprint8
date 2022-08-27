"""homebanking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth.models import User
from django.urls import path, include
from django.shortcuts import get_object_or_404
from Clientes.models import Cliente
from Cuentas.models import Cuenta
from Prestamos.models import Prestamo
from rest_framework import routers, serializers, viewsets,  permissions
from rest_framework.permissions import SAFE_METHODS
from django.db.models import Q
from Tarjetas.models import Tarjetas
from direr.models import Sucursal, Direcciones
from rest_framework.response import Response
from rest_framework import status

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'customer_name',
            'customer_surname',
            'customer_dni',
            'dob',
            'branch_id',
            'tipo',
        ]

class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        userobj = get_object_or_404(User, username=self.request.user)
        if userobj.is_staff:
            return super().get_queryset(*args, **kwargs)
        else: 
            uname = userobj.first_name
            usurname = userobj.last_name
            ufullname = uname[0] + usurname
            uidt = userobj.username.split(ufullname)
            if len(uidt) == 2:
                uid = userobj.username.split(ufullname)[1]
            else:
                uid = userobj.id
            clientobj = Cliente.objects.get(customer_id = uid)
            return super().get_queryset(*args, **kwargs).filter(customer_id = clientobj.customer_id)

class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = [
            'account_id',
            'balance',
            'iban',
            'typeid',
        ]

class CuentaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        userobj = get_object_or_404(User, username=self.request.user)
        if userobj.is_staff:
            return super().get_queryset(*args, **kwargs)
        else: 
            uname = userobj.first_name
            usurname = userobj.last_name
            ufullname = uname[0] + usurname
            uidt = userobj.username.split(ufullname)
            if len(uidt) == 2:
                uid = userobj.username.split(ufullname)[1]
            else:
                uid = userobj.id
            clientobj = Cliente.objects.get(customer_id = uid)
            return super().get_queryset(*args, **kwargs).filter(customer_id = clientobj.customer_id)

class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = [
            'loan_type',
            'loan_date',
            'loan_total',
            'account_id',
        ]

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        accid = serializer.data['account_id']
        amount = serializer.data['loan_total']
        cuenta = Cuenta.objects.get(account_id=accid)
        cuenta.balance += int(amount)
        cuenta.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        url = request.get_full_path()
        url = url.split('/')
        length = len(url) - 2
        loanid = url[length]
        loan = Prestamo.objects.get(loan_id=loanid)
        acc = Cuenta.objects.get(account_id=loan.account_id)
        acc.balance -= int(loan.loan_total)
        acc.save()
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self, *args, **kwargs):
        userobj = get_object_or_404(User, username=self.request.user)
        if userobj.is_staff:
            branchid = self.request.query_params.get('sucursal_id')
            if branchid is not None:
                return super().get_queryset(*args, **kwargs).filter()
            return super().get_queryset(*args, **kwargs)
        else: 
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
            qset = ''
            for z, i in enumerate(cuentas):
                if z != len(cuentas) - 1:
                    qset += f'Q(account_id = {i.account_id}) | '
                else:
                    qset += f'Q(account_id = {i.account_id})'
            print(qset)
            return super().get_queryset(*args, **kwargs).filter(eval(qset))

class DireccionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direcciones
        fields = [
            'calle',
            'numero',
            'ciudad',
            'provincia',
            'pais',
            'customerid',
            'employeeid',
            'branchid',
        ]

class DireccionesViewSet(viewsets.ModelViewSet):
    queryset = Direcciones.objects.all()
    serializer_class = DireccionesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        userobj = get_object_or_404(User, username=self.request.user)
        if userobj.is_staff:
            return super().get_queryset(*args, **kwargs)
        else: 
            uname = userobj.first_name
            usurname = userobj.last_name
            ufullname = uname[0] + usurname
            uidt = userobj.username.split(ufullname)
            if len(uidt) == 2:
                uid = userobj.username.split(ufullname)[1]
            else:
                uid = userobj.id
            clientobj = Cliente.objects.get(customer_id = uid)

            return super().get_queryset(*args, **kwargs).filter(customerid = clientobj.customer_id)

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = [
            'branch_number',
            'branch_name',
            'branch_address_id',
        ]

class SucursalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer

class TarjetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarjetas
        fields = [
            'numero',
            'cvv',
            'fechaotorgamiento',
            'fechaexpiracion',
            'tipo',
            'marcaid',
            'customerid',
        ]

class TarjetasViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tarjetas.objects.all()
    serializer_class = TarjetaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        userobj = get_object_or_404(User, username=self.request.user)
        if userobj.is_staff:
            clientid = self.request.query_params.get('customer_id')
            if clientid is not None:
                return super().get_queryset(*args, **kwargs).filter(customerid = clientid)
            return super().get_queryset(*args, **kwargs)
        else: 
            uname = userobj.first_name
            usurname = userobj.last_name
            ufullname = uname[0] + usurname
            uidt = userobj.username.split(ufullname)
            if len(uidt) == 2:
                uid = userobj.username.split(ufullname)[1]
            else:
                uid = userobj.id
            clientobj = Cliente.objects.get(customer_id = uid)
            return super().get_queryset(*args, **kwargs).filter(customerid = clientobj.customer_id)

router = routers.DefaultRouter()
router.register(r'clientes', ClientViewSet)
router.register(r'cuentas', CuentaViewSet)
router.register(r'prestamos', PrestamoViewSet)
router.register(r'direcciones', DireccionesViewSet)
router.register(r'sucursales', SucursalViewSet)
router.register(r'tarjetas', TarjetasViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('Clientes.urls', namespace='Clientes')),
    path('accounts/', include('Cuentas.urls', namespace='Cuentas')),
    path('tarjetas/', include('Tarjetas.urls', namespace='Tarjetas')),
    path('prestamos/', include('Prestamos.urls', namespace='Prestamos')),
    path('', include('Login.urls', namespace='Login')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))
]

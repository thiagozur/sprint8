from django.db import models

# Create your models here.

class Sucursal(models.Model):
    branch_id = models.IntegerField(db_column='branch_id', primary_key=True)
    branch_number = models.IntegerField(db_column='branch_number')
    branch_name = models.CharField(db_column='branch_name', max_length=200)
    branch_address_id = models.IntegerField(db_column='branch_address_id')

class Direcciones(models.Model):
    direccionid = models.IntegerField(db_column='DireccionId', primary_key=True)
    calle = models.CharField(db_column='Calle', max_length=200)
    numero = models.IntegerField(db_column='Numero')
    ciudad = models.CharField(db_column='Ciudad', max_length=200)
    provincia = models.CharField(db_column='Provincia', max_length=200)
    pais = models.CharField(db_column='Pais', max_length=200)
    customerid = models.IntegerField(db_column='CustomerId', null=True)
    employeeid = models.IntegerField(db_column='EmployeeId', null=True)
    branchid = models.IntegerField(db_column='BranchId', null=True)
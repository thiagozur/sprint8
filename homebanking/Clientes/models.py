from django.db import models

# Create your models here.

class TipoClientes(models.Model):
    tipoid = models.AutoField(db_column='TipoId', primary_key=True)  # Field name made lowercase.
    tipo = models.TextField(db_column='Tipo')  # Field name made lowercase.

    class Meta:
        db_table = 'tipo_clientes'

class Cliente(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.TextField()
    customer_surname = models.TextField()  # This field type is a guess.
    customer_dni = models.TextField(db_column='customer_DNI')  # Field name made lowercase.
    dob = models.TextField(blank=True, null=True)
    branch_id = models.IntegerField()
    tipo = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'cliente'

class Empleado(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.TextField()
    employee_surname = models.TextField()
    employee_hire_date = models.TextField()
    employee_dni = models.TextField(db_column='employee_DNI')  # Field name made lowercase.
    branch_id = models.IntegerField()

    class Meta:
        db_table = 'empleado'
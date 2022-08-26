from django.db import models
from Clientes.models import Cliente

# Create your models here.

class MarcasTarjetas(models.Model):
    marcaid = models.AutoField(db_column='MarcaId', primary_key=True)  # Field name made lowercase.
    marca = models.TextField(db_column='Marca')  # Field name made lowercase.

    class Meta:
        db_table = 'marcas_tarjetas'

class Tarjetas(models.Model):
    tarjetaid = models.AutoField(db_column='TarjetaId', primary_key=True)  # Field name made lowercase.
    numero = models.CharField(max_length=500, db_column='Numero')  # Field name made lowercase.
    cvv = models.IntegerField(db_column='CVV')  # Field name made lowercase.
    fechaotorgamiento = models.TextField(db_column='FechaOtorgamiento')  # Field name made lowercase.
    fechaexpiracion = models.TextField(db_column='FechaExpiracion')  # Field name made lowercase.
    tipo = models.TextField(db_column='Tipo')  # Field name made lowercase.
    marcaid = models.ForeignKey(MarcasTarjetas, models.DO_NOTHING, db_column='MarcaId')  # Field name made lowercase.
    customerid = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='CustomerId')  # Field name made lowercase.

    class Meta:
        db_table = 'tarjetas'
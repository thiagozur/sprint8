from django.db import models

# Create your models here.

class TipoCuentas(models.Model):
    tipoid = models.AutoField(db_column='TipoId', primary_key=True)  # Field name made lowercase.
    tipo = models.TextField(db_column='Tipo')  # Field name made lowercase.

    class Meta:
        db_table = 'tipo_cuentas'

class Cuenta(models.Model):
    account_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    balance = models.IntegerField()
    iban = models.TextField()
    typeid = models.ForeignKey('TipoCuentas', models.DO_NOTHING, db_column='typeId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'cuenta'

class Movimientos(models.Model):
    mov_id = models.AutoField(primary_key=True)
    account_id = models.IntegerField(blank=True, null=True)
    mov_total = models.IntegerField(blank=True, null=True)
    mov_type = models.TextField(blank=True, null=True)
    mov_datetime = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'movimientos'
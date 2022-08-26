from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.TipoCuentas)
admin.site.register(models.Cuenta)
admin.site.register(models.Movimientos)
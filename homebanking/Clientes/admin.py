from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.TipoClientes)
admin.site.register(models.Cliente)
admin.site.register(models.Empleado)
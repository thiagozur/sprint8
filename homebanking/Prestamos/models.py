from django.db import models
from datetime import datetime

# Create your models here.

class Prestamo(models.Model):
    fecha = datetime.now().strftime('%Y-%m-%d')
    loan_id = models.AutoField(primary_key=True)
    loan_type = models.TextField()
    loan_date = models.TextField()
    loan_total = models.IntegerField(default=fecha)
    account_id = models.IntegerField()

    class Meta:
        db_table = 'prestamo'
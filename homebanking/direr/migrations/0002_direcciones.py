# Generated by Django 4.1 on 2022-08-26 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direcciones',
            fields=[
                ('direccionid', models.IntegerField(db_column='DireccionId', primary_key=True, serialize=False)),
                ('calle', models.CharField(db_column='Calle', max_length=200)),
                ('numero', models.IntegerField(db_column='Numero')),
                ('ciudad', models.CharField(db_column='Ciudad', max_length=200)),
                ('provincia', models.CharField(db_column='Provincia', max_length=200)),
                ('pais', models.CharField(db_column='Pais', max_length=200)),
                ('customerid', models.IntegerField(db_column='CustomerId', null=True)),
                ('employeeid', models.IntegerField(db_column='EmployeeId', null=True)),
                ('branchid', models.IntegerField(db_column='BranchId', null=True)),
            ],
        ),
    ]
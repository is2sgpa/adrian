# Generated by Django 2.2 on 2019-05-06 03:32

from django.db import migrations, models
import django.db.models.deletion
import django.views.generic.list


class Migration(migrations.Migration):

    dependencies = [
        ('definicion', '0002_auto_20190506_0325'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgregarProyecto',
            fields=[
                ('proyecto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='definicion.Proyecto')),
            ],
            bases=('definicion.proyecto',),
        ),
        migrations.CreateModel(
            name='Proyectos',
            fields=[
                ('proyecto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='definicion.Proyecto')),
            ],
            bases=(django.views.generic.list.ListView, 'definicion.proyecto'),
        ),
    ]

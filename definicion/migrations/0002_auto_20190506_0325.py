# Generated by Django 2.2 on 2019-05-06 03:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('definicion', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomProyecto',
            new_name='CrearProyecto',
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-23 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_controlrecord_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ControlRecord',
        ),
    ]
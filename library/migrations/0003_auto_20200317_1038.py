# Generated by Django 3.0.3 on 2020-03-17 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20200316_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='restrict',
            field=models.BooleanField(blank=True, null=True, verbose_name='制限'),
        ),
    ]

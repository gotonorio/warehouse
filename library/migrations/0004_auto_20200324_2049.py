# Generated by Django 3.0.4 on 2020-03-24 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20200324_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='title',
            field=models.CharField(max_length=255, verbose_name='タイトル'),
        ),
    ]

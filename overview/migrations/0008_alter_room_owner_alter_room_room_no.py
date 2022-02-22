# Generated by Django 4.0.2 on 2022-02-22 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0007_overview_volume_target_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='owner',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='区分所有者'),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_no',
            field=models.IntegerField(unique=True, verbose_name='部屋番号'),
        ),
    ]

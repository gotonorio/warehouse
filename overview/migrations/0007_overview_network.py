# Generated by Django 4.0.4 on 2022-05-29 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0006_alter_room_parking_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='overview',
            name='network',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='インターネット'),
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-22 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0008_alter_room_owner_alter_room_room_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtype',
            name='niwa',
            field=models.IntegerField(default=0, verbose_name='専用庭使用料'),
        ),
    ]
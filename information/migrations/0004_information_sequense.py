# Generated by Django 5.0.6 on 2024-07-01 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0003_information_members_only'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='sequense',
            field=models.IntegerField(default=0, verbose_name='表示順'),
        ),
    ]

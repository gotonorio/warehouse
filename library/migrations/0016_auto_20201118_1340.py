# Generated by Django 3.1.3 on 2020-11-18 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_auto_20201118_1335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='table_of_contents',
            new_name='key_word',
        ),
    ]
# Generated by Django 4.0.2 on 2022-02-20 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0006_rename_bouka_cjhiiki_overview_bouka_chiiki'),
    ]

    operations = [
        migrations.AddField(
            model_name='overview',
            name='volume_target_area',
            field=models.FloatField(blank=True, null=True, verbose_name='容積対象面積'),
        ),
    ]

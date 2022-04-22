# Generated by Django 4.0.3 on 2022-04-01 23:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='overview',
            name='bouka_chiiki',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='防火地域'),
        ),
        migrations.AddField(
            model_name='overview',
            name='constraction',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='施工会社'),
        ),
        migrations.AddField(
            model_name='overview',
            name='delivery_box',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='宅配ボックス'),
        ),
        migrations.AddField(
            model_name='overview',
            name='height_limit',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='高度制限'),
        ),
        migrations.AddField(
            model_name='overview',
            name='management',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='管理会社'),
        ),
        migrations.AddField(
            model_name='overview',
            name='private_water_equipment',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='専有部給水設備'),
        ),
        migrations.AddField(
            model_name='overview',
            name='public_water_equipment',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='共用部給水設備'),
        ),
        migrations.AddField(
            model_name='overview',
            name='required_parking',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='必要駐車場台数'),
        ),
        migrations.AddField(
            model_name='overview',
            name='seller',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='分譲会社'),
        ),
        migrations.AddField(
            model_name='overview',
            name='specified_building_coverage_ratio',
            field=models.FloatField(blank=True, null=True, verbose_name='指定建ぺい率'),
        ),
        migrations.AddField(
            model_name='overview',
            name='specified_floor_area_ratio',
            field=models.FloatField(blank=True, null=True, verbose_name='指定容積率'),
        ),
        migrations.AddField(
            model_name='overview',
            name='trunk_room',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='トランクルーム'),
        ),
        migrations.AddField(
            model_name='overview',
            name='volume_target_area',
            field=models.FloatField(blank=True, null=True, verbose_name='容積対象面積'),
        ),
        migrations.AddField(
            model_name='overview',
            name='youto_chiiki',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='用途地域'),
        ),
        migrations.AddField(
            model_name='room',
            name='building',
            field=models.CharField(blank=True, max_length=64, verbose_name='建物名'),
        ),
        migrations.AddField(
            model_name='room',
            name='comment',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='備考'),
        ),
        migrations.AddField(
            model_name='room',
            name='house_number',
            field=models.CharField(blank=True, max_length=64, verbose_name='番地'),
        ),
        migrations.AddField(
            model_name='room',
            name='mishuu_fee',
            field=models.IntegerField(default=0, verbose_name='滞納費'),
        ),
        migrations.AddField(
            model_name='room',
            name='municipality',
            field=models.CharField(blank=True, max_length=128, verbose_name='市区町村'),
        ),
        migrations.AddField(
            model_name='room',
            name='prefecture',
            field=models.CharField(blank=True, max_length=32, verbose_name='都道府県'),
        ),
        migrations.AddField(
            model_name='room',
            name='tel_number',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message='電話番号はハイフン(-)無しです。', regex='^[0-9]+$')], verbose_name='電話番号'),
        ),
        migrations.AddField(
            model_name='room',
            name='zip_code',
            field=models.CharField(blank=True, max_length=7, verbose_name='郵便番号'),
        ),
        migrations.AddField(
            model_name='roomtype',
            name='number_unit',
            field=models.IntegerField(default=0, verbose_name='住戸数'),
        ),
        migrations.AlterField(
            model_name='overview',
            name='shunkou',
            field=models.IntegerField(verbose_name='竣工年'),
        ),
        migrations.AlterField(
            model_name='overview',
            name='standard_floor_height',
            field=models.CharField(max_length=32, verbose_name='基準階階高'),
        ),
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
        migrations.AlterField(
            model_name='roomtype',
            name='niwa',
            field=models.IntegerField(default=0, verbose_name='専用庭使用料'),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='type_name',
            field=models.CharField(max_length=16, verbose_name='住戸タイプ'),
        ),
    ]
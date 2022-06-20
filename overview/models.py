from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F, Sum
from django.utils import timezone


class OverView(models.Model):
    """ 概要 """
    name = models.CharField(verbose_name='マンション名', max_length=32)
    kenchiku_kakunin = models.DateField(verbose_name='建築確認認可日')
    shunkou = models.IntegerField(verbose_name='竣工年')
    soukosu = models.IntegerField(verbose_name='総住戸数')
    kouzou = models.CharField(verbose_name='構造', max_length=32)
    flat_parking = models.IntegerField(verbose_name='平面駐車場数')
    machine_parking = models.IntegerField(verbose_name='機械式駐車場数')
    bicycle_parking = models.IntegerField(verbose_name='駐輪場数')
    bike_parking = models.IntegerField(verbose_name='バイク置場数')
    site_area = models.FloatField(verbose_name='敷地面積')
    floor_area_ratio = models.FloatField(verbose_name='容積率')
    building_area = models.FloatField(verbose_name='建築面積')
    building_coverage_ratio = models.FloatField(verbose_name='建ぺい率')
    total_floor_area = models.FloatField(verbose_name='延べ床面積')
    volume_target_area = models.FloatField(verbose_name='容積対象面積', blank=True, null=True)
    standard_floor_height = models.CharField(verbose_name='基準階階高', max_length=32)
    max_height = models.FloatField(verbose_name='最高高さ')
    constraction = models.CharField(verbose_name='施工会社', max_length=32, blank=True, null=True)
    seller = models.CharField(verbose_name='分譲会社', max_length=32, blank=True, null=True)
    management = models.CharField(verbose_name='管理会社', max_length=32, blank=True, null=True)
    # 法規制
    youto_chiiki = models.CharField(verbose_name='用途地域', max_length=32, blank=True, null=True)
    specified_floor_area_ratio = models.FloatField(verbose_name='指定容積率', blank=True, null=True)
    bouka_chiiki = models.CharField(verbose_name='防火地域', max_length=32, blank=True, null=True)
    specified_building_coverage_ratio = models.FloatField(verbose_name='指定建ぺい率', blank=True, null=True)
    height_limit = models.CharField(verbose_name='高度制限', max_length=32, blank=True, null=True)
    required_parking = models.CharField(verbose_name='必要駐車場台数', max_length=32, blank=True, null=True)
    # 設備概要
    private_water_equipment = models.CharField(verbose_name='専有部給水設備', max_length=32, blank=True, null=True)
    public_water_equipment = models.CharField(verbose_name='共用部給水設備', max_length=32, blank=True, null=True)
    trunk_room = models.CharField(verbose_name='トランクルーム', max_length=32, blank=True, null=True)
    delivery_box = models.CharField(verbose_name='宅配ボックス', max_length=32, blank=True, null=True)
    network = models.CharField(verbose_name='インターネット', max_length=32, blank=True, null=True)
    entrance = models.CharField(verbose_name='共用部エントランス', max_length=32, blank=True, null=True)
    security = models.CharField(verbose_name='防犯カメラ', max_length=32, blank=True, null=True)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    """ 住戸タイプ """
    type_name = models.CharField(verbose_name='住戸タイプ', max_length=16)
    area = models.FloatField(verbose_name='専有面積')
    kanrihi = models.IntegerField(verbose_name='管理費')
    shuuzenhi = models.IntegerField(verbose_name='修繕積立金')
    ryokuchi = models.IntegerField(verbose_name='緑地維持管理費')
    niwa = models.IntegerField(verbose_name='専用庭使用料', default=0)
    number_unit = models.IntegerField(verbose_name='住戸数', default=0)

    def __str__(self):
        return self.type_name

    @classmethod
    def total_kanrihi(cls):
        """ 管理費の合計を返す """
        qs = cls.objects.annotate(total=F('number_unit')*F('kanrihi')).aggregate(Sum('total'))
        return qs

    @classmethod
    def total_shuuzenhi(cls):
        """ 修繕費の合計を返す """
        qs = cls.objects.annotate(total=F('number_unit')*F('shuuzenhi')).aggregate(Sum('total'))
        return qs

    @classmethod
    def total_niwa(cls):
        """ 専用庭使用料の合計を返す """
        qs = cls.objects.annotate(total=F('number_unit')*F('niwa')).aggregate(Sum('total'))
        return qs

    @classmethod
    def total_ryokuchi(cls):
        """ 緑地管理費の合計を返す """
        qs = cls.objects.annotate(total=F('number_unit')*F('ryokuchi')).aggregate(Sum('total'))
        return qs


class Room(models.Model):
    """ 住戸データ """
    created_date = models.DateTimeField(verbose_name='更新日', default=timezone.now)
    room_no = models.IntegerField(verbose_name='部屋番号', unique=True)
    room_type = models.ForeignKey(RoomType, verbose_name='住戸タイプ',  on_delete=models.PROTECT)
    owner = models.CharField(verbose_name='区分所有者', max_length=64, blank=True, null=True)
    tenant = models.CharField(verbose_name='賃借人', max_length=64, blank=True, null=True)
    parking_fee = models.IntegerField(verbose_name='駐車場使用料', default=0)
    parking_date = models.DateTimeField(verbose_name='駐車場使用料更新日', null=True, blank=True)
    bicycle_fee = models.IntegerField(verbose_name='駐輪場使用料', default=0)
    bike_fee = models.IntegerField(verbose_name='バイク置場使用料', default=0)
    chounaikai = models.BooleanField(verbose_name='町内会費', default=False)
    mishuu_fee = models.IntegerField(verbose_name='滞納費', default=0)
    comment = models.CharField(verbose_name='備考', max_length=128, blank=True, null=True)
    """ 住所データ """
    zip_code = models.CharField(verbose_name='郵便番号', max_length=7, blank=True, null=True)
    prefecture = models.CharField(verbose_name='都道府県', max_length=32, blank=True, null=True)
    municipality = models.CharField(verbose_name='市区町村', max_length=128, blank=True, null=True)
    house_number = models.CharField(verbose_name='番地', max_length=64, blank=True, null=True)
    building = models.CharField(verbose_name='建物名', max_length=64, blank=True, null=True)
    tel_number_regex = RegexValidator(regex=r'^[0-9]+$', message=("電話番号はハイフン(-)無しです。"))
    tel_number = models.CharField(verbose_name='電話番号', validators=[
                                  tel_number_regex], max_length=16, null=True, blank=True)

    def __str__(self):
        return self.owner

from django.db import models
from django.db.models import F, Sum


class OverView(models.Model):
    """概要"""

    name = models.CharField(verbose_name="マンション名", max_length=32)
    kenchiku_kakunin = models.DateField(verbose_name="建築確認認可日")
    shunkou = models.IntegerField(verbose_name="竣工年")
    soukosu = models.IntegerField(verbose_name="総住戸数")
    kouzou = models.CharField(verbose_name="構造", max_length=32)
    flat_parking = models.IntegerField(verbose_name="平面駐車場数")
    machine_parking = models.IntegerField(verbose_name="機械式駐車場数")
    bicycle_parking = models.IntegerField(verbose_name="駐輪場数")
    bike_parking = models.IntegerField(verbose_name="バイク置場数")
    site_area = models.FloatField(verbose_name="敷地面積")
    floor_area_ratio = models.FloatField(verbose_name="容積率")
    building_area = models.FloatField(verbose_name="建築面積")
    building_coverage_ratio = models.FloatField(verbose_name="建ぺい率")
    total_floor_area = models.FloatField(verbose_name="延べ床面積")
    volume_target_area = models.FloatField(verbose_name="容積対象面積", blank=True, null=True)
    standard_floor_height = models.CharField(verbose_name="基準階階高", max_length=32)
    max_height = models.FloatField(verbose_name="最高高さ")
    constraction = models.CharField(verbose_name="施工会社", max_length=32, blank=True, null=True)
    seller = models.CharField(verbose_name="分譲会社", max_length=32, blank=True, null=True)
    management = models.CharField(verbose_name="管理会社", max_length=32, blank=True, null=True)
    # 法規制
    youto_chiiki = models.CharField(verbose_name="用途地域", max_length=32, blank=True, null=True)
    specified_floor_area_ratio = models.FloatField(verbose_name="指定容積率", blank=True, null=True)
    bouka_chiiki = models.CharField(verbose_name="防火地域", max_length=32, blank=True, null=True)
    specified_building_coverage_ratio = models.FloatField(verbose_name="指定建ぺい率", blank=True, null=True)
    height_limit = models.CharField(verbose_name="高度制限", max_length=32, blank=True, null=True)
    required_parking = models.CharField(verbose_name="必要駐車場台数", max_length=32, blank=True, null=True)
    # 設備概要
    private_water_equipment = models.CharField(
        verbose_name="専有部給水設備", max_length=32, blank=True, null=True
    )
    public_water_equipment = models.CharField(
        verbose_name="共用部給水設備", max_length=32, blank=True, null=True
    )
    trunk_room = models.CharField(verbose_name="トランクルーム", max_length=32, blank=True, null=True)
    delivery_box = models.CharField(verbose_name="宅配ボックス", max_length=32, blank=True, null=True)
    network = models.CharField(verbose_name="インターネット", max_length=32, blank=True, null=True)
    entrance = models.CharField(verbose_name="共用部エントランス", max_length=32, blank=True, null=True)
    security = models.CharField(verbose_name="防犯カメラ", max_length=32, blank=True, null=True)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    """住戸タイプ"""

    type_name = models.CharField(verbose_name="住戸タイプ", max_length=16)
    area = models.FloatField(verbose_name="専有面積")
    kanrihi = models.IntegerField(verbose_name="管理費")
    shuuzenhi = models.IntegerField(verbose_name="修繕積立金")
    ryokuchi = models.IntegerField(verbose_name="緑地維持管理費")
    niwa = models.IntegerField(verbose_name="専用庭使用料", default=0)
    number_unit = models.IntegerField(verbose_name="住戸数", default=0)

    def __str__(self):
        return self.type_name

    @classmethod
    def total_kanrihi(cls, kanrihi_name):
        """全戸数分の管理費等の合計を返す
        kanrihi_nameとしては、
        - kanrihi
        - shuuzenhi
        - niwa
        - ryokuchi
        annnotateでフィールド間演算処理をして、aggrefateで集計処理を行う
        """
        qs = cls.objects.annotate(total=F("number_unit") * F(kanrihi_name)).aggregate(Sum("total"))
        return qs

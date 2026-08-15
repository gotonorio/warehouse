import logging

from django.db import models

logger = logging.getLogger(__name__)


class ControlRecord(models.Model):
    """プロジェクトのコントロール用定数を定義"""

    # 仮登録メニューの表示/非表示コントロール
    tmp_user_flg = models.BooleanField(verbose_name="仮登録", default=False)

    @classmethod
    def get_tmp_user_flg(cls):
        config, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                "tmp_user_flg": False,
            },
        )
        return config.tmp_user_flg

import logging

from django.db import models

logger = logging.getLogger(__name__)


class ControlRecord(models.Model):
    """プロジェクトのコントロール用定数を定義"""

    # 仮登録メニューの表示/非表示コントロール
    tmp_user_flg = models.BooleanField(verbose_name="仮登録", default=False)
    # add your control variable

    @classmethod
    def show_tmp_user_menu(cls):
        return cls.objects.get("tmp_user_flg")

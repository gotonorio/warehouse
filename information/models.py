from django.db import models
from django.utils import timezone


class Information(models.Model):
    """情報"""

    title = models.CharField(verbose_name="Title", max_length=255)
    comment = models.CharField(verbose_name="概要", max_length=255, blank=True)
    information = models.TextField(verbose_name="HTML文")
    display_info = models.BooleanField(verbose_name="表示", default=True)
    created_at = models.DateTimeField(verbose_name="作成日", default=timezone.now)

    def __str__(self):
        return self.title

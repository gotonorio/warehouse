from django.db import models
from django.utils import timezone


class Information(models.Model):
    """ 情報 """
    title = models.CharField('Title', max_length=255)
    comment = models.CharField('概要', max_length=255, blank=True)
    information = models.TextField('HTML文')
    display_info = models.BooleanField('表示', default=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.title

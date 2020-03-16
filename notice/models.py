
from django.db import models
from django.utils import timezone


class News(models.Model):
    """ お知らせ """
    title = models.CharField('お知らせ', max_length=255)
    comment = models.TextField('内容')
    display_news = models.BooleanField('表示', default=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.title

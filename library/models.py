import os

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone


def default_category():
    """デフォルトのカテゴリを返す（まだなければ作る）."""
    category, _ = Category.objects.get_or_create(name='default')
    return category


class BigCategory(models.Model):
    name = models.CharField('親カテゴリ名', max_length=255)
    rank = models.IntegerField('表示順', default=0)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    alive = models.BooleanField('有効', default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """カテゴリ."""
    name = models.CharField('カテゴリ名', max_length=255)
    path_name = models.CharField('ディレクトリ名', max_length=255)
    parent = models.ForeignKey(BigCategory, verbose_name='親カテゴリ',
                               on_delete=models.PROTECT, default=1)
    rank = models.IntegerField('表示順', default=0)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    restrict = models.BooleanField('制限', default=False)
    alive = models.BooleanField('有効', default=True)

    def __str__(self):
        return self.name


def get_upload_to(instance, filename):
    """ upload_toを動的に指定する
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    ここで、ファイルをuploadするパスを設定する。
    media/カテゴリのpath/filename
    """
    try:
        path = os.path.join(str(instance.category.path_name), filename)
    except Exception as e:
        _ = e
        path = os.path.join('default', filename)
    return path


class File(models.Model):
    """アップロードするファイル."""
    title = models.CharField('タイトル', max_length=255)
    category = models.ForeignKey(Category, verbose_name='カテゴリ',
                                 on_delete=models.PROTECT, default=1)
    comment = models.TextField('コメント', blank=True, null=True)
    table_of_contents = models.TextField('目次', blank=True, null=True)
    src = models.FileField('ファイル', upload_to=get_upload_to)
    rank = models.IntegerField('表示順', default=0)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    alive = models.BooleanField('表示', default=True)
    download = models.BooleanField('ダウンロード', default=False)

    def __str__(self):
        return self.title

    def get_filename(self):
        """ ファイル名を返す """
        return os.path.basename(self.src.name)


"""
# Fileオブジェクトのインスタンスが削除されたら、ファイル自体も削除する。
# https://docs.djangoproject.com/ja/2.1/ref/signals/
# http://note.crohaco.net/2018/django-signals/
# https://qiita.com/key/items/73744c3396b08bc0debd

シグナル：post_delete（インスタンスが削除されると発火する）
        pre_deleteの方が良いのかも。
ハンドラ：delete_media_file()（シグナルを受けて実ファイルを削除する）
デコレータ：@receiver（シグナルとハンドラを関連付ける）
post_deleteで送信される引数：sender(model class)、
                instannce(deleted instance)、using(**kwargs)
"""
@receiver(post_delete, sender=File)
def delete_media_file(sender, instance, **kwargs):
    instance.src.delete(False)

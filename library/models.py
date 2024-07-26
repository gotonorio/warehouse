# import os
from pathlib import Path

from django.db import models

# from django.db.models.signals import post_delete
# from django.dispatch import receiver
from django.utils import timezone
from pypdf import PdfReader, PdfWriter


def default_category():
    """デフォルトのカテゴリを返す（まだなければ作る）"""
    category, _ = Category.objects.get_or_create(name="default")
    return category


class BigCategory(models.Model):
    """親カテゴリ"""

    name = models.CharField("親カテゴリ名", max_length=128)
    rank = models.IntegerField("表示順", default=0)
    created_at = models.DateTimeField("作成日", default=timezone.now)
    alive = models.BooleanField("有効", default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """カテゴリ
    - カテゴリ毎に閲覧制限することを考えて、restric要素を追加しておく。
    """

    name = models.CharField("カテゴリ名", max_length=128)
    path_name = models.CharField("ディレクトリ名", max_length=128)
    parent = models.ForeignKey(BigCategory, verbose_name="親カテゴリ", on_delete=models.PROTECT, default=1)
    rank = models.IntegerField("表示順", default=0)
    created_at = models.DateTimeField("作成日", default=timezone.now)
    restrict = models.BooleanField("制限", default=False)
    alive = models.BooleanField("有効", default=True)

    def __str__(self):
        return self.name


def get_upload_to(instance, filename):
    """upload_toを動的(カテゴリのpath毎)に指定する
    https://docs.djangoproject.com/ja/5.0/ref/models/fields/
    ここで、ファイルをuploadするパスを設定する。
    media/カテゴリのpath/filename
    """
    # ToDo
    directory_path = Path(str(instance.category.path_name))
    try:
        path = directory_path / filename
    except Exception as e:
        _ = e
        path = Path("default") / filename
    # try:
    #     path = os.path.join(str(instance.category.path_name), filename)
    # except Exception as e:
    #     _ = e
    #     path = os.path.join("default", filename)
    return path


class File(models.Model):
    """アップロードするファイル.
    - FileFieldにより、ファイルシステム（/media/）に保存する。
    """

    title = models.CharField(verbose_name="タイトル", max_length=128)
    category = models.ForeignKey(Category, verbose_name="カテゴリ", on_delete=models.PROTECT, default=1)
    summary = models.TextField(verbose_name="概要", blank=True, null=True)
    key_word = models.TextField(verbose_name="キーワード", blank=True, null=True)
    src = models.FileField(verbose_name="ファイル", upload_to=get_upload_to)
    rank = models.IntegerField(verbose_name="表示順", default=0)
    created_at = models.DateTimeField(verbose_name="作成日", default=timezone.now)
    alive = models.BooleanField(verbose_name="表示", default=True)
    download = models.BooleanField(verbose_name="ダウンロード", default=False)

    def __str__(self):
        return self.title

    def get_filename(self):
        """ファイル名を返す"""
        # return os.path.basename(self.src.name)
        return Path(self.src.name).name

    @staticmethod
    def fix_pdf_file(input_file_path):
        """「Microsoft Print to PDF」によるtitleの文字化けを修正する
        - 保存したpdfファイルのmetadataを修正して保存する。
        """
        # file名
        new_title = Path(input_file_path).name

        # Open the original PDF
        with open(input_file_path, "rb") as input_file_path:
            # PDFファイルの読み込み
            reader = PdfReader(input_file_path)
            # PDF出力用のオブジェクトを用意
            writer = PdfWriter()

            # Copy all pages from the reader to the writer
            for page_num in range(len(reader.pages)):
                writer.add_page(reader.pages[page_num])

            # metadataの「文字化けTitle」を「new_title」に修正する。
            metadata = reader.metadata
            new_metadata = {key: metadata[key] for key in metadata if key != "/Title"}
            # 「/Title」を「new_title」に修正する。
            new_metadata["/Title"] = new_title
            # 「/Author」は除去する。
            new_metadata["/Author"] = ""
            # new_metadataをセットする。
            writer.add_metadata(new_metadata)
            # pdfオブジェクトを出力してみる。
            print(writer)

            # metadataを修正したファイルを保存する。
            with open(input_file_path, "wb") as output_pdf_file:
                writer.write(output_pdf_file)


# django-cleanupモジュールを使うことにしたため不要。
# https://blog.narito.ninja/detail/186
#
# @receiver(post_delete, sender=File)
# def delete_media_file(sender, instance, **kwargs):
#     """
#     Fileオブジェクトのインスタンスが削除されたら、ファイル自体も削除する。
#     https://docs.djangoproject.com/ja/3.2/topics/signals/
#     http://note.crohaco.net/2018/django-signals/
#     デコレータ：@receiver（シグナルとハンドラを関連付ける）
#     シグナル：post_delete（インスタンスが削除されると発火する）
#             pre_deleteの方が良いのかも。
#     ハンドラ：delete_media_file()（シグナルを受けて実ファイルを削除する）
#     post_deleteで送信される引数：sender(model class)、
#                     instannce(deleted instance)、using(**kwargs)
#     """
#     instance.src.delete(False)

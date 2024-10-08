# Generated by Django 3.2.6 on 2021-08-09 08:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import library.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BigCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128, verbose_name="親カテゴリ名")),
                ("rank", models.IntegerField(default=0, verbose_name="表示順")),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="作成日"
                    ),
                ),
                ("alive", models.BooleanField(default=True, verbose_name="有効")),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128, verbose_name="カテゴリ名")),
                ("path_name", models.CharField(max_length=128, verbose_name="ディレクトリ名")),
                ("rank", models.IntegerField(default=0, verbose_name="表示順")),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="作成日"
                    ),
                ),
                ("restrict", models.BooleanField(default=False, verbose_name="制限")),
                ("alive", models.BooleanField(default=True, verbose_name="有効")),
                (
                    "parent",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="library.bigcategory",
                        verbose_name="親カテゴリ",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128, verbose_name="タイトル")),
                ("summary", models.TextField(blank=True, null=True, verbose_name="概要")),
                (
                    "key_word",
                    models.TextField(blank=True, null=True, verbose_name="キーワード"),
                ),
                (
                    "src",
                    models.FileField(
                        upload_to=library.models.get_upload_to, verbose_name="ファイル"
                    ),
                ),
                ("rank", models.IntegerField(default=0, verbose_name="表示順")),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="作成日"
                    ),
                ),
                ("alive", models.BooleanField(default=True, verbose_name="表示")),
                ("download", models.BooleanField(default=False, verbose_name="ダウンロード")),
                (
                    "category",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="library.category",
                        verbose_name="カテゴリ",
                    ),
                ),
            ],
        ),
    ]

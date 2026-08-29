import unicodedata

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from library.forms import CategoryForm, FileForm
from library.models import Category


# -----------------------------------------------------------------------------
# FileFormのテスト
# -----------------------------------------------------------------------------
def make_uploaded_file(name="test.pdf", size=1024):
    """任意サイズのダミーファイルを作る"""
    return SimpleUploadedFile(
        name=name,
        content=b"a" * size,  # size バイトのダミー
        content_type="application/pdf",
    )


@pytest.mark.django_db
def test_fileform_invalid_extension(big_category):
    """不正拡張子は ValidationError になる"""

    cat = Category.objects.create(
        name="cat",
        path_name="cat",
        alive=True,
        parent=big_category,
    )

    form = FileForm(
        data={
            "title": "test",
            "category": cat.id,
            "rank": 1,
            "alive": True,
            "download": False,
            "is_confidential": False,
        },
        files={"src": make_uploaded_file(name="bad.txt")},
    )

    assert not form.is_valid()
    assert "PDFまたはZIPファイルのみアップロード可能です。" in form.errors["src"]


@pytest.mark.django_db
def test_fileform_file_size_over_limit(settings, big_category):
    """サイズオーバーは ValidationError になる"""

    settings.FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB

    cat = Category.objects.create(
        name="cat",
        path_name="cat",
        alive=True,
        parent=big_category,
    )

    # 51MB のダミーファイル
    big_file = make_uploaded_file(name="big.pdf", size=51 * 1024 * 1024)

    form = FileForm(
        data={
            "title": "test",
            "category": cat.id,
            "rank": 1,
            "alive": True,
            "download": False,
            "is_confidential": False,
        },
        files={"src": big_file},
    )

    assert not form.is_valid()
    assert "ファイルサイズは50MB以下に分割してください。" in form.errors["src"]


@pytest.mark.django_db
def test_fileform_valid_pdf(big_category):
    """PDF でサイズ以内なら成功"""

    cat = Category.objects.create(
        name="cat",
        path_name="cat",
        alive=True,
        parent=big_category,
    )

    form = FileForm(
        data={
            "title": "test",
            "category": cat.id,
            "rank": 1,
            "alive": True,
            "download": False,
            "is_confidential": False,
        },
        files={"src": make_uploaded_file(name="ok.pdf", size=1024)},
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_fileform_filename_normalized(big_category):
    """ファイル名が NFKC 正規化される"""

    cat = Category.objects.create(
        name="cat",
        path_name="cat",
        alive=True,
        parent=big_category,
    )

    # 全角のファイル名
    uploaded = make_uploaded_file(name="ｔｅｓｔ.pdf")

    form = FileForm(
        data={
            "title": "test",
            "category": cat.id,
            "rank": 1,
            "alive": True,
            "download": False,
            "is_confidential": False,
        },
        files={"src": uploaded},
    )

    assert form.is_valid()
    cleaned = form.cleaned_data["src"]
    assert cleaned.name == unicodedata.normalize("NFKC", "ｔｅｓｔ.pdf")


@pytest.mark.django_db
def test_fileform_category_queryset_filtered(big_category):
    """category queryset が alive=True のみになる"""

    alive_cat = Category.objects.create(
        name="alive",
        path_name="alive",
        alive=True,
        parent=big_category,
    )
    dead_cat = Category.objects.create(
        name="dead",
        path_name="dead",
        alive=False,
        parent=big_category,
    )

    form = FileForm()

    qs = form.fields["category"].queryset

    assert alive_cat in qs
    assert dead_cat not in qs


# -----------------------------------------------------------------------------
# CategoryFormのテスト
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_categoryform_invalid_path_name(big_category):
    """path_name が不正なら ValidationError"""

    form = CategoryForm(
        data={
            "name": "test",
            "path_name": "あいうえお",  # 不正（英数字・ハイフン・アンダースコア以外）
            "parent": big_category.id,
            "rank": 1,
            "restrict": False,
            "alive": True,
        }
    )

    assert not form.is_valid()
    assert "英数字・ハイフン・アンダースコアのみ使用可能です。" in form.errors["path_name"]


@pytest.mark.django_db
def test_categoryform_valid_path_name(big_category):
    """path_name が正しければ成功"""

    form = CategoryForm(
        data={
            "name": "test",
            "path_name": "valid_path-123",
            "parent": big_category.id,
            "rank": 1,
            "restrict": False,
            "alive": True,
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_categoryform_name_normalized(big_category):
    """name が NFKC 正規化される"""

    form = CategoryForm(
        data={
            "name": "ｔｅｓｔ",  # 全角
            "path_name": "valid",
            "parent": big_category.id,
            "rank": 1,
            "restrict": False,
            "alive": True,
        }
    )

    assert form.is_valid()
    cleaned = form.cleaned_data["name"]
    assert cleaned == unicodedata.normalize("NFKC", "ｔｅｓｔ")


@pytest.mark.django_db
def test_categoryform_valid(big_category):
    """全て正しい"""
    form = CategoryForm(
        data={
            "name": "Category",
            "path_name": "category_1",
            "parent": big_category.id,
            "rank": 10,
            "restrict": False,
            "alive": True,
        }
    )

    assert form.is_valid()

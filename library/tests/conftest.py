import logging

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.core.files.uploadedfile import SimpleUploadedFile

from library.models import BigCategory, Category, File

# faker と factory_boy の DEBUG ログを強制的に WARNING 以上に制限
logging.getLogger("faker").setLevel(logging.WARNING)
logging.getLogger("factory").setLevel(logging.WARNING)

User = get_user_model()


# -----------------------------------------------------------------------------
# テスト用グループの作成
# -----------------------------------------------------------------------------
@pytest.fixture
def test_group_chairman():
    """テスト用のchairmanグループを作成するfixture"""
    return Group.objects.create(name="chairman")


@pytest.fixture
def test_group_data_manager():
    """テスト用のdata_managerグループを作成するfixture"""
    return Group.objects.create(name="data_manager")


@pytest.fixture
def test_group_sophiag():
    """テスト用のsophiagグループを作成するfixture"""
    return Group.objects.create(name="sophiag")


# -----------------------------------------------------------------------------
# テスト用パーミッションの作成
# -----------------------------------------------------------------------------
@pytest.fixture
def test_permission_view_file():
    """ログインユーザのパーミッション生成"""
    return Permission.objects.get(
        codename="view_file",
        content_type__app_label="library",
    )


@pytest.fixture
def test_permission_add_file():
    """ファイル登録ユーザのパーミッション生成"""
    return Permission.objects.get(
        codename="add_file",
        content_type__app_label="library",
    )


# -----------------------------------------------------------------------------
# テスト用ユーザーの作成
# -----------------------------------------------------------------------------
@pytest.fixture
def test_user_anonymous():
    """未ログインユーザー"""
    return AnonymousUser()


@pytest.fixture
def test_user_sophiag(test_group_sophiag, test_permission_view_file):
    """sophiagユーザー"""
    user_sophiag = User.objects.create_user(username="sophiag", password="pass")
    user_sophiag.groups.add(test_group_sophiag)
    user_sophiag.user_permissions.add(test_permission_view_file)
    return user_sophiag


@pytest.fixture
def test_user_chairman(test_group_chairman, test_permission_view_file):
    """chairmanユーザー"""
    user_chairman = User.objects.create_user(username="chairman", password="pass")
    user_chairman.groups.add(test_group_chairman)
    user_chairman.user_permissions.add(test_permission_view_file)
    return user_chairman


@pytest.fixture
def test_user_data_manager(test_group_data_manager, test_permission_view_file):
    """data_managerユーザー"""
    user_data_manager = User.objects.create_user(username="dm", password="pass")
    user_data_manager.groups.add(test_group_data_manager)
    user_data_manager.user_permissions.add(test_permission_view_file)
    return user_data_manager


@pytest.fixture
def data_manager(test_group_data_manager, test_permission_add_file):
    """data_managerユーザー"""
    user_data_manager = User.objects.create_user(username="dm", password="pass")
    user_data_manager.groups.add(test_group_data_manager)
    user_data_manager.user_permissions.add(test_permission_add_file)
    return user_data_manager


@pytest.fixture
def test_staff_user(db):
    """staffユーザ"""
    return User.objects.create_user(
        username="staff_user",
        password="pass",
        is_staff=True,
    )


# -----------------------------------------------------------------------------
# テスト用のpdfファイルを作成する
# -----------------------------------------------------------------------------
@pytest.fixture
def big_category():
    return BigCategory.objects.create(name="big")


@pytest.fixture
def category_normal(big_category):
    """誰でも閲覧可能なCategoryクラス（restrict=False）を作成"""
    return Category.objects.create(
        name="cat1",
        path_name="cat1",
        parent=big_category,
        restrict=False,
    )


@pytest.fixture
def category_restrict(big_category):
    """restrict=True の Categoryクラスを作成"""
    return Category.objects.create(
        name="cat2",
        path_name="cat2",
        parent=big_category,
        restrict=True,
    )


# test.pdfを保存するため、テスト用のMEDIA_ROOTを作成する
# tmp_pathでsettings.MEDIA_ROOTを上書きすることで、テスト終了後に後始末をしてくれる
@pytest.fixture
def media_root(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    return tmp_path


@pytest.fixture
def test_pdf():
    return SimpleUploadedFile("test.pdf", b"%PDF-1.4 test content", content_type="application/pdf")


# テスト用のMEDIA_ROOTにtest.pdfを作成する
# fixtureを実行させるためにmedia_rootを引数に設定することで、tmp_pathのMEDIA_ROOTを使うことになる
@pytest.fixture
def file_normal(category_normal, test_pdf):
    return File.objects.create(
        title="normal",
        category=category_normal,
        src=test_pdf,
        is_confidential=False,
        download=False,
    )


# テスト用のMEDIA_ROOTにtest.pdfを作成する
# fixtureを実行させるためにmedia_rootを引数に設定することで、tmp_pathのMEDIA_ROOTを使うことになる
@pytest.fixture
def file_confidential(category_normal, test_pdf):
    return File.objects.create(
        title="secret",
        category=category_normal,
        src=test_pdf,
        is_confidential=True,
        download=False,
    )


# テスト用のMEDIA_ROOTにtest.pdfを作成する
# fixtureを実行させるためにmedia_rootを引数に設定することで、tmp_pathのMEDIA_ROOTを使うことになる
@pytest.fixture
def file_restrict(category_restrict, test_pdf):
    return File.objects.create(
        title="restrict",
        category=category_restrict,
        src=test_pdf,
        is_confidential=False,
        download=False,
    )


# -----------------------------------------------------------------------------
# 検索処理用のテストデータ
# -----------------------------------------------------------------------------
@pytest.fixture
def normal_user(db):
    return User.objects.create_user(
        username="normal_user",
        password="pass",
    )


@pytest.fixture
def file_factory(db, category_restrict, test_pdf):
    def create_file(**kwargs):
        defaults = {
            "title": "テストタイトル",
            "category": category_restrict,
            "src": test_pdf,
            "key_word": "テストキーワード",
            "summary": "テスト概要",
            "alive": True,
            "is_confidential": False,
        }
        defaults.update(kwargs)
        return File.objects.create(**defaults)

    return create_file


# @pytest.fixture
# def data_manager(db):
#     user = User.objects.create_user(
#         username="data_manager",
#         password="pass",
#     )

#     permission = Permission.objects.get(
#         codename="add_file",
#         content_type__app_label="library",
#     )
#     user.user_permissions.add(permission)

#     return user

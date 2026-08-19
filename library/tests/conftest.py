import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.files.uploadedfile import SimpleUploadedFile

from library.models import BigCategory, Category, File

User = get_user_model()


@pytest.fixture
def test_group_chairman(db):
    """テスト用のchairmanグループを作成するfixture"""
    return Group.objects.create(name="chairman")


@pytest.fixture
def test_group_data_manager(db):
    """テスト用のdata_managerグループを作成するfixture"""
    return Group.objects.create(name="data_manager")


@pytest.fixture
def test_permission_view_file(db):
    """パーミッション取得"""
    return Permission.objects.get(codename="view_file")


@pytest.fixture
def test_user_no_perm(db, test_permission_view_file):
    user = User.objects.create_user(username="noperm", password="pass")
    user.user_permissions.remove(test_permission_view_file)
    return user


@pytest.fixture
def test_user_chairman(db, test_group_chairman, test_permission_view_file):
    """chairmanユーザー"""
    user_chairman = User.objects.create_user(username="chairman", password="pass")
    user_chairman.groups.add(test_group_chairman)
    user_chairman.user_permissions.add(test_permission_view_file)
    return user_chairman


# @pytest.fixture
# def test_user_data_manager(db, test_group_data_manager, test_permission_view_file):
#     """data_managerユーザー"""
#     user_data_manager = User.objects.create_user(username="data_manager", password="pass")
#     user_data_manager.groups.add(test_group_data_manager)
#     user_data_manager.user_permissions.add(test_permission_view_file)
#     return user_data_manager


@pytest.fixture
def test_user_data_manager(db):
    """data_managerユーザー"""
    return User.objects.create_user(username="dm", password="pass")


# -----------------------------------------------------------------------------
# conftest.py に追加
# -----------------------------------------------------------------------------
@pytest.fixture
def big_category(db):
    return BigCategory.objects.create(name="big")


@pytest.fixture
def category_normal(db, big_category):
    """誰でも閲覧可能なCategoryクラス（restrict=False）を作成"""
    return Category.objects.create(
        name="cat1",
        path_name="cat1",
        parent=big_category,
        restrict=False,
    )


@pytest.fixture
def category_restrict(db, big_category):
    """restrict=True の Categoryクラスを作成"""
    return Category.objects.create(
        name="cat2",
        path_name="cat2",
        parent=big_category,
        restrict=True,
    )


@pytest.fixture
def test_pdf():
    return SimpleUploadedFile("test.pdf", b"%PDF-1.4 test content", content_type="application/pdf")


@pytest.fixture
def file_normal(db, category_normal, test_pdf):
    return File.objects.create(
        title="normal",
        category=category_normal,
        src=test_pdf,
        is_confidential=False,
        download=False,
    )


@pytest.fixture
def file_confidential(db, category_normal, test_pdf):
    return File.objects.create(
        title="secret",
        category=category_normal,
        src=test_pdf,
        is_confidential=True,
        download=False,
    )


@pytest.fixture
def file_restrict(db, category_restrict, test_pdf):
    return File.objects.create(
        title="restrict",
        category=category_restrict,
        src=test_pdf,
        is_confidential=False,
        download=False,
    )

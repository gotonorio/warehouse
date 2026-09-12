import pytest
from django.contrib.auth.models import Permission
from django.test import Client
from django.urls import reverse

from library.views.search_views import search


@pytest.mark.django_db
def test_anonymous_user_is_redirected():
    """未ログインユーザはログイン画面にリダイレクトするために、status_codeをチェックする"""

    # 1. 未ログインユーザのクライアントfixture
    client = Client()

    # 2. テスト対象のURLを逆引き
    target_url = reverse("library:search")
    login_url = reverse("register:login")

    # 3. 未ログイン状態でGETリクエストを送信
    response = client.get(target_url)

    # 4. ログイン画面（デフォルトは /accounts/login/）へリダイレクトされるか検証
    assert response.status_code == 302

    # 5. 期待するリダイレクト先URL（?next= パラメータ付き）を組み立てて完全一致検証
    expected_redirect_url = f"{login_url}?next={target_url}"
    assert response.url == expected_redirect_url


@pytest.mark.django_db
def test_search_empty_keyword(test_user_sophiag):
    """検索キーワードが空なら空のQuerySetを返す"""
    result = search("", test_user_sophiag)

    assert not result.exists()


# @pytest.mark.django_db
# def test_search_none_keyword(test_user_sophiag):
#     """検索キーワードがNoneなら空のQuerySetを返す"""
#     result = search(None, test_user_sophiag)

#     assert not result.exists()


@pytest.mark.django_db
def test_search_title(test_user_sophiag, file_factory):
    """titleに検索ワードが含まれるFileを検索できる
    - テスト用に2つのファイルを作成し、そのうちtargetのファイルだけを検索できるか
    """
    target = file_factory(title="総会のお知らせ")
    file_factory(title="修繕工事のお知らせ")

    result = search("総会", test_user_sophiag)

    assert list(result) == [target]


@pytest.mark.django_db
def test_search_key_word(test_user_sophiag, file_factory):
    """key_wordに検索ワードが含まれるFileを検索できる"""
    target = file_factory(key_word="総会 理事会")
    file_factory(key_word="修繕 工事")

    result = search("理事会", test_user_sophiag)

    assert list(result) == [target]


@pytest.mark.django_db
def test_search_summary(test_user_sophiag, file_factory):
    """summaryに検索ワードが含まれるFileを検索できる"""
    target = file_factory(summary="2026年度の通常総会についてのお知らせです")
    file_factory(summary="大規模修繕工事についてのお知らせです")

    result = search("通常総会", test_user_sophiag)

    assert list(result) == [target]


@pytest.mark.django_db
def test_search_multiple_keywords(test_user_sophiag, file_factory):
    """複数のキーワードはAND検索される"""
    target = file_factory(
        title="通常総会のお知らせ",
        summary="2026年度の通常総会を開催します",
    )

    file_factory(
        title="通常総会のお知らせ",
        summary="2025年度の通常総会について",
    )

    file_factory(
        title="修繕工事のお知らせ",
        summary="工事説明会を開催します",
    )

    result = search("通常総会 2026年度", test_user_sophiag)

    assert list(result) == [target]


@pytest.mark.django_db
def test_search_excludes_confidential_file(test_user_sophiag, file_factory):
    """通常ユーザーは機密ファイルを検索できない"""
    target = file_factory(
        title="公開ファイル",
    )
    file_factory(
        title="機密ファイル",
        is_confidential=True,
    )

    result = search("ファイル", test_user_sophiag)

    assert list(result) == [target]


@pytest.mark.django_db
def test_search_excludes_dead_file(test_user_sophiag, file_factory):
    """通常ユーザーはalive=FalseのFileを検索できない"""
    target = file_factory(
        title="公開ファイル",
        alive=True,
    )
    file_factory(
        title="削除済みファイル",
        alive=False,
    )

    result = search("ファイル", test_user_sophiag)

    assert list(result) == [target]


@pytest.mark.django_db
def test_search_staff_can_search_confidential_file(test_staff_user, file_factory):
    """staffは機密ファイルも検索できる"""
    target = file_factory(
        title="機密ファイル",
        is_confidential=True,
    )

    result = search("機密", test_staff_user)

    assert list(result) == [target]


@pytest.mark.django_db
def test_search_staff_can_search_dead_file(test_staff_user, file_factory):
    """staffはalive=FalseのFileも検索できる"""
    target = file_factory(
        title="削除済みファイル",
        alive=False,
    )

    result = search("削除済み", test_staff_user)

    assert list(result) == [target]


@pytest.mark.django_db
def test_search_user_with_add_file_permission(data_manager, file_factory):
    """library.add_file権限を持つユーザーは機密ファイルも検索できる"""
    target = file_factory(
        title="機密ファイル",
        is_confidential=True,
    )

    result = search("機密", data_manager)

    assert list(result) == [target]


# @pytest.fixture
# def staff_user(db):
#     return User.objects.create_user(
#         username="staff_user",
#         password="pass",
#         is_staff=True,
#     )


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

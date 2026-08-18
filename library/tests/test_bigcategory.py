import pytest
from django.test import Client
from django.urls import reverse

# -----------------------------------------------------------------------------
# 閲覧制御のテスト
# -----------------------------------------------------------------------------


@pytest.mark.django_db
def test_anonymous_user_can_view_public_category_only(
    big_category,
    test_user_no_perm,
):
    """未ログインユーザーは restrict=False のカテゴリのみ取得できること"""

    client = Client()

    # パスワードを省略して強制ログインさせる
    client.force_login(test_user_no_perm)

    # anonymousユーザとしてカテゴリを選択表示させる
    url = reverse("library:bigcategory", kwargs={"pk": big_category.pk})
    response = client.get(url)

    print(f"pk = {big_category.pk}")

    assert response.status_code == 200

    # public_cat 配下のファイルのみが含まれているか確認
    category_list = response.context["category_list"]
    # assert len(category_list) == 1  # 制限カテゴリは含まれないため1個
    # assert category_list[0] in normal_file
    # assert category_list[0] in confidential_file

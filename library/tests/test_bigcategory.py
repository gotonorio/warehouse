import pytest

# from django.core.exceptions import PermissionDenied
from django.test import Client
from django.urls import reverse

# -----------------------------------------------------------------------------
# 閲覧制御のテスト
# -----------------------------------------------------------------------------


@pytest.mark.django_db
def test_bigcategory_category_restrict_control(
    big_category,
    category_normal,
    test_user_sophiag,  # ログインユーザー
):
    client = Client()

    # 1. 未ログイン -> category.restrict=FalseのCategoryは表示される
    response = client.get(reverse("library:bigcategory", args=[big_category.pk]))
    assert response.status_code == 200

    # 2. 未ログイン -> restrict=TrueはPermissionDenied
    # rstrict=FalseのCategoryを削除することで、category.restrict=TrueのCategoryだけにしてテストする
    category_normal.delete()
    response = client.get(reverse("library:bigcategory", args=[big_category.pk]))
    assert response.status_code == 403

    # 3. ログインユーザー（view_fileパーミッション保有ユーザー） -> category.restrict=True は閲覧可能
    # file.is_confidentialの制限チェックは test_pdf_view.py で行う
    # client.force_login(test_user_no_perm)
    client.force_login(test_user_sophiag)
    response = client.get(reverse("library:bigcategory", args=[big_category.pk]))
    assert response.status_code == 200

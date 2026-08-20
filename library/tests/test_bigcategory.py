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
    test_user_no_perm,
    # test_user_data_manager,
    # test_group_data_manager,
    # test_permission_view_file,
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

    # 3. ログインユーザー -> category.restrict=True は表示される
    # file.is_confidentialの制限チェックは test_pdf_view.py で行う
    client.force_login(test_user_no_perm)
    response = client.get(reverse("library:bigcategory", args=[big_category.pk]))
    assert response.status_code == 200

    # # 4. data_manager → restrict=True も表示される
    # user_dm = test_user_data_manager
    # user_dm.groups.add(test_group_data_manager)
    # user_dm.user_permissions.add(test_permission_view_file)
    # user_dm.save()

    # client.force_login(user_dm)
    # response = client.get(reverse("library:bigcategory", args=[big_category.pk]))
    # assert response.status_code == 200


# @pytest.mark.django_db
# def test_anonymous_user_can_view_public_category_only(
#     big_category,
#     category_normal,
#     category_restrict,
# ):
#     """未ログインユーザーは restrict=False のカテゴリのみ取得できること"""

#     client = Client()

#     # # パスワードを省略して強制ログインさせる
#     # client.force_login(test_user_no_perm)

#     # 1. anonymousユーザとしてrestrict=Falseのカテゴリを選択させる
#     url = reverse("library:bigcategory", kwargs={"pk": category_normal.pk})
#     response = client.get(url)
#     # restrict=Falseのカテゴリは表示できることを確認
#     assert response.status_code == 200

#     # 2. anonymousユーザとしてrestrict=Trueのカテゴリを選択させる
#     url = reverse("library:bigcategory", kwargs={"pk": category_restrict.pk})
#     response = client.get(url)
#     # restrict=Trueのカテゴリは表示できることを確認
#     # 本番では403を返すが、テスト環境では404が返るようだ
#     assert response.status_code == 404


# @pytest.mark.django_db
# def test_category_access_control(
#     big_category,
#     category_normal,
#     category_restrict,
#     test_user_no_perm,
#     test_user_data_manager,
#     test_user_chairman,
#     test_group_data_manager,
#     test_permission_view_file,
# ):
#     """カテゴリ閲覧制御の総合テスト"""

#     client = Client()

#     # ============================================================
#     # 1. anonymous（未ログイン）
#     # ============================================================
#     # restrict=False → OK
#     response = client.get(reverse("library:bigcategory", args=[category_normal.pk]))
#     assert response.status_code == 200

#     # restrict=True → NG
#     response = client.get(reverse("library:bigcategory", args=[category_restrict.pk]))
#     assert response.status_code == 404

#     # ============================================================
#     # 2. 一般ユーザー（ログイン済み・sophiagグループ）
#     # ============================================================
#     client.force_login(test_user_no_perm)

#     # restrict=False → OK
#     response = client.get(reverse("library:bigcategory", args=[category_normal.pk]))
#     assert response.status_code == 200

#     # restrict=True → NG
#     response = client.get(reverse("library:bigcategory", args=[category_restrict.pk]))
#     assert response.status_code == 404

#     # ============================================================
#     # 3. data_manager（restrict=True を閲覧可能）
#     # ============================================================
#     user_dm = test_user_data_manager
#     user_dm.groups.add(test_group_data_manager)
#     user_dm.user_permissions.add(test_permission_view_file)

#     client.force_login(user_dm)

#     # data_manager → BigCategory 全体を閲覧可能
#     response = client.get(reverse("library:bigcategory", args=[big_category.pk]))
#     assert response.status_code == 200

# # ============================================================
# # 4. chairman（すべて閲覧可能）
# # ============================================================
# client.force_login(test_user_chairman)

# # restrict=False → OK
# response = client.get(reverse("library:bigcategory", args=[category_normal.pk]))
# assert response.status_code == 200

# # restrict=True → OK
# response = client.get(reverse("library:bigcategory", args=[category_restrict.pk]))
# assert response.status_code == 200

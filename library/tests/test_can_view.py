import pytest


# -----------------------------------------------------------------------------
# 閲覧制御のテスト
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_can_view(
    test_user_anonymous,
    test_user_sophiag,
    test_user_data_manager,
    test_user_chairman,
    file_restrict,
    file_normal,
    file_confidential,
):
    """File.can_view()のテスト"""

    # 1. category.restrict = True（区分所有者のみ閲覧可能）のファイル
    assert file_restrict.can_view(test_user_anonymous) is False  # 閲覧拒否
    assert file_restrict.can_view(test_user_sophiag) is True
    assert file_restrict.can_view(test_user_data_manager) is True
    assert file_restrict.can_view(test_user_chairman) is True

    # 2. category.restrict = False（anonymousユーザ閲覧可能）のファイル
    assert file_normal.can_view(test_user_anonymous) is True
    assert file_normal.can_view(test_user_sophiag) is True
    assert file_normal.can_view(test_user_data_manager) is True
    assert file_normal.can_view(test_user_chairman) is True

    # 3. file.is_confidential = True のファイル
    assert file_confidential.can_view(test_user_anonymous) is False
    assert file_confidential.can_view(test_user_sophiag) is False
    assert file_confidential.can_view(test_user_data_manager) is False
    assert file_confidential.can_view(test_user_chairman) is True

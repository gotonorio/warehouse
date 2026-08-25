import pytest
from django.contrib.auth.models import AnonymousUser


# -----------------------------------------------------------------------------
# 閲覧制御のテスト
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_can_view(
    test_user_sophiag,
    test_user_data_manager,
    test_user_chairman,
    file_restrict,
    file_normal,
    file_confidential,
):
    """File.can_view()のテスト"""

    # 1. category.restrict = True（区分所有者のみ閲覧可能）のファイル
    qs = file_restrict.can_view(AnonymousUser())
    assert qs is False  # 閲覧拒否
    qs = file_restrict.can_view(test_user_sophiag)
    assert qs is True
    qs = file_restrict.can_view(test_user_data_manager)
    assert qs is True
    qs = file_restrict.can_view(test_user_chairman)
    assert qs is True

    # 2. category.restrict = False（anonymousユーザ閲覧可能）のファイル
    qs = file_normal.can_view(AnonymousUser())
    assert qs is True
    qs = file_normal.can_view(test_user_sophiag)
    assert qs is True
    qs = file_normal.can_view(test_user_data_manager)
    assert qs is True
    qs = file_normal.can_view(test_user_chairman)
    assert qs is True

    # 3. file.is_confidential = True のファイル
    qs = file_confidential.can_view(AnonymousUser())
    assert qs is False
    qs = file_confidential.can_view(test_user_sophiag)
    assert qs is False
    qs = file_confidential.can_view(test_user_data_manager)
    assert qs is False
    qs = file_confidential.can_view(test_user_chairman)
    assert qs is True

import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory, override_settings
from django.urls import reverse

from library.views import pdf_view

User = get_user_model()


# -----------------------------------------------------------------------------
# 閲覧制御のテスト
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_pdf_view_access_control(
    test_user_no_perm,
    test_user_chairman,
    test_group_data_manager,
    test_permission_view_file,
    file_confidential,
    file_restrict,
):
    """閲覧制御のテスト"""

    from django.test import Client

    client = Client()

    # -------------------------
    # chairman → 全部閲覧可能
    # -------------------------
    client.force_login(test_user_chairman)
    response = client.get(reverse("library:pdf_view", args=[file_confidential.pk]))
    assert response.status_code == 200

    # -------------------------
    # data_manager → restrict 閲覧可能
    # -------------------------
    user_dm = User.objects.create_user(username="dm", password="pass")
    user_dm.groups.add(test_group_data_manager)
    user_dm.user_permissions.add(test_permission_view_file)

    client.force_login(user_dm)
    response = client.get(reverse("library:pdf_view", args=[file_restrict.pk]))
    assert response.status_code == 200

    # -------------------------
    # 一般ユーザー → restrict / confidential 閲覧不可
    # -------------------------
    client.force_login(test_user_no_perm)

    response = client.get(reverse("library:pdf_view", args=[file_confidential.pk]))
    assert response.status_code == 302
    assert response.url == reverse("notice:news_card")

    response = client.get(reverse("library:pdf_view", args=[file_restrict.pk]))
    assert response.status_code == 302
    assert response.url == reverse("notice:news_card")


# -----------------------------------------------------------------------------
# 配信処理のテスト
# -----------------------------------------------------------------------------
@pytest.mark.django_db
@override_settings(DEBUG=True)
def test_pdf_view_debug_mode(file_normal, test_user_chairman):
    """DEBUG=True → FileResponse が返る"""
    rf = RequestFactory()
    req = rf.get("/")
    req.user = test_user_chairman

    response = pdf_view(req, file_normal.pk)

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"
    assert "Content-Disposition" in response


@pytest.mark.django_db
@override_settings(DEBUG=False, MEDIA_URL="/media/")
def test_pdf_view_production_mode(file_normal, test_user_chairman):
    """DEBUG=False → X-Accel-Redirect が付与される"""
    rf = RequestFactory()
    req = rf.get("/")
    req.user = test_user_chairman

    response = pdf_view(req, file_normal.pk)

    assert response.status_code == 200
    assert "X-Accel-Redirect" in response
    assert response["Content-Type"] == "application/pdf"

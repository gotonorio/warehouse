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
    test_user_sophiag,
    test_user_data_manager,
    test_user_chairman,
    file_confidential,
    file_restrict,
):
    """閲覧制御のテスト"""

    from django.test import Client

    client = Client()

    # -------------------------
    # 未ログインユーザ → restrict 閲覧不可
    # 未ログインユーザ → confidential 閲覧不可
    # -------------------------
    response = client.get(reverse("library:pdf_view", args=[file_restrict.pk]))
    assert response.status_code == 403
    response = client.get(reverse("library:pdf_view", args=[file_confidential.pk]))
    assert response.status_code == 403

    # -------------------------
    # chairman → 全部閲覧可能
    # -------------------------
    client.force_login(test_user_chairman)
    response = client.get(reverse("library:pdf_view", args=[file_confidential.pk]))
    assert response.status_code == 200

    # -------------------------
    # data_manager → 全部閲覧可能
    # -------------------------
    client.force_login(test_user_data_manager)
    response = client.get(reverse("library:pdf_view", args=[file_confidential.pk]))
    assert response.status_code == 200

    # -------------------------
    # sophiag → restrict 閲覧可能
    # sophiag → confidential 閲覧不可
    # -------------------------
    client.force_login(test_user_sophiag)

    response = client.get(reverse("library:pdf_view", args=[file_restrict.pk]))
    assert response.status_code == 200
    response = client.get(reverse("library:pdf_view", args=[file_confidential.pk]))
    assert response.status_code == 403


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

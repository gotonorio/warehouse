import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory, override_settings

from library.views import pdf_view

User = get_user_model()


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

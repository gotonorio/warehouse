import pytest
from django.test import Client
from django.urls import reverse


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

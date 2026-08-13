import tempfile

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages
from django.db.models import ProtectedError
from django.test import TestCase, override_settings
from django.urls import reverse

# BigCategoryモデルは実際のプロジェクトのインポートパスに合わせて変更してください
from library.models import BigCategory, Category

User = get_user_model()

# テスト実行時のみ使用する一時メディアディレクトリ
TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT, AXES_ENABLED=False)
class CategoryViewTests(TestCase):
    def setUp(self):
        # 1. テストユーザーの作成
        self.user_with_perm = User.objects.create_user(username="admin_user", password="password123")
        self.user_without_perm = User.objects.create_user(username="normal_user", password="password123")

        # 2. 権限(library.add_file)の付与
        # ※ ContentTypeのapp_labelやmodelは環境に合わせて調整してください
        content_type = ContentType.objects.get_for_model(Category)
        permission, _ = Permission.objects.get_or_create(
            codename="add_file",
            content_type=content_type,
        )
        self.user_with_perm.user_permissions.add(permission)

        # 3. テストデータの準備
        self.big_category_1 = BigCategory.objects.create(name="親カテゴリ1", rank=1)
        self.big_category_2 = BigCategory.objects.create(name="親カテゴリ2", rank=2)

        self.category_1 = Category.objects.create(
            name="カテゴリ1",
            path_name="cat1",
            parent=self.big_category_1,
            rank=10,
            alive=True,
        )
        self.category_2 = Category.objects.create(
            name="カテゴリ2",
            path_name="cat2",
            parent=self.big_category_2,
            rank=5,
            alive=False,
        )

    # ------------------------------------------------------------------
    # 権限チェック (PermissionRequiredMixin)
    # ------------------------------------------------------------------
    def test_permission_required(self):
        """権限がない場合、403 Forbidden が返されることを確認."""
        # 未ログイン時
        response = self.client.get(reverse("library:category_index"))
        self.assertEqual(response.status_code, 403)

        # 権限のないユーザーでログイン時
        self.client.login(username="normal_user", password="password123")
        response = self.client.get(reverse("library:category_index"))
        self.assertEqual(response.status_code, 403)

    # ------------------------------------------------------------------
    # CategoryIndexView
    # ------------------------------------------------------------------
    def test_category_index_view_get(self):
        """一覧画面が正常に表示され、正しいソート順で取得できるか."""
        self.client.login(username="admin_user", password="password123")
        response = self.client.get(reverse("library:category_index"))

        self.assertEqual(response.status_code, 200)
        # alive（True -> False）の順で取得されているか確認
        object_list = list(response.context["object_list"])
        self.assertEqual(object_list, [self.category_1, self.category_2])

    # ------------------------------------------------------------------
    # CategoryBigView
    # ------------------------------------------------------------------
    def test_category_big_view_get(self):
        """親カテゴリIDでフィルタリングされ、contextにbig_pkが含まれるか."""
        self.client.login(username="admin_user", password="password123")
        url = reverse("library:category_big", kwargs={"big_pk": self.big_category_1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["big_pk"], self.big_category_1.pk)

        # 該当する親カテゴリに紐づくデータのみ含まれているか
        object_list = list(response.context["object_list"])
        self.assertIn(self.category_1, object_list)
        self.assertNotIn(self.category_2, object_list)

    # ------------------------------------------------------------------
    # CategoryCreateView
    # ------------------------------------------------------------------
    def test_category_create_view_initial(self):
        """URLのpkパラメータから親カテゴリの初期値がセットされるか."""
        self.client.login(username="admin_user", password="password123")
        url = reverse("library:category_create", kwargs={"pk": self.big_category_1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].initial.get("parent"), self.big_category_1.pk)

    def test_category_create_view_post_success(self):
        """作成処理が成功してリダイレクトされるか."""
        self.client.login(username="admin_user", password="password123")
        post_data = {
            "name": "新規カテゴリ",
            "path_name": "new_cat",
            "parent": self.big_category_1.pk,
            "rank": 0,
            "restrict": False,
            "alive": True,
        }
        response = self.client.post(reverse("library:category_create"), data=post_data)

        self.assertRedirects(response, reverse("library:category_index"))
        self.assertTrue(Category.objects.filter(name="新規カテゴリ").exists())

    # ------------------------------------------------------------------
    # CategoryUpdateView
    # ------------------------------------------------------------------
    def test_category_update_view_post_success(self):
        """更新処理が成功するか."""
        self.client.login(username="admin_user", password="password123")
        url = reverse("library:category_update", kwargs={"pk": self.category_1.pk})
        post_data = {
            "name": "更新後のカテゴリ名",
            "path_name": "cat1",
            "parent": self.big_category_1.pk,
            "rank": 99,
            "restrict": True,
            "alive": True,
        }
        response = self.client.post(url, data=post_data)

        self.assertRedirects(response, reverse("library:category_index"))
        self.category_1.refresh_from_db()
        self.assertEqual(self.category_1.name, "更新後のカテゴリ名")
        self.assertEqual(self.category_1.rank, 99)

    # ------------------------------------------------------------------
    # CategoryDeleteView
    # ------------------------------------------------------------------
    def test_category_delete_view_post_success(self):
        """削除処理が成功し、メッセージが設定されるか."""
        self.client.login(username="admin_user", password="password123")
        url = reverse("library:category_delete", kwargs={"pk": self.category_1.pk})
        response = self.client.post(url)

        self.assertRedirects(response, reverse("library:category_index"))
        self.assertFalse(Category.objects.filter(pk=self.category_1.pk).exists())

        # successメッセージの検証
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn("を削除しました。", str(messages_list[0]))

    def test_category_delete_view_post_protected_error(self):
        """ProtectedError発生時に削除されず、errorメッセージが表示されるか."""
        self.client.login(username="admin_user", password="password123")
        url = reverse("library:category_delete", kwargs={"pk": self.category_1.pk})

        # Category.delete() が呼び出された時に ProtectedError を送出するようにモック化/シミュレート
        dummy_protected_obj = "紐づくファイル.pdf"
        error = ProtectedError("Protected relation", [dummy_protected_obj])

        from unittest.mock import patch

        with patch.object(Category, "delete", side_effect=error):
            response = self.client.post(url)

        # リダイレクトされることと、削除されていないことを確認
        self.assertRedirects(response, reverse("library:category_index"))
        self.assertTrue(Category.objects.filter(pk=self.category_1.pk).exists())

        # errorメッセージの検証
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn("先に次のファイルを削除してください", str(messages_list[0]))
        self.assertIn(dummy_protected_obj, str(messages_list[0]))

# from unittest.mock import patch
from django.contrib.auth import get_user_model  # ← 追加
from django.contrib.auth.models import Permission

# from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

# プロジェクトの構成に合わせてインポートパスを調整してください
from library.models import BigCategory, Category, File
from library.views import BigCategoryView

User = get_user_model()  # カスタムユーザーモデルを取得


class BigCategoryViewTests(TestCase):
    def setUp(self):
        # 1. 親カテゴリの作成
        self.big_category = BigCategory.objects.create(name="親カテゴリA", rank=1, alive=True)

        # 2. 子カテゴリの作成（公開 / 制限付き）
        self.public_cat = Category.objects.create(
            name="公開カテゴリ",
            path_name="public_category",  # ← 追加
            parent=self.big_category,
            alive=True,
            restrict=False,
            rank=2,
        )
        self.restricted_cat = Category.objects.create(
            name="制限カテゴリ",
            path_name="restricted_category",  # ← 追加（重複しない値）
            parent=self.big_category,
            alive=True,
            restrict=True,
            rank=1,
        )

        # 3. ファイルの作成（通常 / 機密）
        self.normal_file = File.objects.create(
            title="一般ファイル",
            category=self.public_cat,
            alive=True,
            is_confidential=False,
            rank=1,
        )
        self.confidential_file = File.objects.create(
            title="機密ファイル",
            category=self.public_cat,
            alive=True,
            is_confidential=True,
            rank=2,
        )

        # 4. ユーザーの作成
        self.user = User.objects.create_user(username="normal_user", password="password")
        self.admin_user = User.objects.create_user(username="admin_user", password="password")

        # 権限の付与 (library.add_file)
        add_file_perm = Permission.objects.get(codename="add_file", content_type__app_label="library")
        self.admin_user.user_permissions.add(add_file_perm)

        self.factory = RequestFactory()

    @override_settings(SELECT_LIMIT_NUM=5, COMMENT_LIMIT=2)
    def test_anonymous_user_can_view_public_category_only(self):
        """未ログインユーザーは restrict=False のカテゴリのみ取得でき、機密ファイルは除外されること"""
        url = reverse(
            "library:bigcategory", kwargs={"pk": self.big_category.pk}
        )  # URL名はプロジェクトに合わせて調整
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # public_cat 配下のファイルのみが含まれているか確認
        category_list = response.context["category_list"]
        self.assertEqual(len(category_list), 1)  # 制限カテゴリは含まれないため1個
        self.assertIn(self.normal_file, category_list[0])
        self.assertNotIn(self.confidential_file, category_list[0])

    def test_anonymous_user_permission_denied_if_no_public_category(self):
        """未ログイン時に公開カテゴリが存在しない場合、PermissionDenied(403)が発生すること"""
        # 公開カテゴリを無効化
        self.public_cat.alive = False
        self.public_cat.save()

        url = reverse("library:bigcategory", kwargs={"pk": self.big_category.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    @override_settings(SELECT_LIMIT_NUM=5, COMMENT_LIMIT=2)
    def test_authenticated_user_without_perm_cannot_see_confidential_files(self):
        """権限を持たないログインユーザーは、機密ファイルが表示されないこと"""
        self.client.force_login(self.user)
        url = reverse("library:bigcategory", kwargs={"pk": self.big_category.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # 制限カテゴリも取得されるため2つ
        category_list = response.context["category_list"]
        self.assertEqual(len(category_list), 2)

        # 公開カテゴリ配下のファイル一覧を取得
        public_files = category_list[0]
        self.assertIn(self.normal_file, public_files)
        self.assertNotIn(self.confidential_file, public_files)

    @override_settings(SELECT_LIMIT_NUM=5, COMMENT_LIMIT=2)
    def test_user_with_add_perm_can_see_confidential_files(self):
        """add_file権限を持つユーザーは、機密ファイルも表示されること"""
        self.client.force_login(self.admin_user)
        url = reverse("library:bigcategory", kwargs={"pk": self.big_category.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        category_list = response.context["category_list"]
        public_files = category_list[0]

        self.assertIn(self.normal_file, public_files)
        self.assertIn(self.confidential_file, public_files)

    @override_settings(SELECT_LIMIT_NUM=1, COMMENT_LIMIT=2)
    def test_file_limit_is_applied(self):
        """settings.SELECT_LIMIT_NUM の制限数が適用されること"""
        # さらにファイルを追加
        File.objects.create(
            title="一般ファイル2",
            category=self.public_cat,
            alive=True,
            is_confidential=False,
            rank=3,
        )

        self.client.force_login(self.user)
        url = reverse("library:bigcategory", kwargs={"pk": self.big_category.pk})
        response = self.client.get(url)

        category_list = response.context["category_list"]
        # SELECT_LIMIT_NUM=1 の設定のため、ファイルは1件のみ取得されること
        self.assertEqual(len(category_list[0]), 1)

    def test_mobile_user_agent_returns_mobile_template(self):
        """モバイル端末の場合、モバイル用テンプレートが使用されること"""
        view = BigCategoryView()
        request = self.factory.get("/")

        # user_agent の モック (django-user-agents想定)
        request.user_agent = type("UserAgent", (), {"is_mobile": True})()
        view.request = request

        templates = view.get_template_names()
        self.assertEqual(templates, ["library/main_category_mobile.html"])

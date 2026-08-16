from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from library.models import BigCategory, Category, File

User = get_user_model()


class PdfViewTest(TestCase):
    def setUp(self):
        # グループ作成
        self.chairman = Group.objects.create(name="chairman")
        self.data_manager = Group.objects.create(name="data_manager")

        # パーミッション取得
        perm = Permission.objects.get(codename="view_file")

        # chairmanユーザー
        self.user_chairman = User.objects.create_user(username="chairman", password="pass")
        self.user_chairman.groups.add(self.chairman)
        self.user_chairman.user_permissions.add(perm)

        # data_managerユーザー
        self.user_dm = User.objects.create_user(username="dm", password="pass")
        self.user_dm.groups.add(self.data_manager)
        self.user_dm.user_permissions.add(perm)

        # 一般ユーザー（restrict不可）
        self.user_normal = User.objects.create_user(username="normal", password="pass")
        self.user_normal.user_permissions.add(perm)

        # パーミッションなしユーザー
        self.user_no_perm = User.objects.create_user(username="noperm", password="pass")

        # カテゴリ作成
        self.big = BigCategory.objects.create(name="big")
        self.cat_normal = Category.objects.create(
            name="cat1", path_name="cat1", parent=self.big, restrict=False
        )
        self.cat_restrict = Category.objects.create(
            name="cat2", path_name="cat2", parent=self.big, restrict=True
        )

        # テスト用ファイル
        self.test_file = SimpleUploadedFile(
            "test.pdf", b"%PDF-1.4 test content", content_type="application/pdf"
        )

        # 通常ファイル
        self.file_normal = File.objects.create(
            title="normal",
            category=self.cat_normal,
            src=self.test_file,
            is_confidential=False,
        )

        # restrictカテゴリのファイル
        self.file_restrict = File.objects.create(
            title="restrict",
            category=self.cat_restrict,
            src=self.test_file,
            is_confidential=False,
        )

        # confidentialファイル
        self.file_confidential = File.objects.create(
            title="secret",
            category=self.cat_normal,
            src=self.test_file,
            is_confidential=True,
        )

        self.client = Client()

    # ---------------------------------------------------------
    # パーミッションテスト
    # ---------------------------------------------------------
    def test_permission_required(self):
        """パーミッションがないユーザーは403"""
        self.client.force_login(self.user_no_perm)

        url = reverse("library:file_view", args=[self.file_normal.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    # ---------------------------------------------------------
    # chairman はすべて閲覧可能
    # ---------------------------------------------------------
    @override_settings(DEBUG=True)
    def test_chairman_can_view_all(self):
        self.client.force_login(self.user_chairman)

        for f in [self.file_normal, self.file_restrict, self.file_confidential]:
            url = reverse("library:file_view", args=[f.pk])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn("Content-Disposition", response)

    # ---------------------------------------------------------
    # data_manager は restrictカテゴリ閲覧可能
    # ---------------------------------------------------------
    @override_settings(DEBUG=True)
    def test_data_manager_can_view_restrict(self):
        self.client.force_login(self.user_dm)

        url = reverse("library:file_view", args=[self.file_restrict.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # ---------------------------------------------------------
    # 一般ユーザーは restrictカテゴリ閲覧不可 → リダイレクト
    # ---------------------------------------------------------
    def test_normal_user_cannot_view_restrict(self):
        self.client.force_login(self.user_normal)

        url = reverse("library:file_view", args=[self.file_restrict.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("notice:news_card"))

    # ---------------------------------------------------------
    # 一般ユーザーは confidential 閲覧不可 → リダイレクト
    # ---------------------------------------------------------
    def test_normal_user_cannot_view_confidential(self):
        self.client.force_login(self.user_normal)

        url = reverse("library:file_view", args=[self.file_confidential.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("notice:news_card"))

    # ---------------------------------------------------------
    # DEBUG=True の場合 FileResponse が返る
    # ---------------------------------------------------------
    @override_settings(DEBUG=True)
    def test_debug_returns_fileresponse(self):
        self.client.force_login(self.user_dm)

        url = reverse("library:file_view", args=[self.file_normal.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    # ---------------------------------------------------------
    # DEBUG=False の場合 X-Accel-Redirect が付与される
    # ---------------------------------------------------------
    @override_settings(DEBUG=False)
    def test_production_returns_accel_redirect(self):
        self.client.force_login(self.user_dm)

        url = reverse("library:file_view", args=[self.file_normal.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("X-Accel-Redirect", response)

# テスト観点	確認内容
# 1. ファイルの保存確認	指定したファイルが設定されたディレクトリ（upload_to）に実際に生成されているか
# 2. 保存パスの確認	動的パス（カテゴリ名など）が正しく適用され、期待通りのファイルパスになっているか
# 3. DBレコードの確認	FileField に正しいパス情報が記録され、他のメタデータ（タイトルやカテゴリ）も保存されているか
# 4. ビューの動作確認	POSTリクエストでファイルを送信した際、正常にレスポンス（302リダイレクト等）が返るか
# 5. 境界値・例外系	カテゴリが存在しない場合や、同名ファイルがアップロードされた際に正常に処理（リネーム等）されるか
# 6. DBレコードの削除確認: File.objects.filter(pk=...).exists() が False になるか
# 7. 物理ファイルの削除確認 (django-cleanup の動作検証): ディスク上の実ファイルが消えているか
# 8. リダイレクト・メッセージの検証: 処理完了後に正しい画面へ遷移するか

import shutil
import tempfile
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import BigCategory, Category, File

User = get_user_model()

# テスト実行時のみ使用する一時メディアディレクトリ
TEMP_MEDIA_ROOT = tempfile.mkdtemp()


# テスト環境の保護、認証・セキュリティ: django-axes 回避と force_login()
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT, AXES_ENABLED=False)
class FileUploadTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """テスト用共通データの作成 (BigCategory -> Category の順で作成)"""
        # 1. 管理者ユーザー
        cls.user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password123"
        )

        # 2. 親カテゴリ (BigCategory) の作成
        cls.big_category = BigCategory.objects.create(name="業務マニュアル")

        # 3. 子カテゴリ (Category) の作成 (BigCategory を parent に渡す)
        cls.category = Category.objects.create(
            name="経理",
            path_name="accounting",  # upload_to で使用されるディレクトリ名
            parent=cls.big_category,  # <- これがないと IntegrityError になります
        )

    @classmethod
    def tearDownClass(cls):
        """テスト終了後に一時フォルダをクリーンアップ"""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        """login() の代わりに force_login() を使用"""
        self.client.force_login(self.user)

    def test_upload_file_via_view(self):
        """ビュー経由でファイルがアップロードされ、動的パス(accounting/)へ保存されるか"""
        url = reverse("library:file_create", kwargs={"pk": self.category.pk})

        # 1. メモリ上にダミーファイルを生成
        dummy_file = SimpleUploadedFile(
            "test_document.pdf", b"file_binary_content", content_type="application/pdf"
        )

        # 2. POSTデータ (rank を追加)
        post_data = {
            "title": "経理マニュアル2026",
            "category": self.category.pk,
            "src": dummy_file,
            "rank": 0,  # <- 必須フィールドの rank を追加
            "action": "send",
        }

        # 3. リクエスト送信 (follow=False でリダイレクト発生を確認)
        response = self.client.post(url, post_data)

        # 4. 成功リダイレクト (302 Found) の確認
        self.assertEqual(response.status_code, 302)

        # 5. DBに保存されたか確認
        self.assertTrue(File.objects.filter(title="経理マニュアル2026").exists())
        saved_file = File.objects.get(title="経理マニュアル2026")

        # 6. 保存パスの確認 (accounting/test_document.pdf になっているか)
        expected_path = f"accounting/{dummy_file.name}"
        self.assertEqual(saved_file.src.name, expected_path)

        # 7. 物理ファイルがディスク上に存在するか確認
        full_path = Path(saved_file.src.path)
        self.assertTrue(full_path.exists())

    def test_get_filename_method(self):
        """Fileモデルの get_filename メソッドがファイル名のみを返すか"""
        dummy_file = SimpleUploadedFile("sample.txt", b"hello")

        file_obj = File.objects.create(title="サンプル", category=self.category, src=dummy_file)

        # 階層パスが含まれず "sample.txt" のみが返るか
        self.assertEqual(file_obj.get_filename(), "sample.txt")

    def test_duplicate_filename_upload(self):
        """同名ファイルがアップロードされた場合、Djangoが自動的にリネームして保存するか"""
        url = reverse("library:file_create", kwargs={"pk": self.category.pk})

        # 1回目のアップロード (ファイル名: duplicate.pdf)
        file1 = SimpleUploadedFile("duplicate.pdf", b"first_file_content", content_type="application/pdf")
        post_data1 = {
            "title": "1回目のファイル",
            "category": self.category.pk,
            "src": file1,
            "rank": 0,
            "action": "send",
        }
        res1 = self.client.post(url, post_data1)
        self.assertEqual(res1.status_code, 302)

        # 2回目のアップロード (まったく同じファイル名: duplicate.pdf)
        file2 = SimpleUploadedFile("duplicate.pdf", b"second_file_content", content_type="application/pdf")
        post_data2 = {
            "title": "2回目のファイル",
            "category": self.category.pk,
            "src": file2,
            "rank": 0,
            "action": "send",
        }
        res2 = self.client.post(url, post_data2)
        self.assertEqual(res2.status_code, 302)

        # DBからそれぞれのオブジェクトを取得
        obj1 = File.objects.get(title="1回目のファイル")
        obj2 = File.objects.get(title="2回目のファイル")

        # 1. パスの確認: 1つ目は元の指定通りの名前
        self.assertEqual(obj1.src.name, "accounting/duplicate.pdf")

        # 2. リネーム確認: 2つ目のファイルパスは 1つ目と異なる名前に自動変更されているか
        self.assertNotEqual(obj1.src.name, obj2.src.name)
        # 例: accounting/duplicate_a1b2c3d.pdf のように接頭辞と拡張子が維持されているか
        self.assertTrue(obj2.src.name.startswith("accounting/duplicate"))
        self.assertTrue(obj2.src.name.endswith(".pdf"))

        # 3. 物理ファイルの存在確認: 2つのファイルがディスク上に独立して存在しているか
        path1 = Path(obj1.src.path)
        path2 = Path(obj2.src.path)
        self.assertTrue(path1.exists())
        self.assertTrue(path2.exists())
        self.assertNotEqual(path1, path2)

        # 4. 中身の検証: 1回目のファイルが2回目のアップロードで上書きされていないか
        with open(path1, "rb") as f:
            self.assertEqual(f.read(), b"first_file_content")
        with open(path2, "rb") as f:
            self.assertEqual(f.read(), b"second_file_content")

    def test_delete_file_via_view(self):
        """【削除テスト】ビュー経由でファイル削除時、DBと実ファイル(django-cleanup)が両方削除されるか"""
        # 1. テスト用のファイルを1件作成
        dummy_file = SimpleUploadedFile(
            "delete_target.pdf", b"data_to_be_deleted", content_type="application/pdf"
        )
        file_obj = File.objects.create(title="削除用ファイル", category=self.category, src=dummy_file, rank=1)
        file_pk = file_obj.pk
        file_path = Path(file_obj.src.path)

        # 削除前の存在確認
        self.assertTrue(File.objects.filter(pk=file_pk).exists())
        self.assertTrue(file_path.exists())

        delete_url = reverse("library:file_delete", kwargs={"pk": file_pk})

        # コミット時に実行される予定だった処理（＝コールバック）を横取りして、
        # django-cleanup の transaction.on_commit イベントを強制実行させる
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(delete_url)

        # 2. 成功リダイレクト (302) の確認
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("library:file_index"))

        # 3. DBからレコードが削除されているか確認
        self.assertFalse(File.objects.filter(pk=file_pk).exists())

        # 4. 【django-cleanup検証】物理ファイルがディスクから消えているか確認
        self.assertFalse(file_path.exists())

    def test_delete_file_permission_denied(self):
        """【権限テスト】権限を持たない一般ユーザーはファイル削除が拒否(403)されるか"""
        # 1. 権限を持たない一般ユーザーを作成してログイン
        normal_user = User.objects.create_user(username="normal_user", password="password123")
        self.client.force_login(normal_user)

        # 2. テスト用ファイルの作成
        dummy_file = SimpleUploadedFile("noperm.pdf", b"data", content_type="application/pdf")
        file_obj = File.objects.create(title="権限テスト用ファイル", category=self.category, src=dummy_file)

        delete_url = reverse("library:file_delete", kwargs={"pk": file_obj.pk})

        # 3. POSTリクエストを送信すると Forbidden (403) になるか
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 403)

        # 4. DBおよびファイルが削除されずに残っているか確認
        self.assertTrue(File.objects.filter(pk=file_obj.pk).exists())
        self.assertTrue(Path(file_obj.src.path).exists())

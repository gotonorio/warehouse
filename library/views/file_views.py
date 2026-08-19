import logging
import mimetypes
import os
import urllib.parse

from django.conf import settings

# from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic

from library.models import File

logger = logging.getLogger(__name__)


class FileIndexView(PermissionRequiredMixin, generic.ListView):
    """管理者用 ファイル一覧"""

    model = File
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = False  # ログイン画面に飛ばす。
    # paginate_by = 50

    def get_queryset(self):
        return File.objects.order_by("-alive", "category", "rank")


class FileCategoryView(PermissionRequiredMixin, generic.ListView):
    """管理者用 カテゴリ別のファイル一覧"""

    model = File
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    # pagingを止める
    # paginate_by = 20

    def get_queryset(self):
        """カテゴリでfilter."""
        category_pk = self.kwargs["category_pk"]
        return File.objects.filter(category__pk=category_pk).order_by("-alive", "is_confidential", "-rank")

    def get_context_data(self, *args, **kwargs):
        """カテゴリのpkをテンプレートへ渡す."""
        context = super().get_context_data(*args, **kwargs)
        context["category_pk"] = self.kwargs.get("category_pk")
        return context


# ファイル閲覧はanonymousユーザーにも許可する場合があるので、関数全体での閲覧制御は行わない
# # グループ名による閲覧制御（最低限view_fileパーミッションを持つ必要がある）
# @permission_required("library.view_file", raise_exception=True)
def pdf_view(request, pk):
    """ファイル配信処理
    - ローカル環境：Djangoが FileResponse で直接ファイルを配信する。
    - 本番環境：  nginxが HttpResponse で配信することで、nginxの設定（internal）で
                外部からのURL直打ちを防止できる。
    """
    fn = get_object_or_404(File, pk=pk)

    # ログインユーザのグループ名を取得する
    groups = set(request.user.groups.values_list("name", flat=True))

    # グループと「カテゴリ権限」「ファイル権限」による閲覧制御
    if "chairman" not in groups:
        # 機密ファイルはchairmanグループ以外閲覧禁止
        if fn.is_confidential:
            raise PermissionDenied()
        # 未ログインユーザはrestrict=Trueのカテゴリのファイル閲覧禁止
        if groups is None and fn.category.restrict:
            raise PermissionDenied()

    # 配信するファイル名
    filename = os.path.basename(fn.src.name)
    # ファイル名のエンコード
    quoted = urllib.parse.quote(filename)

    # ファイル名から MIME タイプを推測 (例: 'application/zip', 'application/pdf')
    # fn.src.name が "example.zip" なら 'application/zip' が返る
    content_type, _ = mimetypes.guess_type(fn.src.name)
    # 判別できない場合は、一般的なバイナリ形式 'application/octet-stream' をデフォルトにする
    content_type = content_type or "application/octet-stream"

    # 環境による分岐
    if settings.DEBUG:
        # ローカル環境：Djangoが FileResponse で直接ファイルを配信する
        response = FileResponse(fn.src)
    else:
        # 本番環境：nginxが HttpResponse で配信する
        # パスを作成する。"/media/" + "path/to/file.pdf"
        # fn.src は FileField なので str(fn.src) で相対パスが取れる
        raw_path = os.path.join(settings.MEDIA_URL, str(fn.src))

        # パスをURLエンコードする。スラッシュ '/' までエンコードされないように safe='/' を指定する
        # Nginx（HTTPヘッダー）は本来ASCII文字しか想定していないため。
        protected_path = urllib.parse.quote(raw_path, safe="/")

        response = HttpResponse()
        # 本番環境ではnginxによるリダイレクト
        response["X-Accel-Redirect"] = protected_path

    # 共通ヘッダーのセット
    # 日本語ファイル名に対応するため RFC 6266 (filename*) を使用する。
    # 古いブラウザ向けの filename= は付与しない。
    response["Content-Type"] = content_type
    disposition = "attachment" if fn.download else "inline"
    response["Content-Disposition"] = f"{disposition}; filename*=UTF-8''{quoted}"

    return response

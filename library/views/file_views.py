import logging
import mimetypes
import os
import urllib.parse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from library.forms import FileForm
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


class FileCreateView(PermissionRequiredMixin, generic.CreateView):
    """管理者用 ファイルの作成."""

    model = File
    form_class = FileForm
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:file_index")

    def get_initial(self):
        """カテゴリの指定があれば、そのカテゴリを選択状態に."""
        initial = super().get_initial()
        initial["category"] = self.kwargs.get("pk")
        return initial

    def form_valid(self, form):
        file = form.save()
        action = self.request.POST["action"]
        # file登録のログを記録する。
        file_name = form.cleaned_data["src"]
        logger.info(f"create {file_name} by {self.request.user}")
        # 保存してもう一つ追加ボタンのとき
        if action == "send_more":
            return redirect("library:file_create", file.category.pk)
        # それ以外、送信ボタン
        else:
            return redirect("library:file_index")


class FileUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """管理者用 ファイルの更新."""

    model = File
    form_class = FileForm
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:file_index")

    def form_valid(self, form):
        file = form.save()
        action = self.request.POST["action"]
        # fileアップデートのログを記録する。
        file_name = form.cleaned_data["src"]
        logger.warning(f"update {file_name} by {self.request.user}")

        # 保存してもう一つ追加ボタンのとき
        if action == "send_more":
            return redirect("library:file_create", file.category.pk)
        # それ以外、送信ボタン
        else:
            return redirect("library:file_index")


class FileDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """管理者用 ファイルの削除."""

    template_name = "library/file_confirm_delete.html"
    model = File
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:file_index")

    def post(self, request, *args, **kwargs):
        """ファイルs削除処理を自前で処理する"""

        self.object = self.get_object()
        try:
            self.object.delete()
            logger.warning(f"delete {self.object} by {request.user}")
            messages.success(request, f"{self.object}を削除しました。")
        except models.ProtectedError as e:
            messages.error(request, f"fファイル削除に失敗しました{e}」")
        return redirect(self.get_success_url())


def pdf_view(request, pk):
    """ファイル配信処理
    - ローカル環境：Djangoが FileResponse で直接ファイルを配信する。
    - 本番環境：  nginxが HttpResponse で配信することで、nginxの設定（internal）で
                外部からのURL直打ちを防止できる。
    """
    fn = get_object_or_404(File, pk=pk)

    # 権限チェック
    if fn.category.restrict and not request.user.is_active:
        return redirect("notice:news_card")

    # 配信するファイル名
    filename = urllib.parse.quote(os.path.basename(fn.src.name))

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
        response["X-Accel-Redirect"] = protected_path

    # 共通ヘッダーのセット
    response["Content-Type"] = content_type
    if fn.download:
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
    else:
        response["Content-Disposition"] = f'inline; filename="{filename}"'

    return response


# FileResponse をそのまま返すと Django がファイルを読み込んで配信するが効率が非常に悪い。
# X-Accel-Redirect ヘッダーを返すことで、配信業務を Nginx にバトンタッチできる。
# nginxの設定
# /media/ への外部からの直接アクセスを禁止し、内部からのリクエスト（Djangoからの指示）のみ許可する設定に変更。
# location /media/ {
#    # internalを指定することで、ブラウザからの直接アクセス(URL叩き)を404にする
#    internal;
#    alias /code_warehouse/media/;
# }
#
# def pdf_view(request, pk):
#     """静的ファイル（PDFファイル）の閲覧処理
#     - 効率的には下記のようにwebサーバが静的ファイルを配信するが、urlをコピーするとログインせずに表示できてしまう。
#     - <a href="{{file.src.url}}" target="_blank" rel="noopener noreferrer" download>{{file.title}}</a>
#     - セキュリティを重視するため下記のように配信用の関数を使う。
#     - <a href="{% url 'library:file_view' file.pk %}" target="_blank">{{file.title}}</a>
#     """
#     fn = get_object_or_404(File, pk=pk)
#     if fn.category.restrict:
#         if request.user.is_active:
#             if fn.download:
#                 return FileResponse(fn.src, as_attachment=True)
#             else:
#                 return FileResponse(fn.src)
#         else:
#             # @login_required制限をはずすと、ログインしない場合に下記を実行する。
#             # ログイン画面に戻す場合は@login_requiredをセットする。
#             # メイン画面に戻す場合は@login_requiredを外す。
#             return redirect("notice:news_card")
#     else:
#         if fn.download:
#             return FileResponse(fn.src, as_attachment=True)
#         else:
#             return FileResponse(fn.src)

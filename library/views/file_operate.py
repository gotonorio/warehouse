import logging

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from library.forms import FileForm
from library.models import File

logger = logging.getLogger(__name__)


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
        # 1. DBへ保存（ファイルも指定パスへ自動保存される）
        file = form.save()
        # 2. 安全に POST パラメータを取得 (KeyError防止)
        action = self.request.POST.get("action", "")
        # 3. file登録のログを記録する。（srcは必ず指定されるのでgetは不要）
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
        # 1. DBへ保存（ファイルも指定パスへ自動保存される）
        file = form.save()
        # 2. 安全に POST パラメータを取得 (KeyError防止)
        action = self.request.POST.get("action", "")
        # 3. file登録のログを記録する。（srcは必ず指定されるのでgetは不要）
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
    # 💡 ポイント1: 権限名の確認
    # 必要な権限
    permission_required = "library.delete_file"
    raise_exception = True
    success_url = reverse_lazy("library:file_index")

    def post(self, request, *args, **kwargs):
        """ファイル削除処理を自前で処理する"""
        self.object = self.get_object()

        # 削除前にログ・メッセージ用の文字列を取得しておく
        target_name = str(self.object)

        try:
            # django-cleanupが有効なため、.delete() 時に物理ファイルも自動削除される
            self.object.delete()
            logger.warning(f"delete {target_name} by {request.user}")
            messages.success(request, f"{target_name}を削除しました。")
        except models.ProtectedError as e:
            logger.error(f"Failed to delete {target_name}: {e}")
            messages.error(
                request, f"ファイル「{target_name}」の削除に失敗しました（他のデータから参照されています）。"
            )

        return redirect(self.get_success_url())

import datetime
import os
import shutil

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from control.forms import UpdateControlForm
from control.models import ControlRecord


class ControlRecordListView(PermissionRequiredMixin, generic.ListView):
    model = ControlRecord
    template_name = "control/control_list.html"
    permission_required = "register.add_user"


class ControlRecordUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """コントロールデータのアップデート"""

    model = ControlRecord
    form_class = UpdateControlForm
    template_name = "control/control_form.html"
    permission_required = "register.add_user"
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy("notice:news_card")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "コントロールデータの修正"
        return context


def backupDB(request):
    """DBのバックアップ処理"""
    try:
        now = datetime.datetime.now()

        src_file = "./wh2.sqlite3"
        backup_dir = "./backup"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # 認証されているユーザーかチェック
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = "anonymous"

        # ファイル名に使用できるように一部文字を置換（/ や \ など）
        safe_username = username.replace("/", "_").replace("\\", "_")

        dst_file = os.path.join(backup_dir, f"{now.strftime('%Y-%m-%d')}-{safe_username}.sqlite3")

        # 元DBファイルが存在するか確認
        if not os.path.exists(src_file):
            messages.error(request, f"バックアップ元のDBファイルが見つかりません: {src_file}")
            return redirect("notice:news_card")

        # コピー実行
        shutil.copy(src_file, dst_file)
        messages.info(request, f"DBをバックアップしました。 ファイル名: {dst_file}")

        # バックアップファイルの一覧取得
        file_list = [
            f
            for f in os.listdir(backup_dir)
            if f.endswith(".sqlite3") and os.path.isfile(os.path.join(backup_dir, f))
        ]
        file_list.sort()

        # 上限超過チェック（デフォルトは20）
        if len(file_list) > getattr(settings, "BACKUP_NUM", 20):
            old_file = os.path.join(backup_dir, file_list[0])
            try:
                os.remove(old_file)
                messages.info(request, f"古いバックアップを削除しました: {old_file}")
            except Exception as e:
                messages.warning(request, f"古いバックアップの削除に失敗しました: {e}")

    except Exception as e:
        messages.error(request, f"バックアップ中にエラーが発生しました: {e}")

    return redirect("notice:news_card")

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
    """DBのバックアップ処理
    静的ページに戻さざるを得ない？
    """
    # DBコピー
    now = datetime.datetime.now()

    src_file = "./wh2.sqlite3"
    dst_file = f"./backup/{now.year}-{now.month}-{now.day}-{request.user}.sqlite3"
    shutil.copy(src_file, dst_file)
    # backupファイルのリスト
    file_list = os.listdir("./backup")
    # もし20を超えたら古いバックアップを削除する。
    if len(file_list) >= settings.BACKUP_NUM:
        file_list.sort()
        # ソートした結果の最初（古い）ファイルを削除する。
        os.remove("./backup/" + file_list[0])

    # master_pageに戻る。
    # https://docs.djangoproject.com/en/4.0/ref/contrib/messages/
    # https://stackoverflow.com/questions/51155947/django-redirect-to-another-view-with-context
    messages.info(request, f"DBをバックアップしました。 ファイル名:{dst_file}")
    return redirect("notice:news_card")

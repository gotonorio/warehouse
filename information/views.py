import logging

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from information.forms import InformationForm
from information.models import Information

logger = logging.getLogger(__name__)


class InformationListView(LoginRequiredMixin, generic.ListView):
    """情報一覧。 権限と表示フラグを考慮する"""

    model = Information
    # context_object_name = "information_list"

    def get_template_names(self):
        """デバイスによってテンプレートを切り替える"""
        if getattr(self.request, "user_agent_flag", None) == "mobile":
            return ["information/mobile_information.html"]
        return ["information/pc_information.html"]

    def get_queryset(self):
        """ユーザー権限に基づいてクエリセットをフィルタリングする"""
        user = self.request.user

        # 共通のベースクエリ（表示フラグがTrueのもの）
        qs = Information.objects.filter(display_info=True)

        # 権限による分岐
        if user.has_perm("library.add_file") or user.has_perm("notice.add_news"):
            # 特定の権限がある場合は全表示
            return qs.order_by("-sequense")
        else:
            # 権限がない場合は「情報」タイプのみに絞り込む
            return qs.filter(type_name__type_name="情報").order_by("-sequense")

    def get_context_data(self, **kwargs):
        """一覧以外の追加データを渡す（必要であれば）"""
        context = super().get_context_data(**kwargs)
        # 例：最新の日付をタイトル用に取得するなど
        # context["latest_date"] = ...
        return context


class InfoListView(generic.ListView):
    """
    編集時用 情報一覧、
    """

    model = Information
    template_name = "information/info_manage_list.html"
    queryset = Information.objects.all().order_by("-display_info", "-type_name", "-sequense")


class InformationCreateView(PermissionRequiredMixin, generic.CreateView):
    """情報の作成"""

    model = Information
    form_class = InformationForm
    # 必要な権限
    permission_required = "notice.add_news"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("information:info_list")


class InformationUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """情報の更新"""

    model = Information
    # デフォルトテンプレート名は「news_form.html」となる。（createviewと共通）
    form_class = InformationForm
    # 必要な権限
    permission_required = "notice.add_news"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("information:info_list")


class InformationDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """情報の削除
    getで呼び出された時は、model_confirm_delete.html が確認のため自動的に呼ばれる。
    confirmでpostとして、再度呼び出された時に削除が行われる。
    """

    model = Information
    # 必要な権限
    permission_required = "notice.add_news"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("information:info_list")

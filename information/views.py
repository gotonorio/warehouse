import logging

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from common.mixins import CustomPermissionRequiredMixin
from information.forms import InformationForm
from information.models import Information

logger = logging.getLogger(__name__)


class InformationListView(PermissionRequiredMixin, generic.ListView):
    """区分所有者用の情報一覧
    - 情報タイプ（type_name）が「情報」のデータを表示
    """

    model = Information
    template_name = "information/pc_information.html"
    # 区分所有者権限以上がアクセス可能
    permission_required = "library.view_file"
    # テンプレートへ渡したい変数を辞書で指定する
    extra_context = {
        "page_title": "マンション情報",
    }

    def get_queryset(self):
        """ユーザー権限に基づいてクエリセットをフィルタリングする"""

        # 共通のベースクエリ（表示フラグがTrueのもの）
        qs = (
            Information.objects.filter(display_info=True)
            .filter(type_name__type_name=settings.TYPE_NAME_INFO)
            .order_by("-sequense")
        )

        return qs


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


class BoardInformationListView(InformationListView, CustomPermissionRequiredMixin):
    """理事会用の情報一覧
    - 理事会メンバー以上の権限が必要
    """

    # diretorグループ以上の権限以上がアクセス可能
    permission_required = "library.view_category"
    # 権限がない場合に表示される
    permission_denied_template = "403_board_information.html"
    # テンプレートへ渡したい変数を辞書で指定する
    extra_context = {
        "page_title": "理事会専用情報",
    }

    def get_queryset(self):

        # アクセスユーザを取得
        user = self.request.user

        # type_nameが「情報」は除外
        qs = (
            Information.objects.filter(display_info=True)
            .exclude(type_name__type_name=settings.TYPE_NAME_INFO)
            .order_by("-sequense")
        )

        # data_manager権限以上は全て表示
        if user.has_perm("library.add_file"):
            return qs.order_by("-sequense")
        else:
            # director権限（理事会メンバー）の場合は「理事会」タイプのみに絞り込む
            return qs.filter(type_name__type_name=settings.TYPE_NAME_BOARD).order_by("-sequense")

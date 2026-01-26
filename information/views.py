import logging

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from information.forms import InformationForm
from information.models import Information

logger = logging.getLogger(__name__)


class InformationView(LoginRequiredMixin, generic.TemplateView):
    """情報一覧。 表示・非表示を考慮する"""

    model = Information

    def get_template_names(self):
        """templateファイルを切り替える"""
        if self.request.user_agent_flag == "mobile":
            template_name = "information/mobile_information.html"
        else:
            template_name = "information/pc_information.html"
        return [template_name]

    def get_context_data(self, **kwargs):
        """最新の日付データをタイトルとして表示する"""
        context = super().get_context_data(**kwargs)
        # userのgroup権限によって、表示を変える
        user = self.request.user
        if user.is_authenticated:
            # 権限での判定例
            if user.has_perm("library.add_file"):
                qs = Information.objects.filter(display_info=True).order_by("-sequense")
            elif user.has_perm("notice.add_news"):
                qs = Information.objects.filter(display_info=True).order_by("-sequense")
            else:
                # sophiagユーザ（loginユーザ）で、上記権限がない場合
                qs = (
                    Information.objects.filter(display_info=True)
                    .filter(type_name__type_name="情報")
                    .order_by("-sequense")
                )
            # グループ名での判定例
            # if user.groups.filter(name="chairman").exists():
            #     logger.debug("you are chairman")
            # elif user.groups.filter(name="data_manager").exists():
            #     logger.debug("you are data_manager")
            # elif user.groups.filter(name="news_manager").exists():
            #     logger.debug("you are news_manager")
            # else:
            #     logger.debug("you are normal user")

        context["information_list"] = qs
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

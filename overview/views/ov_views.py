import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import F
from django.urls import reverse_lazy
from django.views import generic
from overview.forms import OverviewForm, RoomTypeForm
from overview.models import OverView, RoomType

logger = logging.getLogger(__name__)


class Overview(generic.TemplateView):
    """公開情報 トップページ"""

    model = OverView

    # テンプレートを切り替える
    def get_template_names(self):
        """デバイスによってテンプレートを切り替える"""
        if self.request.user_agent.is_mobile:
            return ["overview/overview/overview_mobile.html"]
        return ["overview/overview/overview_pc.html"]

    # def get_template_names(self):
    #     if getattr(self.request, "user_agent_flag", None) == "mobile":
    #         return ["overview/overview/overview_mobile.html"]
    #     return ["overview/overview/overview_pc.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # .first() を使うことで、データが0件の場合でもエラー（IndexError）にならず None を返してくれる
        context["ov"] = OverView.objects.first()

        return context


class OverviewUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """マンション公開情報データアップデート
    - 概要は変化しないので、管理画面で初期データを登録する。
    - 駐車場台数や法規制は変更の可能性があるので、修正画面を作成する。
    """

    model = OverView
    form_class = OverviewForm
    template_name = "overview/overview/overview_form.html"
    permission_required = "library.add_file"
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy("overview:overview")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "マンション概要データの修正"
        return context

    def form_valid(self, form):
        """アップデートのログ記録のため"""
        logger.info(f"{self.request.user} update overview")
        return super().form_valid(form)


class RoomTypeUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """マンション住戸データのアップデートView"""

    model = RoomType
    form_class = RoomTypeForm
    template_name = "overview/overview/roomtype_form.html"
    permission_required = "library.add_file"
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy("overview:overview")


class RoomTypeListView(generic.ListView):
    model = RoomType
    template_name = "overview/overview/roomtype_list.html"

    def get_queryset(self):
        # 一覧表示に必要なアノテーションをここで一括で行う
        return RoomType.objects.annotate(total=F("kanrihi") + F("shuuzenhi") + F("ryokuchi") + F("niwa"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 集計処理
        # 各項目の合計を計算して、contextに追加（update）する
        metrics = {
            "total_kanrihi": RoomType.total_kanrihi("kanrihi")["total__sum"] or 0,
            "total_shuuzenhi": RoomType.total_kanrihi("shuuzenhi")["total__sum"] or 0,
            "total_niwa": RoomType.total_kanrihi("niwa")["total__sum"] or 0,
            "total_ryokuchi": RoomType.total_kanrihi("ryokuchi")["total__sum"] or 0,
        }

        context.update(metrics)

        # 全体合計の算出
        context["total_all"] = sum(metrics.values())

        return context

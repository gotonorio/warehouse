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

    def get_template_names(self):
        """templateファイルを切り替える"""
        if self.request.user_agent_flag == "mobile":
            template_name = "overview/overview/overview_mobile.html"
        else:
            template_name = "overview/overview/overview_pc.html"
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = OverView.objects.all()
        context["ov"] = qs[0]
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


class RoomTypeView(generic.TemplateView):
    """住戸タイプデータ"""

    model = RoomType
    template_name = "overview/overview/roomtype_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = RoomType.objects.all()
        qs = qs.annotate(total=F("kanrihi") + F("shuuzenhi") + F("ryokuchi") + F("niwa"))
        context["roomtypelist"] = qs
        # 管理費の合計
        total_kanrihi = RoomType.total_kanrihi("kanrihi")["total__sum"]
        context["total_kanrihi"] = total_kanrihi
        # 修繕費の合計
        total_shuuzenhi = RoomType.total_kanrihi("shuuzenhi")["total__sum"]
        context["total_shuuzenhi"] = total_shuuzenhi
        # 専用庭使用料の合計
        total_niwa = RoomType.total_kanrihi("niwa")["total__sum"]
        context["total_niwa"] = total_niwa
        # 緑地維持管理費の合計
        total_ryokuchi = RoomType.total_kanrihi("ryokuchi")["total__sum"]
        context["total_ryokuchi"] = total_ryokuchi
        # 合計
        context["total_all"] = total_kanrihi + total_shuuzenhi + total_niwa + total_ryokuchi

        return context

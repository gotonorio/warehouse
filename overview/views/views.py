import logging

from django.db.models import F
from django.views import generic
from overview.models import OverView, RoomType

logger = logging.getLogger(__name__)


class Overview(generic.TemplateView):
    """マンション概要"""

    model = OverView

    def get_template_names(self):
        """templateファイルを切り替える"""
        if self.request.user_agent_flag == "mobile":
            template_name = "overview/overview_mobile.html"
        else:
            template_name = "overview/overview_pc.html"
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = OverView.objects.all()
        context["ov"] = qs[0]
        return context


class RoomTypeView(generic.TemplateView):
    """住戸タイプデータ"""

    model = RoomType
    template_name = "overview/roomtype_list.html"

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

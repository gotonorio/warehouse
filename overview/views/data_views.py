import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from overview.forms import OverviewForm, RoomTypeForm
from overview.models import OverView, RoomType

logger = logging.getLogger(__name__)


class OverviewUpdateListView(PermissionRequiredMixin, generic.ListView):
    model = OverView
    permission_required = "library.add_file"


class OverviewUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """マンション概要データアップデートView
    - 概要は変化しないので、管理画面で初期データを登録する。
    - 駐車場台数や法規制は変更の可能性があるので、修正画面を作成する。
    """

    model = OverView
    form_class = OverviewForm
    template_name = "overview/overview_form.html"
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
    permission_required = "library.add_file"
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy("overview:overview")

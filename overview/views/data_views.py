from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from overview.forms import OverviewForm, RoomForm
from overview.models import OverView, Room


class OverviewUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """ マンション概要データアップデートView
    - 概要は変化しないので、管理画面で初期データを登録する。
    - 駐車場台数や法規制は変更の可能性があるので、修正画面を作成する。
    """
    model = OverView
    form_class = OverviewForm
    template_name = 'overview/overview_form.html'
    permission_required = ("library.add_file")
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy('overview:overview')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'マンション概要データの修正'
        return context


class RoomCreateView(PermissionRequiredMixin, generic.CreateView):
    """ 住戸データの登録 """
    model = Room
    form_class = RoomForm
    template_name = "overview/room_form.html"
    # 必要な権限
    permission_required = ("library.add_file")
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy('overview:create_room')


class RoomUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """ 住戸データのアップデート """
    model = Room
    form_class = RoomForm
    template_name = "overview/room_form.html"
    # 必要な権限
    permission_required = ("library.add_file")
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy('overview:room_list')

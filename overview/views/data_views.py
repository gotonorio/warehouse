from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from overview.forms import OverviewForm
from overview.models import OverView


class OverviewUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """ マンション概要データアップデートView """
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

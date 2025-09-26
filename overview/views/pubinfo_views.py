import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from overview.forms import PublicInformationForm
from overview.models import PublicInformation

logger = logging.getLogger(__name__)


class PublicInfoView(generic.TemplateView):
    """公開情報表示View"""

    model = PublicInformation
    template_name = "overview/pubinfo/pub_info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = PublicInformation.objects.all().filter(is_published=True).order_by("-year")

        context["pubinfo"] = qs
        return context


class PublicInfoListView(generic.ListView):
    """
    編集時用 情報一覧、
    """

    model = PublicInformation
    template_name = "overview/pubinfo/pub_info_list.html"

    def get_queryset(self):
        return PublicInformation.objects.order_by("-year", "-is_published")


class InformationCreateView(PermissionRequiredMixin, generic.CreateView):
    """情報の作成"""

    model = PublicInformation
    form_class = PublicInformationForm
    template_name = "overview/pubinfo/pub_info_form.html"
    # 必要な権限
    permission_required = "notice.add_news"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("overview:overview")


class PublicInfoUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """情報の更新"""

    model = PublicInformation
    form_class = PublicInformationForm
    template_name = "overview/pubinfo/pub_info_form.html"
    # 必要な権限
    permission_required = "notice.add_news"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("overview:overview")

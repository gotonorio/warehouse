import logging

from django.views import generic
from overview.models import PublicInformation

logger = logging.getLogger(__name__)


class PublicInfoView(generic.TemplateView):
    """公開情報表示View"""

    model = PublicInformation
    template_name = "overview/pubinfo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = PublicInformation.objects.all().filter(is_published=True).order_by("-year")

        context["pubinfo"] = qs
        return context

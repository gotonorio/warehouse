import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import generic

from library.models import File

logger = logging.getLogger(__name__)


class SearchlistView(LoginRequiredMixin, generic.ListView):
    """検索結果表示用View
    - 検索ボタンで抽出されたFileオブジェクトを一覧表示する。
    - 検索対象は「summary」「key_word」
    """

    model = File
    template_name = "notice/search_list.html"
    # paginate_by = 10

    def get_queryset(self):
        keyword = self.request.GET.get("keyword")
        return File.search(keyword, self.request.user)

    # 検索ボックスに検索ワードを表示し続けるための処理。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get("keyword")
        context["keyword"] = keyword
        return context

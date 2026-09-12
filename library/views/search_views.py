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
        return search(keyword, self.request.user)

    # 検索ボックスに検索ワードを表示し続けるための処理。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get("keyword")
        context["keyword"] = keyword
        logger.debug(context["keyword"])
        return context


def search(keyword, user):
    """File検索クエリを返す"""

    if not keyword:
        return File.objects.none()

    # キーワードのリストを作成
    kw_list = keyword.split()

    queryset = File.objects.order_by("-created_at")

    # データ管理者、スタッフ権限保持者以外は機密ファイル以外を検索できる
    if not (user.has_perm("library.add_file") or user.is_staff):
        queryset = queryset.filter(alive=True, is_confidential=False)

    # Q オブジェクト生成
    q_obj = Q()
    for value in kw_list:
        q_obj &= Q(title__icontains=value) | Q(key_word__icontains=value) | Q(summary__icontains=value)

    return queryset.filter(q_obj).distinct()

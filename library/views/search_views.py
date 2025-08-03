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
        user = self.request.user

        if not keyword:
            return File.objects.none()  # 検索キーワードがないときは空のクエリセットを返す

        kw_list = keyword.split()
        queryset = File.objects.order_by("-created_at")

        # 権限がない場合、alive=True で絞る
        if not (user.has_perm("library.add_file") or user.is_staff):
            queryset = queryset.filter(alive=True)

        q_objects = self.mk_q_objects(kw_list)  # Qオブジェクトを組み立てる独自関数
        return queryset.filter(q_objects).distinct()

    # 検索ボックスに検索ワードを表示し続けるための処理。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get("keyword")
        context["keyword"] = keyword
        return context

    def mk_q_objects(self, kw_list):
        """and検索のためのQオブジェクトを生成する"""
        # 空ならそのまま返す
        if not kw_list:
            return Q()

        q_obj = Q()
        for value in kw_list:
            q_obj &= (
                Q(**{"title__icontains": value})
                | Q(**{"key_word__icontains": value})
                | Q(**{"summary__icontains": value})
            )
        return q_obj

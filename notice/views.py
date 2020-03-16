# import logging

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q  # filterでor検索するために必要。
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from library.models import BigCategory, Category, File
from notice.forms import NewsForm
from notice.models import News


class NewsCardView(generic.ListView):
    """お知らせのcardによる一覧。 表示・非表示を考慮する。"""

    model = News
    template_name = "notice/news_card_list.html"
    paginate_by = 5
    queryset = News.objects.filter(display_news=True).order_by('-created_at')


class NewsListView(PermissionRequiredMixin, generic.ListView):
    """ お知らせのlist一覧。管理用なので、全データを表示させる."""

    model = News
    template_name = "notice/news_manage_list.html"
    paginate_by = 10
    # 必要な権限
    permission_required = ("notice.add_news")
    queryset = News.objects.order_by('-created_at')


class NewsCreateView(PermissionRequiredMixin, generic.CreateView):
    """カテゴリの作成."""

    model = News
    form_class = NewsForm
    # 必要な権限
    permission_required = ("notice.add_news")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('notice:news_card')


class NewsUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """カテゴリの更新."""

    model = News
    # デフォルトテンプレート名は「news_form.html」となる。（createviewと共通）
    form_class = NewsForm
    # 必要な権限
    permission_required = ("notice.add_news")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('notice:news_card')


class NewsDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """カテゴリの削除."""

    model = News
    # 必要な権限
    permission_required = ("notice.add_news")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('notice:news_card')


class BigCategoryView(generic.TemplateView):
    """ 全体メニューで選択された「BigCategory」に属するファイルを「Category」毎に表示する。
    表示数は100に制限する。（増えたらまた考える）
    """
    template_name = "notice/main_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        big_category = get_object_or_404(BigCategory, pk=self.kwargs['pk'])
        # user_idは、ログインしていないとNoneとなる。
        user_id = self.request.user.id
        # ログインしている場合は表示。していない場合はlimit=Trueのカテゴリは非表示とする。
        if user_id is None:
            category_obj = Category.objects.filter(
                parent=big_category, limit=False).order_by('-order', '-created_at')
        else:
            category_obj = Category.objects.filter(
                parent=big_category).order_by('-order', '-created_at')
        category_list = []
        # settings.pyでSELECT構文のLIMIT値を設定してある。
        limit = settings.SELECT_LIMIT_NUM
        for i in category_obj:
            file_obj = File.objects.filter(
                category=i.pk).filter(
                    alive=True).order_by('-order', '-created_at')[:limit]
            file_list = []
            for j in file_obj:
                file_list.append(j)
            category_list.append(file_list)
        context['category_list'] = category_list
        context['big_category_name'] = big_category.name
        context['comment_limit'] = settings.COMMENT_LIMIT + 1
        return context


class SearchlistView(generic.ListView):
    """ 検索結果表示用View
     検索ボタンで抽出されたFileオブジェクトを一覧表示する。
     検索対象は「title」「comment」
    """
    model = File
    template_name = "notice/search_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = File.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(comment__icontains=keyword)
                | Q(table_of_contents__icontains=keyword)
            )
        return queryset

    # 検索ボックスに検索ワードを表示し続けるための処理。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')
        context['keyword'] = keyword
        return context

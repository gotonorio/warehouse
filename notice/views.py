# import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from notice.forms import NewsForm
from notice.models import News


class NewsCardView(generic.ListView):
    """お知らせのcardによる一覧。 表示・非表示を考慮する。"""

    model = News
    template_name = "notice/news_card_list.html"
    paginate_by = 20
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
    """ お知らせの作成 """

    model = News
    form_class = NewsForm
    # 必要な権限
    permission_required = ("notice.add_news")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('notice:news_card')


class NewsUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """ お知らせの更新 """

    model = News
    # デフォルトテンプレート名は「news_form.html」となる。（createviewと共通）
    form_class = NewsForm
    # 必要な権限
    permission_required = ("notice.add_news")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('notice:news_card')

    def form_valid(self, form):
        # commitを停止する。
        self.object = form.save(commit=False)
        # created_atをセット。
        self.object.created_at = timezone.datetime.now()
        # データを保存。
        self.object.save()
        return super().form_valid(form)


class NewsDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """ お知らせの削除 """

    model = News
    # 必要な権限
    permission_required = ("notice.add_news")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('notice:news_card')

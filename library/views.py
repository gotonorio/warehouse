# import logging
from django.http import FileResponse

from django.conf import settings
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from library.forms import BigCategoryForm, CategoryForm, FileForm
from library.models import BigCategory, Category, File


class FileIndexView(PermissionRequiredMixin, generic.ListView):
    """ 管理者用 ファイル一覧 """
    model = File
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = False  # ログイン画面に飛ばす。
    paginate_by = 50

    def get_queryset(self):
        return File.objects.order_by('category', 'rank')


# def indirect_link(request, pk):
#     """ 間接リンク。実際のURLへリダイレクト """
#     file = get_object_or_404(File, pk=pk)
#     return redirect(file.src.url)


class FileCategoryView(PermissionRequiredMixin, generic.ListView):
    """ 管理者用 カテゴリ別のファイル一覧 """
    model = File
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    paginate_by = 20

    def get_queryset(self):
        """ カテゴリでfilter. """
        category_pk = self.kwargs['category_pk']
        return File.objects.filter(category__pk=category_pk).order_by('-rank')

    def get_context_data(self, *args, **kwargs):
        """ カテゴリのpkをテンプレートへ渡す. """
        context = super().get_context_data(*args, **kwargs)
        context['category_pk'] = self.kwargs.get('category_pk')
        return context


class FileCreateView(PermissionRequiredMixin, generic.CreateView):
    """ 管理者用 ファイルの作成. """
    model = File
    form_class = FileForm
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('library:file_index')

    def get_initial(self):
        """ カテゴリの指定があれば、そのカテゴリを選択状態に. """
        initial = super().get_initial()
        initial['category'] = self.kwargs.get('pk')
        return initial

    def form_valid(self, form):
        file = form.save()
        action = self.request.POST['action']

        # 保存してもう一つ追加ボタンのとき
        if action == 'send_more':
            return redirect('library:file_create', file.category.pk)
        # それ以外、送信ボタン
        else:
            return redirect('library:file_index')


class FileUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """ 管理者用 ファイルの更新. """
    model = File
    form_class = FileForm
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('library:file_index')

    def form_valid(self, form):
        file = form.save()
        action = self.request.POST['action']

        # 保存してもう一つ追加ボタンのとき
        if action == 'send_more':
            return redirect('library:file_create', file.category.pk)
        # それ以外、送信ボタン
        else:
            return redirect('library:file_index')


class FileDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """ 管理者用 ファイルの削除. """
    template_name = 'library/file_confirm_delete.html'
    model = File
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('library:file_index')


class CategoryIndexView(PermissionRequiredMixin, generic.ListView):
    """ 管理者用 カテゴリの一覧. """
    model = Category
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    paginate_by = 20

    def get_queryset(self):
        return Category.objects.order_by('parent__rank')


class CategoryBigView(PermissionRequiredMixin, generic.ListView):
    """ 管理者用 親カテゴリ別のカテゴリ一覧. """
    model = Category
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    paginate_by = 20

    def get_queryset(self):
        """ カテゴリでfilter. """
        big_pk = self.kwargs['big_pk']
        return Category.objects.filter(
            parent__pk=big_pk, alive=True).order_by('-rank', '-created_at')

    def get_context_data(self, *args, **kwargs):
        """ 親カテゴリのpkをテンプレートへ渡す. """
        context = super().get_context_data(*args, **kwargs)
        context['big_pk'] = self.kwargs.get('big_pk')
        return context


class CategoryCreateView(PermissionRequiredMixin, generic.CreateView):
    """ 管理者用 カテゴリの作成. """
    model = Category
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    form_class = CategoryForm
    success_url = reverse_lazy('library:category_index')

    def get_initial(self):
        """ 親カテゴリの指定があれば、その親カテゴリを選択状態に. """
        initial = super().get_initial()
        initial['parent'] = self.kwargs.get('pk')
        return initial


class CategoryUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """ 管理者用 カテゴリの更新. """
    model = Category
    form_class = CategoryForm
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('library:category_index')


class CategoryDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """ 管理者用 カテゴリの削除. """
    model = Category
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('library:category_index')
# Create your views here.


class BigCategoryIndexView(PermissionRequiredMixin, generic.ListView):
    """ 管理者用 親カテゴリの一覧
    templateは モデル名_list.html
    """
    model = BigCategory
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    queryset = BigCategory.objects.order_by('rank')
    paginate_by = 20


class BigCategoryCreateView(PermissionRequiredMixin, generic.CreateView):
    """ 親カテゴリの作成. """
    model = BigCategory
    form_class = BigCategoryForm
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('library:big_category_index')


class BigCategoryUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """ 親カテゴリの更新. """
    model = BigCategory
    form_class = BigCategoryForm
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('library:big_category_index')


class BigCategoryDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """ 親カテゴリの削除. """
    model = BigCategory
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('library:big_category_index')


class BigCategoryView(generic.TemplateView):
    """ メニューで選択された「BigCategory」に属するファイルを「Category」毎
    に表示する。表示数は100に制限する。（増えたら settings.py で変更してね）
    """
    template_name = "library/main_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        big_category = get_object_or_404(BigCategory, pk=self.kwargs['pk'])
        # user_idは、ログインしていないとNoneとなる。
        user_id = self.request.user.id
        # ログインしている場合は表示。していない場合はrestrict=Trueのカテゴリは非表示とする。
        if user_id is None:
            category_obj = Category.objects.filter(
                parent=big_category, restrict=False).order_by('parent__rank', '-rank')
        else:
            category_obj = Category.objects.filter(
                parent=big_category).order_by('parent__rank', '-rank')
        # settings.pyでSELECT構文のLIMIT値を設定してある。
        # limit = settings.SELECT_LIMIT_NUM
        category_list = []
        for i in category_obj:
            file_obj = File.objects.filter(
                category=i.pk).filter(
                    alive=True).order_by('-rank', '-created_at')
                    # alive=True).order_by('-rank', '-created_at')[:limit]
            file_list = []
            for j in file_obj:
                file_list.append(j)
            category_list.append(file_list)
        # templatesデータ設定
        context['category_list'] = category_list
        context['big_category_name'] = big_category.name
        context['comment_limit'] = settings.COMMENT_LIMIT + 1
        return context


class SearchlistView(LoginRequiredMixin, generic.ListView):
    """ 検索結果表示用View
     検索ボタンで抽出されたFileオブジェクトを一覧表示する。
     検索対象は「summary」「key_word」
    """
    model = File
    template_name = "notice/search_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = File.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(key_word__icontains=keyword)
                | Q(summary=keyword)
            )
        return queryset

    # 検索ボックスに検索ワードを表示し続けるための処理。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')
        context['keyword'] = keyword
        return context


class RijikaiMinutesView(LoginRequiredMixin, generic.ListView):
    """ 理事会議事録ファイルの一覧表
    左サイドのBigCategoryメニューからの表示は50件に制限している。
    ここでは全ファイルを表示する。
    """
    model = File
    template_name = "library/rijikai_minutes_list.html"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    paginate_by = 40

    def get_queryset(self):
        """ カテゴリパス名「rijikai」でfilter. """
        return File.objects.filter(category__path_name='rijikai').order_by('-rank')


class RijikaiDataListView(LoginRequiredMixin, generic.ListView):
    """ 理事会資料ファイルの一覧表
    左サイドのBigCategoryメニューからの表示は50件に制限している。
    ここでは全ファイルを表示する。
    """
    model = File
    template_name = "library/rijikai_data_list.html"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    paginate_by = 40

    def get_queryset(self):
        """ カテゴリパス名「rijikai_data」でfilter. """
        return File.objects.filter(category__path_name='rijikai_data').order_by('-rank')


class SoukaiRejimeListView(LoginRequiredMixin, generic.ListView):
    """ 総会議事録ファイルの一覧表
    左サイドのBigCategoryメニューからの表示は50件に制限している。
    ここでは全ファイルを表示する。
    """
    model = File
    template_name = "library/soukai_rejime_list.html"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    paginate_by = 40

    def get_queryset(self):
        """ カテゴリパス名「soukai_rejime」でfilter. """
        return File.objects.filter(category__path_name='soukai_rejime').order_by('-rank')


def pdf_view(request, pk):
    """ 効率的にはwebサーバが静的ファイルを配信するべきだが、
    djangoで配信してみる実験。
    """
    fn = get_object_or_404(File, pk=pk)
    if fn.download:
        return FileResponse(fn.src, as_attachment=True)
    else:
        return FileResponse(fn.src)

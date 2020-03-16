# import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from library.forms import BigCategoryForm, CategoryForm, FileForm
from library.models import BigCategory, Category, File


class FileIndexView(PermissionRequiredMixin, generic.ListView):
    """ ファイル一覧 """
    model = File
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = False  # ログイン画面に飛ばす。
    queryset = File.objects.order_by('category', '-created_at')
    paginate_by = 50


def indirect_link(request, pk):
    """ 間接リンク。実際のURLへリダイレクト """
    file = get_object_or_404(File, pk=pk)
    return redirect(file.src.url)


class FileCategoryView(PermissionRequiredMixin, generic.ListView):
    """ カテゴリ別のファイル一覧 """
    model = File
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    paginate_by = 20

    def get_queryset(self):
        """ カテゴリでfilter. """
        category_pk = self.kwargs['category_pk']
        return File.objects.filter(
            category__pk=category_pk).order_by('-rank')

    def get_context_data(self, *args, **kwargs):
        """ カテゴリのpkをテンプレートへ渡す. """
        context = super().get_context_data(*args, **kwargs)
        context['category_pk'] = self.kwargs.get('category_pk')
        return context


class FileCreateView(PermissionRequiredMixin, generic.CreateView):
    """ ファイルの作成. """
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
    """ ファイルの更新. """
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
    """ ファイルの削除. """
    template_name = 'library/file_confirm_delete.html'
    model = File
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('library:file_index')


class CategoryIndexView(PermissionRequiredMixin, generic.ListView):
    """ カテゴリの一覧. """

    model = Category
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    queryset = Category.objects.order_by('parent')
    paginate_by = 20


class CategoryBigView(PermissionRequiredMixin, generic.ListView):
    """ 親カテゴリ別のカテゴリ一覧. """
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
            parent__pk=big_pk).order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        """ 親カテゴリのpkをテンプレートへ渡す. """
        context = super().get_context_data(*args, **kwargs)
        context['big_pk'] = self.kwargs.get('big_pk')
        return context


class CategoryCreateView(PermissionRequiredMixin, generic.CreateView):
    """ カテゴリの作成. """
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
    """ カテゴリの更新. """
    model = Category
    form_class = CategoryForm
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('library:category_index')


class CategoryDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """ カテゴリの削除. """
    model = Category
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('library:category_index')
# Create your views here.


class BigCategoryIndexView(PermissionRequiredMixin, generic.ListView):
    """ 親カテゴリの一覧. """
    model = BigCategory
    # 必要な権限
    permission_required = ("library.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    queryset = BigCategory.objects.order_by('rank')
    paginate_by = 10


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

import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from library.forms import BigCategoryForm, CategoryForm, FileForm
from library.models import BigCategory, Category, File

logger = logging.getLogger(__name__)


class FileIndexView(PermissionRequiredMixin, generic.ListView):
    """管理者用 ファイル一覧"""

    model = File
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = False  # ログイン画面に飛ばす。
    # paginate_by = 50

    def get_queryset(self):
        return File.objects.order_by("-alive", "category", "rank")


class FileCategoryView(PermissionRequiredMixin, generic.ListView):
    """管理者用 カテゴリ別のファイル一覧"""

    model = File
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    # pagingを止める
    # paginate_by = 20

    def get_queryset(self):
        """カテゴリでfilter."""
        category_pk = self.kwargs["category_pk"]
        return File.objects.filter(category__pk=category_pk).order_by("-alive", "-rank")

    def get_context_data(self, *args, **kwargs):
        """カテゴリのpkをテンプレートへ渡す."""
        context = super().get_context_data(*args, **kwargs)
        context["category_pk"] = self.kwargs.get("category_pk")
        return context


class FileCreateView(PermissionRequiredMixin, generic.CreateView):
    """管理者用 ファイルの作成."""

    model = File
    form_class = FileForm
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:file_index")

    def get_initial(self):
        """カテゴリの指定があれば、そのカテゴリを選択状態に."""
        initial = super().get_initial()
        initial["category"] = self.kwargs.get("pk")
        return initial

    def form_valid(self, form):
        file = form.save()
        action = self.request.POST["action"]
        # file登録のログを記録する。
        file_name = form.cleaned_data["src"]
        logger.info(f"create {file_name} by {self.request.user}")
        # 保存してもう一つ追加ボタンのとき
        if action == "send_more":
            return redirect("library:file_create", file.category.pk)
        # それ以外、送信ボタン
        else:
            return redirect("library:file_index")


class FileUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """管理者用 ファイルの更新."""

    model = File
    form_class = FileForm
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:file_index")

    def form_valid(self, form):
        file = form.save()
        action = self.request.POST["action"]
        # fileアップデートのログを記録する。
        file_name = form.cleaned_data["src"]
        logger.warning(f"update {file_name} by {self.request.user}")

        # 保存してもう一つ追加ボタンのとき
        if action == "send_more":
            return redirect("library:file_create", file.category.pk)
        # それ以外、送信ボタン
        else:
            return redirect("library:file_index")


class FileDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """管理者用 ファイルの削除."""

    template_name = "library/file_confirm_delete.html"
    model = File
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:file_index")

    def post(self, request, *args, **kwargs):
        """ファイルs削除処理を自前で処理する"""

        self.object = self.get_object()
        try:
            self.object.delete()
            logger.warning(f"delete {self.object} by {request.user}")
            messages.success(request, f"{self.object}を削除しました。")
        except models.ProtectedError as e:
            messages.error(request, f"fファイル削除に失敗しました{e}」")
        return redirect(self.get_success_url())


class CategoryIndexView(PermissionRequiredMixin, generic.ListView):
    """管理者用 カテゴリの一覧."""

    model = Category
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    # paginate_by = 20

    def get_queryset(self):
        return Category.objects.order_by("-alive", "parent__rank")


class CategoryBigView(PermissionRequiredMixin, generic.ListView):
    """管理者用 親カテゴリ別のカテゴリ一覧."""

    model = Category
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    # paginate_by = 20

    def get_queryset(self):
        """カテゴリでfilter."""
        big_pk = self.kwargs["big_pk"]
        return Category.objects.filter(parent__pk=big_pk).order_by("-alive", "-rank", "-created_at")

    def get_context_data(self, *args, **kwargs):
        """親カテゴリのpkをテンプレートへ渡す."""
        context = super().get_context_data(*args, **kwargs)
        context["big_pk"] = self.kwargs.get("big_pk")
        return context


class CategoryCreateView(PermissionRequiredMixin, generic.CreateView):
    """管理者用 カテゴリの作成."""

    model = Category
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    form_class = CategoryForm
    success_url = reverse_lazy("library:category_index")

    def get_initial(self):
        """親カテゴリの指定があれば、その親カテゴリを選択状態に."""
        initial = super().get_initial()
        initial["parent"] = self.kwargs.get("pk")
        return initial


class CategoryUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """管理者用 カテゴリの更新."""

    model = Category
    form_class = CategoryForm
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:category_index")


class CategoryDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """管理者用 カテゴリの削除."""

    model = Category
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:category_index")

    def post(self, request, *args, **kwargs):
        """カテゴリ削除失敗時の処理"""

        self.object = self.get_object()
        try:
            self.object.delete()
            logger.warning(f"delete {self.object} by {request.user}")
            messages.success(request, f"{self.object}を削除しました。")
        except models.ProtectedError as e:
            protected_objects = list(e.protected_objects)
            detail = ", ".join(str(obj) for obj in protected_objects[:5])  # 長い場合は最初の5件のみ
            messages.error(request, f"先に次のファイルを削除してください。「{detail}」")
        return redirect(self.get_success_url())


class BigCategoryIndexView(PermissionRequiredMixin, generic.ListView):
    """管理者用 親カテゴリの一覧
    templateは モデル名_list.html
    """

    model = BigCategory
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。403.htmlがない場合はログイン画面に飛ばす。
    raise_exception = True
    queryset = BigCategory.objects.order_by("rank")
    # paginate_by = 20


class BigCategoryCreateView(PermissionRequiredMixin, generic.CreateView):
    """親カテゴリの作成."""

    model = BigCategory
    form_class = BigCategoryForm
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:big_category_index")


class BigCategoryUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """親カテゴリの更新."""

    model = BigCategory
    form_class = BigCategoryForm
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:big_category_index")


class BigCategoryDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """親カテゴリの削除."""

    model = BigCategory
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:big_category_index")

    def post(self, request, *args, **kwargs):
        """親カテゴリ削除を自前処理する"""

        self.object = self.get_object()
        try:
            self.object.delete()
            logger.warning(f"delete {self.object} by {request.user}")
            messages.success(request, f"{self.object}を削除しました。")
        except models.ProtectedError as e:
            protected_objects = list(e.protected_objects)
            detail = ", ".join(str(obj) for obj in protected_objects[:5])  # 長い場合は最初の5件のみ
            messages.error(request, f"先に次のkカテゴリを削除してください。「{detail}」")
        return redirect(self.get_success_url())


class BigCategoryView(generic.TemplateView):
    """メニューで選択された「BigCategory」に属するファイルを「Category」毎に表示する。
    - ファイル表示数はsettings.pyで変更する。
    - limit = settings.SELECT_LIMIT_NUM
    """

    def get_template_names(self):
        """templateファイルを切り替える"""
        if self.request.user_agent_flag == "mobile":
            template_name = "library/main_category_mobile.html"
        else:
            template_name = "library/main_category.html"
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        big_category = get_object_or_404(BigCategory, pk=self.kwargs["pk"])
        # user.idは、ログインしていないとNoneとなる。
        user = self.request.user
        # 選択されたメニュー（BigCategory）を親とするCategoryオブジェクトを取得する。
        # ユーザ権限によってrestrictフラグで取得できるCategoryを制限する。
        category_obj = Category.objects.filter(parent=big_category, alive=True)
        # ログイン制限(restrict=True)があるカテゴリはPermissionエラーを返す。
        if user.id is None:
            category_obj = category_obj.filter(restrict=False).order_by("parent__rank", "-rank")
            if len(category_obj) < 1:
                raise PermissionDenied()
        else:
            # ログインの場合はカテゴリを表示する。
            category_obj = category_obj.order_by("parent__rank", "-rank")
        # settings.pyでSELECT構文のLIMIT値を設定してある。
        limit = settings.SELECT_LIMIT_NUM
        category_list = []
        for i in category_obj:
            file_obj = (
                File.objects.filter(category=i.pk).filter(alive=True).order_by("-rank", "-created_at")[:limit]
            )
            # alive=True).order_by('-rank', '-created_at')
            file_list = []
            for j in file_obj:
                file_list.append(j)
            category_list.append(file_list)
        # templatesデータ設定
        context["category_list"] = category_list
        context["big_category_name"] = big_category.name
        context["comment_limit"] = settings.COMMENT_LIMIT + 1
        return context


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


def pdf_view(request, pk):
    """静的ファイル（PDFファイル）の閲覧処理
    - 効率的には下記のようにwebサーバが静的ファイルを配信する。urlをコピーするとログインせずに表示できてしまう。
    - <a href="{{file.src.url}}" target="_blank" rel="noopener noreferrer" download>{{file.title}}</a>
    - セキュリティを重視するため下記のように配信用の関数を使う。
    - <a href="{% url 'library:file_view' file.pk %}" target="_blank">{{file.title}}</a>
    """
    fn = get_object_or_404(File, pk=pk)
    if fn.category.restrict:
        if request.user.is_active:
            if fn.download:
                return FileResponse(fn.src, as_attachment=True)
            else:
                return FileResponse(fn.src)
        else:
            # @login_required制限をはずすと、ログインしない場合に下記を実行する。
            # ログイン画面に戻す場合は@login_requiredをセットする。
            # メイン画面に戻す場合は@login_requiredを外す。
            return redirect("notice:news_card")
    else:
        if fn.download:
            return FileResponse(fn.src, as_attachment=True)
        else:
            return FileResponse(fn.src)

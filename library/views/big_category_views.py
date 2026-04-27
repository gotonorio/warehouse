import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from library.forms import BigCategoryForm
from library.models import BigCategory, Category, File

logger = logging.getLogger(__name__)


class BigCategoryView(generic.DetailView):
    """
    BigCategoryに基づき、配下のCategoryとFileを構造化して表示する。
    - ファイル表示数はsettings.pyで変更する。
    - limit = settings.SELECT_LIMIT_NUM
    """

    model = BigCategory
    context_object_name = "big_category"  # templateで {{ big_category.name }} が使用可能

    def get_template_names(self):
        if getattr(self.request, "user_agent_flag", None) == "mobile":
            return ["library/main_category_mobile.html"]
        return ["library/main_category.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TemplateViewの場合、get_object_or_404()が必要となる
        # big_category = get_object_or_404(BigCategory, pk=self.kwargs["pk"])
        # DetailViewがURLのpkから自動取得したBigCategory
        big_category = self.object
        user = self.request.user
        limit = settings.SELECT_LIMIT_NUM

        # 1. カテゴリの取得と閲覧制限の判定
        # ログインしていない場合(user.id is None)の処理を整理
        category_qs = Category.objects.filter(parent=big_category, alive=True)

        if not user.is_authenticated:
            # 未ログイン時は制限(restrict)がないカテゴリのみ
            category_qs = category_qs.filter(restrict=False)
            if not category_qs.exists():
                raise PermissionDenied()

        category_obj = category_qs.order_by("parent__rank", "-rank")

        # 2. カテゴリごとのファイルリストを作成
        category_list = []
        has_add_perm = user.has_perm("library.add_file")

        for cat in category_obj:
            # クエリの組み立て
            file_qs = File.objects.filter(category=cat, alive=True)

            # 権限がない場合は機密ファイル(is_confidential)を除外
            if not has_add_perm:
                file_qs = file_qs.filter(is_confidential=False)

            # 並び替えとリミット適用
            # 既存の forループで append する処理を list() で簡略化
            files = list(file_qs.order_by("-rank", "-created_at")[:limit])

            # 既存テンプレートに合わせて「ファイルのリスト」をリストに追加
            category_list.append(files)

        # 3. テンプレートへ渡すデータ
        context["category_list"] = category_list
        context["big_category_name"] = big_category.name
        context["comment_limit"] = settings.COMMENT_LIMIT + 1

        return context


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
    """管理者用 親カテゴリの作成"""

    model = BigCategory
    form_class = BigCategoryForm
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:big_category_index")


class BigCategoryUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """管理者用 親カテゴリの更新"""

    model = BigCategory
    form_class = BigCategoryForm
    # 必要な権限
    permission_required = "library.add_file"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("library:big_category_index")


class BigCategoryDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """管理者用 親カテゴリの削除."""

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

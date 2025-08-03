import logging

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from library.forms import CategoryForm
from library.models import Category

logger = logging.getLogger(__name__)


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

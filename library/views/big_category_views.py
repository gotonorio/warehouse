import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from library.forms import BigCategoryForm
from library.models import BigCategory, Category, File

logger = logging.getLogger(__name__)


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

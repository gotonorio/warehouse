from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from information.forms import InformationForm
from information.models import Information


class InformationView(generic.ListView):
    """ 情報一覧。 表示・非表示を考慮する """

    model = Information
    template_name = "information/information_list.html"
    queryset = Information.objects.filter(
        display_info=True).order_by('-created_at')


class InfoListView(generic.ListView):
    """ 情報一覧、編集時用 """

    model = Information
    template_name = "information/info_manage_list.html"
    queryset = Information.objects.order_by('-created_at')


class InformationCreateView(PermissionRequiredMixin, generic.CreateView):
    """ 情報の作成 """

    model = Information
    form_class = InformationForm
    # 必要な権限
    permission_required = ("file_uploader.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('information:info_list')


class InformationUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """ 情報の更新 """

    model = Information
    # デフォルトテンプレート名は「news_form.html」となる。（createviewと共通）
    form_class = InformationForm
    # 必要な権限
    permission_required = ("file_uploader.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('information:info_list')


class InformationDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """
     情報の削除
       getで呼び出された時は、model_confirm_delete.html が確認のため自動的に呼ばれる。
       confirmでpostとして、再度呼び出された時に削除が行われる。
     """
    model = Information
    # 必要な権限
    permission_required = ("file_uploader.add_file")
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy('information:info_list')

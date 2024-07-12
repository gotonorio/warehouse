import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from information.forms import InformationForm
from information.models import Information

logger = logging.getLogger(__name__)


class InformationView(LoginRequiredMixin, generic.TemplateView):
    """情報一覧。 表示・非表示を考慮する"""

    model = Information

    def get_template_names(self):
        """templateファイルを切り替える"""
        if self.request.user_agent_flag == "mobile":
            template_name = "information/mobile_information.html"
        else:
            template_name = "information/pc_information.html"
        return [template_name]

    def get_context_data(self, **kwargs):
        """最新の日付データをタイトルとして表示する"""
        context = super().get_context_data(**kwargs)
        qs = (
            Information.objects.filter(display_info=True)
            .filter(type_name__type_name="情報")
            .order_by("-sequense")
        )
        context["information_list"] = qs
        return context


class InfoListView(generic.ListView):
    """情報一覧、編集時用"""

    model = Information
    template_name = "information/info_manage_list.html"
    queryset = Information.objects.order_by("-sequense")


class InformationCreateView(PermissionRequiredMixin, generic.CreateView):
    """情報の作成"""

    model = Information
    form_class = InformationForm
    # 必要な権限
    permission_required = "notice.add_news"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("information:info_list")


class InformationUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """情報の更新"""

    model = Information
    # デフォルトテンプレート名は「news_form.html」となる。（createviewと共通）
    form_class = InformationForm
    # 必要な権限
    permission_required = "notice.add_news"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("information:info_list")


class InformationDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """情報の削除
    getで呼び出された時は、model_confirm_delete.html が確認のため自動的に呼ばれる。
    confirmでpostとして、再度呼び出された時に削除が行われる。
    """

    model = Information
    # 必要な権限
    permission_required = "notice.add_news"
    # 権限がない場合、Forbidden 403を返す。これがない場合はログイン画面に飛ばす。
    raise_exception = True
    success_url = reverse_lazy("information:info_list")


@login_required
def weasyprint(request, pk):
    """Generate pdf.
    https://docs.djangoproject.com/ja/4.0/topics/auth/default/
    https://qiita.com/mag-chang/items/c01ccb21a05c51cb1b45
    https://thr3a.hatenablog.com/entry/20200816/1597541884
    https://weasyprint.readthedocs.io/en/stable/tutorial.html
    https://doc.courtbouillon.org/weasyprint/latest/first_steps.html#linux
    """
    from django.http import HttpResponse
    from django.template.loader import get_template
    from weasyprint import HTML

    # Model data
    target_qs = Information.objects.get(id=pk)

    # pdf化するtemplatesを読み込む
    html_template = get_template("information/weasyprint.html")

    html_str = html_template.render({"target": target_qs}, request)
    pdf_file = HTML(
        string=html_str,
        # 現在アクセスしているページのURLを設定
        base_url=request.build_absolute_uri(),
    ).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    file_name = "information.pdf"
    response["Content-Disposition"] = f"attachment; filename={file_name}"
    return response

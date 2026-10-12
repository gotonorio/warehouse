import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic

from control.models import ControlRecord
from register.forms import LoginForm

# https://djangobrothers.com/blogs/referencing_the_user_model/
User = get_user_model()

logger = logging.getLogger(__name__)


def test_view(request):
    logger.debug(request.META.get("REMOTE_ADDR"))
    logger.debug(request.META.get("HTTP_X_FORWARDED_FOR"))


class Login(LoginView):
    """ログインページ"""

    form_class = LoginForm
    template_name = "register/login.html"

    def get_context_data(self, **kwargs):
        """ログインページで仮登録メニューを表示させる"""
        context = super().get_context_data(**kwargs)
        context["tmp_user_flg"] = ControlRecord.get_tmp_user_flg()
        test_view(self.request)

        return context


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""

    template_name = "register/logout.html"


class MenuView(LoginRequiredMixin, generic.TemplateView):
    """メニュー画面"""

    def get_template_names(self):
        """デバイスによってテンプレートを切り替える"""
        if self.request.user_agent.is_mobile:
            return ["register/menu_mobile.html"]
        return ["register/menu_pc.html"]

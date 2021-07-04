# import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from library.models import File

from .forms import LoginForm


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'register/logout.html'


class MenuView(TemplateView):
    """ メニュー画面 """
    template_name = 'register/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = File.objects.filter(title='基本使用規則')
        for kisoku in qs:
            context['kisoku'] = kisoku
        return context

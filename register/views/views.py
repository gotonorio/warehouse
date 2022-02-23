# import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, resolve_url
from django.views import generic
from library.models import File
from register.forms import (LoginForm, PasswordUpdateForm, TempUserCreateForm,
                            UserUpdateForm)

# https://djangobrothers.com/blogs/referencing_the_user_model/
User = get_user_model()


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'register/logout.html'


class MenuView(generic.TemplateView):
    """ メニュー画面 """

    def get_template_names(self):
        """ templateファイルを切り替える """
        if self.request.user_agent_flag == 'mobile':
            template_name = "register/menu_mobile.html"
        else:
            template_name = "register/menu_pc.html"
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = File.objects.filter(title='基本使用規則')
        for kisoku in qs:
            context['kisoku'] = kisoku
        return context

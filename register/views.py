from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm
from django.shortcuts import render


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'register/logout.html'


# メニュー画面
def warehouse_menu(request):
    return render(request, 'register/menu.html')

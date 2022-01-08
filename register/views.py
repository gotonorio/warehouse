import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, resolve_url
from django.views import generic
from library.models import File

from .forms import (LoginForm, PasswordUpdateForm, TempUserCreateForm,
                    UserUpdateForm)

# https://djangobrothers.com/blogs/referencing_the_user_model/
MyUser = get_user_model()


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'register/logout.html'


class MenuView(generic.TemplateView):
    """ メニュー画面 """
    template_name = 'register/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = File.objects.filter(title='基本使用規則')
        for kisoku in qs:
            context['kisoku'] = kisoku
        return context


class TempUserCreateView(generic.CreateView):
    """ 未登録ユーザーが仮登録するためのVIEW。
    ユーザには「add_post」と「view_post」のパーミションを付加する。
    """
    template_name = 'register/temp_user_create.html'
    form_class = TempUserCreateForm

    def form_valid(self, form):
        """ 仮登録ではis_activeフラグを立てず、管理者が承認することで
        is_active＝Trueとする。また登録するユーザには権限を付加する。
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # signalによってgroupを追加してpermissionを付加してみる。
        # permission = Permission.objects.get(codename='add_post')
        # user.user_permissions.add(permission)
        # permission = Permission.objects.get(codename='view_post')
        # user.user_permissions.add(permission)

        return redirect('register:temp_user_done')


class TempUserDoneView(generic.TemplateView):
    """ 仮登録完了後、メールを待つように表示するだけのVIEW。 """
    template_name = 'register/temp_user_done.html'


class UserListView(PermissionRequiredMixin, generic.ListView):
    """ 管理者が使用するユーザリストの一覧表示。
    templatesファイルはデフォルト（user_list.html）を使用。
    渡されるobjectもデフォルトの「user_list」。
    """
    model = MyUser
    permission_required = ("register.add_myuser",)

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs).order_by('groups', 'is_active')
        return qs


class OnlyYouMixin(UserPassesTestMixin):
    """ パスワードの変更処理用
    自分自身だけでなく、ユーザ登録情報によって制限することができる。
    https://qiita.com/chanyou0311/items/31a4380d11c904563c86
    https://docs.djangoproject.com/ja/2.2/topics/auth/default/
    """
    raise_exception = True

    def test_func(self):
        user = self.request.user
        # return user.pk == self.kwargs['pk'] or user.is_superuser
        return user.pk == self.kwargs['pk']


class UserPasswordUpdate(OnlyYouMixin, PasswordChangeView):
    """ ログインしたユーザが自分でパスワードを変更するためのVIEW。"""
    model = MyUser
    form_class = PasswordUpdateForm
    template_name = 'register/password_update_form.html'

    def get_success_url(self):
        # return resolve_url('register:pwd_update', pk=self.kwargs['pk'])
        return resolve_url('register:mypage')


class UserManagementView(PermissionRequiredMixin, generic.UpdateView):
    """ 管理者がユーザの「有効性」を操作するためのVIEW。 """
    model = MyUser
    form_class = UserUpdateForm
    template_name = 'register/user_update_form.html'
    permission_required = ("register.add_myuser",)

    def get_success_url(self):
        return resolve_url('register:user_list')

    def form_valid(self, form):
        """ 仮登録ではis_activeフラグを立てず、管理者が承認することで
        is_active＝Trueとする。またグループの変更も行う。
        """
        user = form.save(commit=False)
        user.save()
        new_group = form.cleaned_data['group']
        user.groups.clear()
        group = Group.objects.get(name=new_group)
        user.groups.add(group)
        return redirect('register:user_list')

    def get_context_data(self, **kwargs):
        """ ユーザ修正画面で現在値をformに表示させる  """
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        user = MyUser.objects.get(pk=pk)
        groups = user.groups.all()
        logging.debug(groups[0])
        user_update_form = UserUpdateForm(initial={
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'group': groups[0]
        })
        context['form'] = user_update_form
        return context

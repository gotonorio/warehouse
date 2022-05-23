import logging

from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

logger = logging.getLogger(__name__)


class ControlRecord(models.Model):
    """ プロジェクトのコントロール用定数を定義 """
    # 仮登録メニューの表示/非表示コントロール
    tmp_user_flg = models.BooleanField(verbose_name='仮登録', default=False)
    # add your control variable

    @classmethod
    def show_tmp_user_menu(cls):
        return cls.objects.get('tmp_user_flg')


class AttendanceRecord(models.Model):
    """ ログイン・ログアウト履歴を保存、管理画面で確認
    2022-05-16:ログはファイル出力するようにしたので不要となる。
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='ユーザー', on_delete=models.PROTECT)
    login_time = models.DateTimeField('ログイン時刻', blank=True, null=True)
    logout_time = models.DateTimeField('ログアウト時刻', blank=True, null=True)

    def __str__(self):
        """ フォームやテンプレート以外では自分でローカルタイムに変換 """
        login_dt = timezone.localtime(self.login_time)
        return '{0} - {1.year}/{1.month}/{1.day} {1.hour}:{1.minute}:{1.second} - {2}'.format(
            self.user.username, login_dt, self.get_diff_time()
        )

    def get_diff_time(self):
        """ログアウト時間ーログイン時間"""
        if not self.logout_time:
            return 'ログアウトしていません'
        else:
            td = self.logout_time - self.login_time
            return '{0}時間{1}分'.format(
                td.seconds // 3600, (td.seconds // 60) % 60)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """ ログインした際に呼ばれて、管理者ならログ記録する """
    if user_is_manager(request, user):
        # AttendanceRecord.objects.create(user=user, login_time=timezone.now())
        logger.info(f'{user} login')


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """ ログアウトした際に呼ばれる """
    if user_is_manager(request, user):
        logger.info(f'{user} logout')
        # records = AttendanceRecord.objects.filter(user=user, logout_time__isnull=True)
        # if records:
        #     record = records.latest('pk')
        #     record.logout_time = timezone.now()
        #     record.save()


def user_is_manager(request, user):
    """ userが「管理者」どうかの判定(adminuserは除外) """
    rtn = False
    qs = request.user.groups.values_list('name', flat=True)
    if qs and list(qs)[0] in ['chairman', 'master']:
        rtn = True
    return rtn

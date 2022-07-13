import collections
import logging
import re

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import F
from django.views import generic
from overview.models import OverView, Room, RoomType

logger = logging.getLogger(__name__)


class Overview(generic.TemplateView):
    """ マンション概要 """
    model = OverView

    def get_template_names(self):
        """ templateファイルを切り替える """
        if self.request.user_agent_flag == 'mobile':
            template_name = "overview/overview_mobile.html"
        else:
            template_name = "overview/overview_pc.html"
        return [template_name]

    def get_context_data(self, **kwargs):
        """ 最新の日付データをタイトルとして表示する """
        context = super().get_context_data(**kwargs)
        qs_dict = OverView.objects.all().values()
        context['ov'] = qs_dict[0]
        return context


class RoomView(PermissionRequiredMixin, generic.TemplateView):
    """ 住戸データ """
    model = Room
    template_name = "overview/room_list.html"
    permission_required = ("overview.view_room")

    # 管理費等の合計をpython関数で求める。
    def calc_total(self, sql):
        """ 縦の合計を返す """
        total = {'total': 0, 'parking': 0, 'bicycle': 0, 'bike': 0, 'membershipfee': 0}
        for d in sql:
            total['total'] += (d.room_type.kanrihi+d.room_type.shuuzenhi +
                               d.room_type.ryokuchi+d.room_type.niwa)
            total['parking'] += d.parking_fee
            if d.chounaikai:
                total['membershipfee'] += settings.MEMBERSHIP_FEE
            total['bicycle'] += d.bicycle_fee
            total['bike'] += d.bike_fee
        return total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Room.objects.all().order_by('room_no')
        qs = qs.annotate(
            total=F('room_type__kanrihi')+F('room_type__shuuzenhi')+F('room_type__ryokuchi')+F('room_type__niwa'))
        total = self.calc_total(qs)
        context['roomlist'] = qs
        context['total'] = total['total']
        context['total_parking'] = total['parking']
        context['total_bicycle'] = total['bicycle']
        context['total_bike'] = total['bike']
        context['total_membershipfee'] = total['membershipfee']
        context['membership_fee'] = settings.MEMBERSHIP_FEE
        return context


class RoomTypeView(generic.TemplateView):
    """ 住戸タイプデータ """
    model = RoomType
    template_name = "overview/roomtype_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = RoomType.objects.all()
        qs = qs.annotate(total=F('kanrihi')+F('shuuzenhi')+F('ryokuchi')+F('niwa'))
        context['roomtypelist'] = qs
        # 管理費の合計
        total_kanrihi = RoomType.total_kanrihi('kanrihi')['total__sum']
        context['total_kanrihi'] = total_kanrihi
        # 修繕費の合計
        total_shuuzenhi = RoomType.total_kanrihi('shuuzenhi')['total__sum']
        context['total_shuuzenhi'] = total_shuuzenhi
        # 専用庭使用料の合計
        total_niwa = RoomType.total_kanrihi('niwa')['total__sum']
        context['total_niwa'] = total_niwa
        # 緑地維持管理費の合計
        total_ryokuchi = RoomType.total_kanrihi('ryokuchi')['total__sum']
        context['total_ryokuchi'] = total_ryokuchi
        # 合計
        context['total_all'] = total_kanrihi+total_shuuzenhi+total_niwa+total_ryokuchi

        return context


class BicycleStorage(generic.TemplateView):
    """ 自転車置場 """
    model = Room
    template_name = 'overview/bicycle_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Room.objects.exclude(comment__exact=None).values(
            'room_no', 'comment').order_by('room_no')
        data_dict = {}
        bicycle_storage_list = []
        for obj in qs:
            # comment文から半角カンマで連続している数字列を半角空白区切りの文字列として取り出す
            values_str = self.list_to_str(re.findall('[0-9]+', obj['comment']))
            # 空白区切りの文字列をlistに変換してappendする
            str_list = values_str.split(' ')
            # 自転車置場番号をlistとして作成する
            bicycle_storage_list.extend(str_list)
            # 部屋番号をkeyとして自転車置場番号をvalueとするdictを作成する
            data_dict[obj['room_no']] = values_str
        int_list = list(map(int, bicycle_storage_list))
        context['bicycle_list'] = data_dict
        context['bicycle_storage_list'] = sorted(int_list)
        context['bicycle_num'] = len(bicycle_storage_list)
        return context

    def list_to_str(self, list_data):
        """ リストを空白区切りの文字列として返す """
        result = ""
        for s in list_data:
            result += s + " "
        return result.strip()

    def check_storage(self, list_data):
        """ 駐輪場番号の重複をチェックする """
        chk_list = []
        for k, v in collections.Counter(list_data).items():
            if v > 1:
                chk_list.append(k)
        return chk_list

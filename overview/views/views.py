from django.conf import settings
from django.db.models import F
from django.views import generic
from overview.models import OverView, Room, RoomType


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


class RoomView(generic.TemplateView):
    """ 住戸データ """
    model = Room
    template_name = "overview/room_list.html"

    # 管理費等の合計をpython関数で求める。
    def calc_total(self, sql):
        total = {'total': 0, 'parking': 0, 'bicycle': 0, 'bike': 0, 'membershipfee': 0}
        for d in sql:
            total['total'] += (d.room_type.kanrihi + d.room_type.shuuzenhi + d.room_type.ryokuchi + d.room_type.niwa)
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
        return context

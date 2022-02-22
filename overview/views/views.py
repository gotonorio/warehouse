from django.views import generic
from overview.models import OverView, Room


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Room.objects.all().order_by('room_no')
        context['roomlist'] = qs
        return context

import csv
import io
import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from overview.forms import CSVImportForm, OverviewForm, RoomForm
from overview.models import OverView, Room

logger = logging.getLogger(__name__)


class OverviewUpdateListView(PermissionRequiredMixin, generic.ListView):
    model = OverView
    permission_required = ("library.add_file")


class OverviewUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """ マンション概要データアップデートView
    - 概要は変化しないので、管理画面で初期データを登録する。
    - 駐車場台数や法規制は変更の可能性があるので、修正画面を作成する。
    """
    model = OverView
    form_class = OverviewForm
    template_name = 'overview/overview_form.html'
    permission_required = ("library.add_file")
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy('overview:overview')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'マンション概要データの修正'
        return context

    def form_valid(self, form):
        """ アップデートのログ記録のため """
        logger.info(f'{self.request.user} update overview')
        return super().form_valid(form)


class RoomCreateView(PermissionRequiredMixin, generic.CreateView):
    """ 住戸データの登録
    最初に1回しか使わないので、管理画面で初期登録を行うため使用しない。
    """
    model = Room
    form_class = RoomForm
    template_name = "overview/room_form.html"
    # 必要な権限
    permission_required = ("library.add_file")
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy('overview:create_room')


class RoomUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """ 住戸データのアップデート """
    model = Room
    form_class = RoomForm
    template_name = "overview/room_form.html"
    # 必要な権限
    permission_required = ("library.add_file")
    # 保存が成功した場合に遷移するurl
    success_url = reverse_lazy('overview:room_list')

    def form_valid(self, form):
        # commitを停止する。
        self.object = form.save(commit=False)
        # created_dateをセット。
        self.object.created_date = timezone.datetime.now()
        # データを保存。
        self.object.save()
        # ログファイルに更新者と更新した部屋番号を記録する。
        logger.info(f'{self.request.user} update room {self.object.room_no}')
        return super().form_valid(form)


class ImportParkingfee(PermissionRequiredMixin, generic.FormView):
    """ 駐車場使用料をインポート """
    template_name = 'overview/import_parkingfee.html'
    success_url = reverse_lazy('notice:news_card')
    form_class = CSVImportForm
    # 必要な権限
    permission_required = ("library.add_file")

    def pk_dict(self):
        """ 部屋番号をキーとするプライマリキーの辞書を返す """
        qs = Room.objects.all().order_by('room_no')
        pkdict = {}
        for obj in qs:
            pkdict[obj.room_no] = obj.pk
        return pkdict

    def clear_parkingfee(self):
        """ 全住戸の駐車場費をクリアする """
        qs = Room.objects.all().order_by('room_no')
        for row in qs:
            row.parking_fee = 0
            row.save()

    def form_valid(self, form):
        """ 駐車場使用料をアップデートする。
        - CSVファイルはヘッダー無し。
        - 同じ部屋番号で複数台使用を考慮。.
        """
        pkdict = self.pk_dict()
        # 最初に全住戸の駐車場費をクリア。
        self.clear_parkingfee()
        # csv.readerに渡すため、TextIOWrapperでテキストモードなファイルに変換
        csvfile = io.TextIOWrapper(form.cleaned_data['file'], encoding='utf-8')
        parking = csv.reader(csvfile)
        # 1行目の年月データを読み込む
        year_month = next(parking)
        # 2行目から1行ずつ取り出して処理する。
        for row in parking:
            pk = pkdict[int(row[0])]
            room = Room.objects.get(id=pk)
            room.parking_fee += int(row[1].replace(',', ''))
            room.parking_date = year_month[0]
            room.save()
        logger.info(f'{self.request.user} update {year_month} parking_fee')
        return super().form_valid(form)

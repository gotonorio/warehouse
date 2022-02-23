from django.urls import path

from overview.views import views
from overview.views import data_views

app_name = "overview"

urlpatterns = [
    # 概要表示
    path('overview', views.Overview.as_view(), name='overview'),
    path('room/list', views.RoomView.as_view(), name='room_list'),
    path('roomtype/list', views.RoomTypeView.as_view(), name='roomtype_list'),
    # データ処理
    path('overview/update/<int:pk>', data_views.OverviewUpdateView.as_view(), name='overview_update'),
    path('room/create', data_views.RoomCreateView.as_view(), name='create_room'),
    path('room/update/<int:pk>', data_views.RoomUpdateView.as_view(), name='room_update'),
]

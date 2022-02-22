from django.urls import path

from overview.views import views
from overview.views import data_views

app_name = "overview"

urlpatterns = [
    path('overview', views.Overview.as_view(), name='overview'),
    path('overview/update/<int:pk>', data_views.OverviewUpdateView.as_view(), name='overview_update'),
    path('room/list', views.RoomView.as_view(), name='room_list'),
    path('room/create', data_views.RoomCreateView.as_view(), name='create_room'),
    path('room/update/<int:pk>', data_views.RoomUpdateView.as_view(), name='room_update'),
]

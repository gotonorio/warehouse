from django.urls import path

from overview.views import views
from overview.views import data_views

app_name = "overview"

urlpatterns = [
    path('overview', views.Overview.as_view(), name='overview'),
    path('overview/update/<int:pk>', data_views.OverviewUpdateView.as_view(), name='overview_update'),
    path('room/create', data_views.SectionOwnerCreateView.as_view(), name='create_room'),
]

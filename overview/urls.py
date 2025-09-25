from django.urls import path

from overview.views import ov_views, pubinfo_views

app_name = "overview"

urlpatterns = [
    # 公開情報
    path("pubinfo", pubinfo_views.PublicInfoView.as_view(), name="pubinfo"),
    path("overview", ov_views.Overview.as_view(), name="overview"),
    path("roomtype/list", ov_views.RoomTypeView.as_view(), name="roomtype_list"),
    # データ処理
    path(
        "overview/update/<int:pk>",
        ov_views.OverviewUpdateView.as_view(),
        name="overview_update",
    ),
    path(
        "roomtype/update/<int:pk>",
        ov_views.RoomTypeUpdateView.as_view(),
        name="roomtype_update",
    ),
]

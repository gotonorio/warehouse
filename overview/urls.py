from django.urls import path

from overview.views import ov_views, pubinfo_views

app_name = "overview"

urlpatterns = [
    # 公開情報
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
    # 公開情報の表示、作成、更新
    path("pubinfo", pubinfo_views.PublicInfoView.as_view(), name="pubinfo"),
    path("overview/pub_create/", pubinfo_views.InformationCreateView.as_view(), name="pub_create"),
    path("pub_info_list/", pubinfo_views.PublicInfoListView.as_view(), name="pub_info_list"),
    path(
        "overview/pub_update/<int:pk>",
        pubinfo_views.PublicInfoUpdateView.as_view(),
        name="pub_update",
    ),
]

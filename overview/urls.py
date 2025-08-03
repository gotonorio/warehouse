from django.urls import path

from overview import views

app_name = "overview"

urlpatterns = [
    # 概要表示
    path("overview", views.Overview.as_view(), name="overview"),
    path("roomtype/list", views.RoomTypeView.as_view(), name="roomtype_list"),
    # データ処理
    path(
        "overview/update/<int:pk>",
        views.OverviewUpdateView.as_view(),
        name="overview_update",
    ),
    path(
        "roomtype/update/<int:pk>",
        views.RoomTypeUpdateView.as_view(),
        name="roomtype_update",
    ),
]

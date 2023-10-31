from django.urls import path

from information import views

app_name = "information"

urlpatterns = [
    # Informationの表示
    path("", views.InformationView.as_view(), name="information"),
    path("information/", views.InformationView.as_view(), name="information"),
    # 編集用のtitle一覧表示
    path("info_list/", views.InfoListView.as_view(), name="info_list"),
    # 情報の作成
    path("info_add/", views.InformationCreateView.as_view(), name="info_add"),
    # 情報の修正
    path(
        "info_update/<int:pk>",
        views.InformationUpdateView.as_view(),
        name="info_update",
    ),
    # 情報の削除
    path(
        "info_delete/<int:pk>",
        views.InformationDeleteView.as_view(),
        name="info_delete",
    ),
]

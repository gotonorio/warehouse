from django.urls import path

from notice import views

app_name = "notice"

urlpatterns = [
    # NewsのCRUD
    path('', views.NewsCardView.as_view(), name='news_card'),
    path('news/', views.NewsCardView.as_view(), name='news_card'),
    path('news/list/', views.NewsListView.as_view(), name='news_list'),
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/update/<int:pk>',
         views.NewsUpdateView.as_view(), name='news_update'),
    path('news/delete/<int:pk>',
         views.NewsDeleteView.as_view(), name='news_delete'),
    # BigCategoruに属するファイルを一覧表示
    path('bigcategory/<int:pk>/',
         views.BigCategoryView.as_view(), name='bigcategory'),
    # 検索結果表示
    path('search/', views.SearchlistView.as_view(), name='search'),
]

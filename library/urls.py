from django.urls import path

from library import views

app_name = "library"

urlpatterns = [
    # FileのCRUD
    path('', views.FileIndexView.as_view(), name='file_index'),
    path('file/category/<int:category_pk>', views.FileCategoryView.as_view(), name='file_category'),
    path('file/create/', views.FileCreateView.as_view(), name='file_create'),
    path('file/create/<int:pk>', views.FileCreateView.as_view(), name='file_create'),
    path('file/update/<int:pk>', views.FileUpdateView.as_view(), name='file_update'),
    path('file/delete/<int:pk>', views.FileDeleteView.as_view(), name='file_delete'),

    # 間接リンク
    # path('indirect/link/<int:pk>', views.indirect_link, name='indirect_link'),

    # CategoryのCRUD
    path('category/', views.CategoryIndexView.as_view(), name='category_index'),
    path('category/bigcategory/<int:big_pk>', views.CategoryBigView.as_view(), name='category_big'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/create/<int:pk>', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>', views.CategoryDeleteView.as_view(), name='category_delete'),

    # BigCategoryのCRUD
    path('big_category/', views.BigCategoryIndexView.as_view(), name='big_category_index'),
    path('big_category/create/', views.BigCategoryCreateView.as_view(), name='big_category_create'),
    path('big_category/update/<int:pk>', views.BigCategoryUpdateView.as_view(), name='big_category_update'),
    path('big_category/delete/<int:pk>', views.BigCategoryDeleteView.as_view(), name='big_category_delete'),

    # BigCategoruに属するファイルを一覧表示
    path('bigcategory/<int:pk>/', views.BigCategoryView.as_view(), name='bigcategory'),
    # 保管庫メニュー
    path('rijikai_minutes', views.RijikaiMinutesView.as_view(), name='rijikai_minutes'),
    path('rijikai_data', views.RijikaiDataListView.as_view(), name='rijikai_data'),
    path('soukai_rejime', views.SoukaiRejimeListView.as_view(), name='soukai_rejime'),
    # 検索結果表示
    path('search/', views.SearchlistView.as_view(), name='search'),
    # djangoでpdfファイルを配信する。（静的ファイルの配信はnginxで行うべきだが。）
    path('file_view/<int:pk>', views.pdf_view, name='file_view'),
]

from django.urls import path
from . import views


app_name = 'register'
urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('menu/', views.warehouse_menu, name='menu'),
]

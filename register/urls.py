from django.urls import path
from . import views


app_name = 'register'
urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('signup', views.TempUserCreateView.as_view(), name='signup'),
    path('signup_done', views.TempUserDoneView.as_view(), name='temp_user_done'),
    path('list', views.UserListView.as_view(), name='user_list'),
    path('user_update/<int:pk>/', views.UserManagementView.as_view(), name='user_update'),
    path('pwd_update/<int:pk>/', views.UserPasswordUpdate.as_view(), name='pwd_update'),
]

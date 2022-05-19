from django.urls import path
from register.views import views
from register.views import user_views


app_name = 'register'
urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('signup', user_views.TempUserCreateView.as_view(), name='signup'),
    path('signup_done', user_views.TempUserDoneView.as_view(), name='temp_user_done'),
    path('list', user_views.UserListView.as_view(), name='user_list'),
    path('user_update/<int:pk>/', user_views.UserManagementView.as_view(), name='user_update'),
    path('pwd_update/<int:pk>/', user_views.UserPasswordUpdate.as_view(), name='pwd_update'),
    path('control_list', user_views.ControlRecordListView.as_view(), name='control_list'),
    path('control_update/<int:pk>/', user_views.ControlRecordUpdateView.as_view(), name='control_update'),
]

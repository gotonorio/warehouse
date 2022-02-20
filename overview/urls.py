from django.urls import path

from overview import views

app_name = "overview"

urlpatterns = [
    path('overview', views.Overview.as_view(), name='overview'),
]

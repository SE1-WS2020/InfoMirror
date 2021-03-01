from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name="api-overview"),
    path('user-config/', views.userConfigList, name="user-config-list")
]
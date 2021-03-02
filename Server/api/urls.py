from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name="api-overview"),
    path('user-config/', views.user_config_list, name="user-config-list"),
    path('user-config/<int:pk>', views.user_config_detail, name="user-config-detail"),
    path('user-config/<str:username>', views.username_config_detail, name="username_config_detail"),
    path('user-config/create', views.user_config_create, name="user-config-create"),
]
from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.api_overview, name="api-overview"),
    path('user-config/', views.user_config_list, name="user-config-list"),
    path('user-config/<str:user_email>', views.username_config_detail, name="username_config_detail"),
    path('user-config/create/', views.user_config_create, name="user-config-create"),
    path('register/', views.registration_view, name="register"),
    path('login/', obtain_auth_token, name="login"),
    path('login-check/<str:user_email>', views.check_token_validity, name="check token validity"),
    path('upload_image/', views.put_image, name="upload user image"),
    path('download_image/', views.get_image, name="upload user image"),
    path('all_users/', views.get_all_useremails, name="get all user emails"),
    # path('download_images/', views.get_user_images, name="download all user images"),
]

from django.contrib import admin

# Register your models here.
from api.models import UserConfigModel, UserImageModel

admin.site.register(UserConfigModel)
admin.site.register(UserImageModel)
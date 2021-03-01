from rest_framework import serializers
from .models import UserConfig


class UserConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfig
        fields = '__all__'

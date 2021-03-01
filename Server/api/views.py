from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import UserConfig
from .serializers import UserConfigSerializer

# Create your views here.


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'list': '/user-config/',
        'user config(id)': '/user-config/<str:pk>',
        'user config(name)': '/user-config/<str:username>'
    }
    return Response(api_urls)


@api_view(['GET'])
def userConfigList(request):
    configs = UserConfig.objects.all()
    serializer = UserConfigSerializer(configs, many=True)

    return Response(serializer.data)
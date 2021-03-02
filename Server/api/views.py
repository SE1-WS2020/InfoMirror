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
def user_config_list(request):
    configs = UserConfig.objects.all()
    serializer = UserConfigSerializer(configs, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def user_config_detail(request, pk):
    configs = UserConfig.objects.get(id=pk)
    serializer = UserConfigSerializer(configs, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def user_config_create(request):
    serializer = UserConfigSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response("Successfully created config.")
    return Response("Config could not be created.")


@api_view(['GET'])
def username_config_detail(request, username):
    configs = UserConfig.objects.get(username=username)
    serializer = UserConfigSerializer(configs, many=False)

    return Response(serializer.data)

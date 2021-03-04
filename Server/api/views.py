from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from account.models import Account
from .models import UserConfig
from .serializers import UserConfigSerializer, RegistrationSerializer


# Create your views here.

@api_view(['GET'])
@permission_classes(())
def api_overview(request):
    api_urls = {
        'list': '/user-config/',
        'user config(id)': '/user-config/<str:pk>',
        'user config(name)': '/user-config/<str:username>'
    }
    return Response(api_urls)


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def user_config_list(request):
    configs = UserConfig.objects.all()
    serializer = UserConfigSerializer(configs, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def user_config_create(request):
    try:
        # try to get existing config
        existing_config = UserConfig.objects.get(user_account=request.data['user_account'])

        # config already exists
        if existing_config.user_account == request.user or request.user.is_admin:
            existing_config.news_app = True if request.data['news_app'] == 'true' else False
            existing_config.covid_tracker = True if request.data['covid_tracker'] == 'true' else False
            existing_config.traffic_status = True if request.data['traffic_status'] == 'true' else False
            existing_config.weather_app = True if request.data['weather_app'] == 'true' else False

            existing_config.save()
            return Response("Existing config has been updated.")
        else:
            return Response("You have no permissions to update the configuration.")

    except Exception:
        # config does not exist yet
        serializer = UserConfigSerializer(data=request.data)

        if request.data['user_account'] == request.user.email:
            if serializer.is_valid():
                serializer.save()
                return Response("Successfully created config.")
            else:
                return Response("Config could not be created.")
        else:
            return Response("Can not create config for another user.")


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def username_config_detail(request, user_email):
    try:
        configs = UserConfig.objects.get(user_account=user_email)
    except Exception:
        return Response({'response': 'No config exists for this user.'})

    serializer = UserConfigSerializer(configs, many=False)

    user = request.user

    if configs.user_account == user or user.is_admin:
        return Response(serializer.data)

    return Response({'response': 'No permission.'})


@api_view(['POST', ])
@permission_classes(())
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registered a new user"
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def check_token_validity(request, user_email):
    try:
        user = Account.objects.get(email=user_email)
    except Exception:
        return Response({'response': 'Authentication token does not match user email address.'})

    if user == request.user:
        return Response({'response': 'Token ok.'})
    else:
        return Response({'response': 'Authentication token does not match user email address.'})

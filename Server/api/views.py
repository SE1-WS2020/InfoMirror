from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from account.models import Account
from .models import UserConfigModel, UserImageModel
from .serializers import UserConfigSerializer, RegistrationSerializer, ImageSerializer, UserImageEmailSerializer


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
    configs = UserConfigModel.objects.all()
    serializer = UserConfigSerializer(configs, many=True)

    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAdminUser, ))
def get_all_useremails(request):
    all_user_emails = UserImageModel.objects.all()
    serializer = UserImageEmailSerializer(all_user_emails, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def user_config_create(request):
    try:
        # try to get existing config
        existing_config = UserConfigModel.objects.get(user_account=request.data['user_account'])

        # config already exists
        if existing_config.user_account == request.user or request.user.is_superuser:
            existing_config.news_app = True if request.data['news_app'] == 'true' else False
            existing_config.covid_tracker = True if request.data['covid_tracker'] == 'true' else False
            existing_config.traffic_status = True if request.data['traffic_status'] == 'true' else False
            existing_config.weather_app = True if request.data['weather_app'] == 'true' else False

            existing_config.save()
            return Response({"response": "Existing config has been updated."})
        else:
            return Response({"response": "You have no permissions to update the configuration."})

    except Exception:
        # config does not exist yet
        serializer = UserConfigSerializer(data=request.data)

        print(request.data)
        if request.data['user_account'] == request.user.email:
            if serializer.is_valid():
                serializer.save()
                return Response({"response": "Successfully created config."})
            else:
                return Response({"response":"Config could not be created."})
        else:
            return Response({"response":"Can not create config for another user."})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def username_config_detail(request, user_email):
    try:
        configs = UserConfigModel.objects.get(user_account=user_email)
    except Exception:
        return Response({'response': 'No config exists for this user.'})

    serializer = UserConfigSerializer(configs, many=False)

    user = request.user

    if configs.user_account == user or user.is_superuser:
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
        print(request)
        user = Account.objects.get(email=user_email)
    except Exception:
        return Response({'response': 'Authentication token does not match user email address.'})

    if user == request.user:
        return Response({'response': 'Token ok.'})
    else:
        return Response({'response': 'Authentication token does not match user email address.'})



@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def put_image(request):
    user_email = request.data["user_account"]

    try:
        existing_image = UserImageModel.objects.get(user_account=user_email)

        if existing_image.user_account == request.user or request.user.is_superuser:
            existing_image.user_image = request.data['user_image']
            existing_image.save()

            return Response("Existing image has been updated.")
        else:
            return Response("You have no permissions to update that user's image.")
    except:
        if user_email == request.user.email or request.user.is_superuser:
            # image does not exist yet
            serializer = ImageSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response("user image has been updated")
            else:
                return Response(serializer.errors)
        else:
            return Response("You have no permissions to update that user's image.")


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_image(request):
    user_email = request.data["user_account"]

    if request.user.email == user_email or request.user.is_superuser:
        existing_image = UserImageModel.objects.get(user_account=user_email)
        return HttpResponse(existing_image.user_image, content_type="image/png")
    else:
        return Response("You have no permissions.")

"""
@api_view(['GET', ])
@permission_classes((IsAdminUser, ))
def get_user_images(request):
    user_images = UserImageModel.objects.all()

    for image in user_images:
        print(image.user_account)
        print(image.user_image)

    serializer = ImageSerializer(user_images, many=True)

    return JsonResponse(serializer.data, safe=False)
"""
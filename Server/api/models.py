from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
from account.models import Account


IMAGE_FILE_PATH = "user_images/"


class UserConfigModel(models.Model):
    user_account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    news_app = models.BooleanField()
    covid_tracker = models.BooleanField()
    traffic_status = models.BooleanField()
    weather_app = models.BooleanField()

    def __str__(self):
        return self.user_account.email


class UserImageModel(models.Model):
    user_account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    user_image = models.ImageField(upload_to=IMAGE_FILE_PATH)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


class UserConfig(models.Model):
    username = models.CharField(max_length=64)
    news_app = models.BooleanField()
    covid_tracker = models.BooleanField()
    traffic_status = models.BooleanField()
    weather_app = models.BooleanField()

    def __str__(self):
        return self.username + "'s config"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
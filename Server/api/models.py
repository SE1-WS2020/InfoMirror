from django.db import models

# Create your models here.


class UserConfig(models.Model):
    username = models.CharField(max_length=64)
    news_app = models.BooleanField()
    covid_tracker = models.BooleanField()
    traffic_status = models.BooleanField()
    weather_app = models.BooleanField()

    def __str__(self):
        return self.username + "'s config"

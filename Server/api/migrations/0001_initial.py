# Generated by Django 3.1.4 on 2021-03-01 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('news_app', models.BooleanField()),
                ('covid_tracker', models.BooleanField()),
                ('traffic_status', models.BooleanField()),
                ('weather_app', models.BooleanField()),
            ],
        ),
    ]

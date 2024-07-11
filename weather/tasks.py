from celery import shared_task
from django.core.mail import send_mail
from .models import Location
from weather.services import WeatherService
from django.contrib.auth.models import User

@shared_task
def send_daily_weather_email():
    users = User.objects.all()
    for user in users:
        locations = Location.objects.filter(user=user)
        weather_reports = []
        for location in locations:
            weather_data = WeatherService.get_forecast(location.name)
            if weather_data:
                weather_reports.append(f"Location: {location.name}, Temperature: {weather_data['current']['temp_c']}°C")

        if weather_reports:
            email_body = '\n'.join(weather_reports)
            send_mail(
                'Daily Weather Report',
                email_body,
                'your_email@example.com',
                [user.email],
                fail_silently=False,
            )
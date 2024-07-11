import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_project.settings")
django.setup()
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status


class WeatherTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        print(f"Token created: {self.token.key}")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    @patch("weather.services.requests.get")
    def test_current_weather(self, mock_get):
        mock_get.return_value.json.return_value = {
            "location": "Chennai",
            "current": {"temp_c": 30},
        }
        url = reverse("current_weather", kwargs={"location": "chennai"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["location"], "Chennai")

    def test_current_weather_integration(self):
        # Prepare a URL for the current_weather endpoint, replacing 'chennai' with your desired location
        location = "chennai"
        url = reverse("current_weather", kwargs={"location": location})

        # Perform a GET request to the endpoint
        response = self.client.get(url)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the structure or content of the response as needed
        self.assertIn("current", response.data)
        print(response.data)
        self.assertEqual(response.data["location"]["name"], "Chennai")

    @patch("weather.services.requests.get")
    def test_forecast_weather(self, mock_get):
        mock_get.return_value.json.return_value = {
            "location": "Chennai",
            "forecast": {"forecastday": [{"day": {"maxtemp_c": 25}}]},
        }
        response = self.client.get(
            reverse("forecast_weather", kwargs={"location": "London", "days": 3})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["location"], "Chennai")

    def test_forecast_weather_integration(
        self,
    ):
        response = self.client.get(
            reverse("forecast_weather", kwargs={"location": "London", "days": 3})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["location"]["name"], "London")

    def test_user_registration(self):
        response = self.client.post(
            reverse("register"), {"username": "newuser", "password": "newpassword"}
        )
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)

from django.urls import path
from .views import RegisterUserView, LoginView, CurrentWeatherView, ForecastWeatherView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Weather API",
        default_version="v1",
        description="API documentation for the weather service",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "weather/current/<str:location>/",
        CurrentWeatherView.as_view(),
        name="current_weather",
    ),
    path(
        "weather/forecast/<str:location>/<int:days>/",
        ForecastWeatherView.as_view(),
        name="forecast_weather",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

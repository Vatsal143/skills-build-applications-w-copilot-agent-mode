"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path


def get_api_base_url(request):
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        return f'https://{codespace_name}-8000.app.github.dev'
    return request.build_absolute_uri('/').rstrip('/')


def api_root(request):
    base_url = get_api_base_url(request)
    return JsonResponse({
        'activities': f'{base_url}/api/activities/',
        'users': f'{base_url}/api/users/',
        'teams': f'{base_url}/api/teams/',
        'leaderboard': f'{base_url}/api/leaderboard/',
        'workouts': f'{base_url}/api/workouts/',
    })


def api_component(request, component):
    base_url = get_api_base_url(request)
    return JsonResponse({
        'endpoint': f'{base_url}/api/{component}/',
        'component': component,
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/<str:component>/', api_component),
]

"""
URL configuration for task_management project.
"""
from django.contrib import admin
from django.urls import path, include
from tasks.home_views import home, api_info

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('tasks.api_urls')),
    path('api-info/', api_info, name='api_info'),
    path('panel/', include('tasks.panel_urls')),
]


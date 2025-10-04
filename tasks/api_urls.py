from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .api_views import (
    CustomTokenObtainPairView,
    get_tasks,
    update_task,
    get_task_report
)

urlpatterns = [
    # JWT Authentication endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Task API endpoints
    path('tasks/', get_tasks, name='api_get_tasks'),
    path('tasks/<int:id>/', update_task, name='api_update_task'),
    path('tasks/<int:id>/report/', get_task_report, name='api_task_report'),
]


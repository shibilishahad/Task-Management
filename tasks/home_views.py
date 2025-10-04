from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    """
    Homepage with links to admin panel and API documentation
    """
    return render(request, 'home.html')

def api_info(request):
    """
    API information endpoint
    """
    api_info = {
        "message": "Task Management API",
        "version": "1.0",
        "endpoints": {
            "authentication": {
                "POST /api/token/": "Get JWT access and refresh tokens",
                "POST /api/token/refresh/": "Refresh JWT access token"
            },
            "tasks": {
                "GET /api/tasks/": "Get user's assigned tasks",
                "PUT /api/tasks/{id}/": "Update task status",
                "GET /api/tasks/{id}/report/": "View task completion report (Admin/SuperAdmin only)"
            }
        },
        "admin_panel": "/panel/login/",
        "documentation": {
            "setup_guide": "See setup_guide.md",
            "api_testing": "See API_TESTING_GUIDE.md",
            "quick_reference": "See QUICK_REFERENCE.md"
        }
    }
    return JsonResponse(api_info, json_dumps_params={'indent': 2})

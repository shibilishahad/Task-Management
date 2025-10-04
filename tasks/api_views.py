from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Task
from .serializers import (
    TaskSerializer, 
    TaskUpdateSerializer, 
    TaskReportSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT Token view - Returns JWT tokens for authentication
    """
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    """
    GET /api/tasks
    Fetch all tasks assigned to the logged-in user
    Only returns tasks for the logged user who is sending the request
    """
    # Only regular users can access this endpoint
    if not request.user.is_regular_user():
        return Response(
            {'error': 'This endpoint is only accessible to regular users.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    tasks = Task.objects.filter(assigned_to=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, id):
    """
    PUT /api/tasks/{id}
    Allows users to update the status of a task (mark it as Completed)
    When setting a task status to Completed, users are required to submit
    a Completion Report and the number of Worked Hours
    """
    # Only regular users can access this endpoint
    if not request.user.is_regular_user():
        return Response(
            {'error': 'This endpoint is only accessible to regular users.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        task = Task.objects.get(id=id, assigned_to=request.user)
    except Task.DoesNotExist:
        return Response(
            {'error': 'Task not found or you do not have permission to update this task.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                'message': 'Task updated successfully.',
                'task': TaskSerializer(task).data
            },
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_report(request, id):
    """
    GET /api/tasks/{id}/report
    Admins and SuperAdmins can view the Completion Report and Worked Hours for a specific task
    This is only available for tasks that are marked as Completed
    """
    # Only admins and superadmins can access this endpoint
    if not (request.user.is_admin() or request.user.is_superadmin()):
        return Response(
            {'error': 'This endpoint is only accessible to Admins and SuperAdmins.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        task = Task.objects.get(id=id)
        
        # If admin, check if task is assigned to one of their users
        if request.user.is_admin():
            if not task.assigned_to.assigned_to_admin == request.user:
                return Response(
                    {'error': 'You do not have permission to view this task report.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
    except Task.DoesNotExist:
        return Response(
            {'error': 'Task not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if task is completed
    if task.status != 'completed':
        return Response(
            {'error': 'Task report is only available for completed tasks.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = TaskReportSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


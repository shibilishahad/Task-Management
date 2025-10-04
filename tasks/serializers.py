from rest_framework import serializers
from .models import Task, CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User information
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id', 'role']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task listing
    """
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_to_username',
            'due_date', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'assigned_to']


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating task status with completion report
    """
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']
    
    def validate(self, data):
        """
        Validate that completion_report and worked_hours are provided when status is 'completed'
        """
        if data.get('status') == 'completed':
            if not data.get('completion_report'):
                raise serializers.ValidationError({
                    'completion_report': 'Completion report is required when marking task as completed.'
                })
            if not data.get('worked_hours'):
                raise serializers.ValidationError({
                    'worked_hours': 'Worked hours are required when marking task as completed.'
                })
            if data.get('worked_hours') and data['worked_hours'] <= 0:
                raise serializers.ValidationError({
                    'worked_hours': 'Worked hours must be greater than 0.'
                })
        return data


class TaskReportSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing task completion report
    """
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    assigned_to_email = serializers.CharField(source='assigned_to.email', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to_username', 'assigned_to_email',
            'due_date', 'status', 'completion_report', 'worked_hours', 
            'created_at', 'updated_at'
        ]
        read_only_fields = fields


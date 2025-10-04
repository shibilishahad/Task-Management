"""
Sample Data Creation Script for Task Management Application

This script creates sample users, admins, and tasks for testing purposes.
Run this after setting up the database and creating a superadmin.

Usage: python manage.py shell < create_sample_data.py
Or: python create_sample_data.py (if Django is configured)
"""

import os
import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

from tasks.models import CustomUser, Task

def create_sample_data():
    print("Creating sample data...")
    
    # Create SuperAdmin (if not exists)
    superadmin, created = CustomUser.objects.get_or_create(
        username='superadmin',
        defaults={
            'email': 'superadmin@example.com',
            'role': 'superadmin',
            'first_name': 'Super',
            'last_name': 'Admin',
        }
    )
    if created:
        superadmin.set_password('super123456')
        superadmin.save()
        print(f"✓ Created SuperAdmin: {superadmin.username} (Password: super123456)")
    else:
        print(f"✓ SuperAdmin already exists: {superadmin.username}")
    
    # Create Admins
    admins = []
    for i in range(1, 3):
        admin, created = CustomUser.objects.get_or_create(
            username=f'admin{i}',
            defaults={
                'email': f'admin{i}@example.com',
                'role': 'admin',
                'first_name': f'Admin',
                'last_name': f'User{i}',
            }
        )
        if created:
            admin.set_password(f'admin{i}123456')
            admin.save()
            print(f"✓ Created Admin: {admin.username} (Password: admin{i}123456)")
        else:
            print(f"✓ Admin already exists: {admin.username}")
        admins.append(admin)
    
    # Create Regular Users
    users = []
    for i in range(1, 6):
        user, created = CustomUser.objects.get_or_create(
            username=f'user{i}',
            defaults={
                'email': f'user{i}@example.com',
                'role': 'user',
                'first_name': f'User',
                'last_name': f'Test{i}',
                'assigned_to_admin': admins[(i-1) % len(admins)]  # Distribute users among admins
            }
        )
        if created:
            user.set_password(f'user{i}123456')
            user.save()
            print(f"✓ Created User: {user.username} (Password: user{i}123456) - Assigned to {user.assigned_to_admin.username}")
        else:
            print(f"✓ User already exists: {user.username}")
        users.append(user)
    
    # Create Sample Tasks
    task_templates = [
        {
            'title': 'Develop Login Feature',
            'description': 'Implement user authentication with JWT tokens',
            'status': 'pending'
        },
        {
            'title': 'Design Database Schema',
            'description': 'Create ERD and design database tables for the application',
            'status': 'in_progress'
        },
        {
            'title': 'Write API Documentation',
            'description': 'Document all API endpoints with request/response examples',
            'status': 'pending'
        },
        {
            'title': 'Setup CI/CD Pipeline',
            'description': 'Configure automated testing and deployment pipeline',
            'status': 'completed',
            'completion_report': 'Successfully set up GitHub Actions for automated testing and deployment. Pipeline runs on every push and pull request.',
            'worked_hours': 6.5
        },
        {
            'title': 'Implement Password Reset',
            'description': 'Add functionality for users to reset forgotten passwords',
            'status': 'in_progress'
        },
    ]
    
    tasks_created = 0
    for i, template in enumerate(task_templates):
        user = users[i % len(users)]
        task, created = Task.objects.get_or_create(
            title=template['title'],
            assigned_to=user,
            defaults={
                'description': template['description'],
                'status': template['status'],
                'due_date': date.today() + timedelta(days=(i+1)*7),
                'created_by': user.assigned_to_admin,
                'completion_report': template.get('completion_report'),
                'worked_hours': template.get('worked_hours'),
            }
        )
        if created:
            tasks_created += 1
            print(f"✓ Created Task: '{task.title}' - Assigned to {user.username}")
        else:
            print(f"✓ Task already exists: '{task.title}'")
    
    print("\n" + "="*60)
    print("Sample Data Creation Complete!")
    print("="*60)
    print("\n📊 Summary:")
    print(f"  - SuperAdmins: 1")
    print(f"  - Admins: {len(admins)}")
    print(f"  - Users: {len(users)}")
    print(f"  - Tasks: {tasks_created + Task.objects.count() - tasks_created}")
    
    print("\n🔐 Login Credentials:")
    print("\nSuperAdmin:")
    print("  Username: superadmin")
    print("  Password: super123456")
    print("  Panel URL: http://127.0.0.1:8000/panel/login/")
    
    print("\nAdmins:")
    for i in range(1, 3):
        print(f"  Username: admin{i}, Password: admin{i}123456")
    
    print("\nUsers (for API access):")
    for i in range(1, 6):
        print(f"  Username: user{i}, Password: user{i}123456")
    
    print("\n🚀 Next Steps:")
    print("  1. Run: python manage.py runserver")
    print("  2. Visit: http://127.0.0.1:8000/panel/login/")
    print("  3. Login with superadmin credentials")
    print("  4. Test API with user credentials")
    print("\n✨ Happy Testing!\n")

if __name__ == '__main__':
    create_sample_data()


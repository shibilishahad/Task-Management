from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .models import CustomUser, Task
from datetime import datetime


def panel_login(request):
    """
    Login page for Admin Panel
    """
    if request.user.is_authenticated:
        if request.user.is_superadmin():
            return redirect('superadmin_dashboard')
        elif request.user.is_admin():
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Only Admins and SuperAdmins can access the panel.')
            logout(request)
            return redirect('panel_login')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_admin() or user.is_superadmin():
                login(request, user)
                if user.is_superadmin():
                    return redirect('superadmin_dashboard')
                else:
                    return redirect('admin_dashboard')
            else:
                messages.error(request, 'Only Admins and SuperAdmins can access the panel.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'panel/login.html')


@login_required(login_url='panel_login')
def panel_logout(request):
    """
    Logout from Admin Panel
    """
    # Clear session data completely
    request.session.flush()
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('panel_login')


# ==================== SUPERADMIN VIEWS ====================

@login_required(login_url='panel_login')
def superadmin_dashboard(request):
    """
    SuperAdmin Dashboard - Overview of all users, admins, and tasks
    """
    if not request.user.is_superadmin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    total_admins = CustomUser.objects.filter(role='admin').count()
    total_users = CustomUser.objects.filter(role='user').count()
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    
    context = {
        'total_admins': total_admins,
        'total_users': total_users,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'panel/superadmin/dashboard.html', context)


@login_required(login_url='panel_login')
def superadmin_manage_admins(request):
    """
    SuperAdmin - View and manage all admins
    """
    if not request.user.is_superadmin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    admins = CustomUser.objects.filter(role='admin').order_by('-date_joined')
    context = {'admins': admins}
    return render(request, 'panel/superadmin/manage_admins.html', context)


@login_required(login_url='panel_login')
def superadmin_create_admin(request):
    """
    SuperAdmin - Create a new admin
    """
    if not request.user.is_superadmin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            admin = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='admin'
            )
            messages.success(request, f'Admin "{username}" created successfully.')
            return redirect('superadmin_manage_admins')
    
    return render(request, 'panel/superadmin/create_admin.html')


@login_required(login_url='panel_login')
def superadmin_delete_admin(request, admin_id):
    """
    SuperAdmin - Delete an admin
    """
    if not request.user.is_superadmin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    admin = get_object_or_404(CustomUser, id=admin_id, role='admin')
    
    if request.method == 'POST':
        username = admin.username
        admin.delete()
        messages.success(request, f'Admin "{username}" deleted successfully.')
        return redirect('superadmin_manage_admins')
    
    context = {'admin': admin}
    return render(request, 'panel/superadmin/delete_admin.html', context)


@login_required(login_url='panel_login')
def superadmin_manage_users(request):
    """
    SuperAdmin - View and manage all users
    """
    if not request.user.is_superadmin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    users = CustomUser.objects.filter(role='user').order_by('-date_joined')
    context = {'users': users}
    return render(request, 'panel/superadmin/manage_users.html', context)


@login_required(login_url='panel_login')
def superadmin_create_user(request):
    """
    SuperAdmin - Create a new user
    """
    if not request.user.is_superadmin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    admins = CustomUser.objects.filter(role='admin')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        assigned_admin_id = request.POST.get('assigned_to_admin')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='user'
            )
            
            if assigned_admin_id:
                user.assigned_to_admin_id = assigned_admin_id
                user.save()
            
            messages.success(request, f'User "{username}" created successfully.')
            return redirect('superadmin_manage_users')
    
    context = {'admins': admins}
    return render(request, 'panel/superadmin/create_user.html', context)


@login_required(login_url='panel_login')
def superadmin_edit_user(request, user_id):
    """
    SuperAdmin - Edit user details and assign to admin
    """
    if not request.user.is_superadmin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    user = get_object_or_404(CustomUser, id=user_id, role='user')
    admins = CustomUser.objects.filter(role='admin')
    
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        assigned_admin_id = request.POST.get('assigned_to_admin')
        
        if assigned_admin_id:
            user.assigned_to_admin_id = assigned_admin_id
        else:
            user.assigned_to_admin = None
        
        user.save()
        messages.success(request, f'User "{user.username}" updated successfully.')
        return redirect('superadmin_manage_users')
    
    context = {'user': user, 'admins': admins}
    return render(request, 'panel/superadmin/edit_user.html', context)


@login_required(login_url='panel_login')
def superadmin_delete_user(request, user_id):
    """
    SuperAdmin - Delete a user
    """
    if not request.user.is_superadmin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    user = get_object_or_404(CustomUser, id=user_id, role='user')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" deleted successfully.')
        return redirect('superadmin_manage_users')
    
    context = {'user': user}
    return render(request, 'panel/superadmin/delete_user.html', context)


@login_required(login_url='panel_login')
def superadmin_manage_tasks(request):
    """
    SuperAdmin - View and manage all tasks
    """
    if not request.user.is_superadmin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    tasks = Task.objects.all().order_by('-created_at')
    context = {'tasks': tasks}
    return render(request, 'panel/superadmin/manage_tasks.html', context)


@login_required(login_url='panel_login')
def superadmin_view_task_report(request, task_id):
    """
    SuperAdmin - View task completion report
    """
    if not request.user.is_superadmin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    task = get_object_or_404(Task, id=task_id)
    
    if task.status != 'completed':
        messages.warning(request, 'This task is not completed yet.')
    
    context = {'task': task}
    return render(request, 'panel/superadmin/view_task_report.html', context)


# ==================== ADMIN VIEWS ====================

@login_required(login_url='panel_login')
def admin_dashboard(request):
    """
    Admin Dashboard - Overview of assigned users and tasks
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    my_users = CustomUser.objects.filter(assigned_to_admin=request.user, role='user')
    my_tasks = Task.objects.filter(assigned_to__assigned_to_admin=request.user)
    completed_tasks = my_tasks.filter(status='completed').count()
    
    context = {
        'total_users': my_users.count(),
        'total_tasks': my_tasks.count(),
        'completed_tasks': completed_tasks,
    }
    return render(request, 'panel/admin/dashboard.html', context)


@login_required(login_url='panel_login')
def admin_view_users(request):
    """
    Admin - View users assigned to this admin
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    users = CustomUser.objects.filter(assigned_to_admin=request.user, role='user').order_by('-date_joined')
    
    # Add task counts for each user
    users_with_counts = []
    for user in users:
        total_tasks = user.tasks.count()
        completed_tasks = user.tasks.filter(status='completed').count()
        users_with_counts.append({
            'user': user,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks
        })
    
    context = {'users_with_counts': users_with_counts}
    return render(request, 'panel/admin/view_users.html', context)


@login_required(login_url='panel_login')
def admin_manage_tasks(request):
    """
    Admin - View and manage tasks assigned to their users
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    tasks = Task.objects.filter(assigned_to__assigned_to_admin=request.user).order_by('-created_at')
    context = {'tasks': tasks}
    return render(request, 'panel/admin/manage_tasks.html', context)


@login_required(login_url='panel_login')
def admin_create_task(request):
    """
    Admin - Create and assign a task to their users
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    users = CustomUser.objects.filter(assigned_to_admin=request.user, role='user')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        status_value = request.POST.get('status', 'pending')
        
        task = Task.objects.create(
            title=title,
            description=description,
            assigned_to_id=assigned_to_id,
            created_by=request.user,
            due_date=due_date,
            status=status_value
        )
        messages.success(request, f'Task "{title}" created successfully.')
        return redirect('admin_manage_tasks')
    
    context = {'users': users}
    return render(request, 'panel/admin/create_task.html', context)


@login_required(login_url='panel_login')
def admin_edit_task(request, task_id):
    """
    Admin - Edit a task assigned to their users
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    task = get_object_or_404(Task, id=task_id, assigned_to__assigned_to_admin=request.user)
    users = CustomUser.objects.filter(assigned_to_admin=request.user, role='user')
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.assigned_to_id = request.POST.get('assigned_to')
        task.due_date = request.POST.get('due_date')
        task.status = request.POST.get('status')
        task.save()
        
        messages.success(request, f'Task "{task.title}" updated successfully.')
        return redirect('admin_manage_tasks')
    
    context = {'task': task, 'users': users}
    return render(request, 'panel/admin/edit_task.html', context)


@login_required(login_url='panel_login')
def admin_delete_task(request, task_id):
    """
    Admin - Delete a task assigned to their users
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    task = get_object_or_404(Task, id=task_id, assigned_to__assigned_to_admin=request.user)
    
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted successfully.')
        return redirect('admin_manage_tasks')
    
    context = {'task': task}
    return render(request, 'panel/admin/delete_task.html', context)


@login_required(login_url='panel_login')
def admin_view_task_report(request, task_id):
    """
    Admin - View completion report for tasks assigned to their users
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('panel_login')
    
    task = get_object_or_404(Task, id=task_id, assigned_to__assigned_to_admin=request.user)
    
    if task.status != 'completed':
        messages.warning(request, 'This task is not completed yet.')
    
    context = {'task': task}
    return render(request, 'panel/admin/view_task_report.html', context)


# ==================== USER LOGIN VIEWS ====================

def user_login(request):
    """
    Login page for Regular Users
    """
    if request.user.is_authenticated:
        if request.user.is_regular_user():
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Only regular users can access this page.')
            logout(request)
            return redirect('user_login')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_regular_user():
                login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Only regular users can access this page.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    response = render(request, 'panel/user/login.html')
    # Add cache control headers to prevent caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required(login_url='user_login')
def user_dashboard(request):
    """
    User Dashboard - View assigned tasks
    """
    if not request.user.is_regular_user():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('user_login')
    
    # Get user's tasks
    tasks = Task.objects.filter(assigned_to=request.user).order_by('-created_at')
    
    # Calculate statistics
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    pending_tasks = tasks.filter(status='pending').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    
    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
    }
    
    response = render(request, 'panel/user/dashboard.html', context)
    # Add cache control headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required(login_url='user_login')
def user_view_task(request, task_id):
    """
    User - View task details
    """
    if not request.user.is_regular_user():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('user_login')
    
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    context = {'task': task}
    return render(request, 'panel/user/view_task.html', context)


@login_required(login_url='user_login')
def user_update_task(request, task_id):
    """
    User - Update task status
    """
    if not request.user.is_regular_user():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('user_login')
    
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        completion_report = request.POST.get('completion_report', '')
        worked_hours = request.POST.get('worked_hours', '')
        
        # Validate completion report and worked hours for completed tasks
        if status == 'completed':
            if not completion_report.strip():
                messages.error(request, 'Completion report is required when marking task as completed.')
                return redirect('user_view_task', task_id=task_id)
            if not worked_hours or float(worked_hours) <= 0:
                messages.error(request, 'Worked hours must be greater than 0 when marking task as completed.')
                return redirect('user_view_task', task_id=task_id)
        
        # Update task
        task.status = status
        if status == 'completed':
            task.completion_report = completion_report
            task.worked_hours = float(worked_hours)
        else:
            # Clear completion data if not completed
            task.completion_report = ''
            task.worked_hours = None
        
        task.save()
        messages.success(request, f'Task "{task.title}" updated successfully!')
        return redirect('user_view_task', task_id=task_id)
    
    return redirect('user_view_task', task_id=task_id)


@login_required(login_url='user_login')
def user_logout(request):
    """
    Logout from User Panel
    """
    # Clear session data completely
    request.session.flush()
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    response = redirect('user_login')
    # Add aggressive cache control headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['Last-Modified'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    return response


from django.urls import path
from .panel_views import (
    panel_login,
    panel_logout,
    # SuperAdmin URLs
    superadmin_dashboard,
    superadmin_manage_admins,
    superadmin_create_admin,
    superadmin_delete_admin,
    superadmin_manage_users,
    superadmin_create_user,
    superadmin_edit_user,
    superadmin_delete_user,
    superadmin_manage_tasks,
    superadmin_view_task_report,
    # Admin URLs
    admin_dashboard,
    admin_view_users,
    admin_manage_tasks,
    admin_create_task,
    admin_edit_task,
    admin_delete_task,
    admin_view_task_report,
    # User URLs
    user_login,
    user_dashboard,
    user_view_task,
    user_update_task,
    user_logout,
)

urlpatterns = [
    # Authentication
    path('login/', panel_login, name='panel_login'),
    path('logout/', panel_logout, name='panel_logout'),
    
    # SuperAdmin URLs
    path('superadmin/dashboard/', superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin/admins/', superadmin_manage_admins, name='superadmin_manage_admins'),
    path('superadmin/admins/create/', superadmin_create_admin, name='superadmin_create_admin'),
    path('superadmin/admins/<int:admin_id>/delete/', superadmin_delete_admin, name='superadmin_delete_admin'),
    path('superadmin/users/', superadmin_manage_users, name='superadmin_manage_users'),
    path('superadmin/users/create/', superadmin_create_user, name='superadmin_create_user'),
    path('superadmin/users/<int:user_id>/edit/', superadmin_edit_user, name='superadmin_edit_user'),
    path('superadmin/users/<int:user_id>/delete/', superadmin_delete_user, name='superadmin_delete_user'),
    path('superadmin/tasks/', superadmin_manage_tasks, name='superadmin_manage_tasks'),
    path('superadmin/tasks/<int:task_id>/report/', superadmin_view_task_report, name='superadmin_view_task_report'),
    
    # Admin URLs
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/users/', admin_view_users, name='admin_view_users'),
    path('admin/tasks/', admin_manage_tasks, name='admin_manage_tasks'),
    path('admin/tasks/create/', admin_create_task, name='admin_create_task'),
    path('admin/tasks/<int:task_id>/edit/', admin_edit_task, name='admin_edit_task'),
    path('admin/tasks/<int:task_id>/delete/', admin_delete_task, name='admin_delete_task'),
    path('admin/tasks/<int:task_id>/report/', admin_view_task_report, name='admin_view_task_report'),
    
    # User URLs
    path('user/login/', user_login, name='user_login'),
    path('user/logout/', user_logout, name='user_logout'),
    path('user/dashboard/', user_dashboard, name='user_dashboard'),
    path('user/tasks/<int:task_id>/', user_view_task, name='user_view_task'),
    path('user/tasks/<int:task_id>/update/', user_update_task, name='user_update_task'),
]


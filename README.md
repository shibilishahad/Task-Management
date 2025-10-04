# Task Management System

A professional task management application built with Django, featuring role-based access control and comprehensive task tracking with completion reports.

## Features

### User Roles and Permissions

#### SuperAdmin
- Manage all admins (create, delete, assign roles)
- Manage all users (create, delete, update, assign to admins)
- View and manage all tasks across the system
- View all task completion reports
- Full access to the Admin Panel

#### Admin
- Create and assign tasks to their assigned users
- View and manage tasks for their users
- View completion reports for tasks (including worked hours)
- Limited access to Admin Panel (cannot manage users/admins)

#### User (Regular User)
- View tasks assigned to them via API
- Update task status and submit completion reports
- Interact with tasks only through the User API

### API Endpoints

#### Authentication
- **POST** `/api/token/` - Obtain JWT access and refresh tokens
- **POST** `/api/token/refresh/` - Refresh JWT access token

#### Tasks
- **GET** `/api/tasks/` - Fetch all tasks assigned to the logged-in user
- **PUT** `/api/tasks/{id}/` - Update task status (requires completion report and worked hours when marking as completed)
- **GET** `/api/tasks/{id}/report/` - View completion report (Admins and SuperAdmins only)

### Admin Panel
- Custom web interface for SuperAdmins and Admins
- Beautiful, modern UI with responsive design
- Dashboard with statistics and quick actions
- Full CRUD operations for managing users, admins, and tasks

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project
```bash
cd taskkkk
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create a SuperAdmin User
```bash
python manage.py createsuperuser
```
Follow the prompts to create your first superadmin account. Make sure to set the role to 'superadmin' after creation (see Additional Setup below).

### Step 6: Set SuperAdmin Role (Important!)
After creating the superuser, you need to manually set their role to 'superadmin':

```bash
python manage.py shell
```

Then in the Python shell:
```python
from tasks.models import CustomUser
user = CustomUser.objects.get(username='your_username_here')
user.role = 'superadmin'
user.save()
exit()
```

### Step 7: Run the Development Server
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## Usage

### Admin Panel Access
1. Navigate to: `http://127.0.0.1:8000/panel/login/`
2. Login with your SuperAdmin credentials
3. You'll be redirected to the SuperAdmin Dashboard

### SuperAdmin Workflow
1. **Create Admins**: Go to "Manage Admins" → "Create New Admin"
2. **Create Users**: Go to "Manage Users" → "Create New User"
3. **Assign Users to Admins**: When creating/editing users, select an admin from the dropdown
4. **View All Tasks and Reports**: Access from "Manage Tasks"

### Admin Workflow
1. Login to the Admin Panel with your admin credentials
2. **View Assigned Users**: Check which users are assigned to you
3. **Create Tasks**: Go to "Manage Tasks" → "Create New Task"
4. **Assign Tasks**: Select a user from your assigned users
5. **View Completion Reports**: Once users complete tasks, view their reports

### User Workflow (API)

#### 1. Obtain JWT Token
```bash
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
    "username": "user_username",
    "password": "user_password"
}
```

Response:
```json
{
    "refresh": "refresh_token_here",
    "access": "access_token_here"
}
```

#### 2. Get My Tasks
```bash
GET http://127.0.0.1:8000/api/tasks/
Authorization: Bearer your_access_token_here
```

#### 3. Update Task Status (Complete a Task)
```bash
PUT http://127.0.0.1:8000/api/tasks/1/
Authorization: Bearer your_access_token_here
Content-Type: application/json

{
    "status": "completed",
    "completion_report": "Task completed successfully. Implemented all required features and tested thoroughly.",
    "worked_hours": 8.5
}
```

#### 4. Admin/SuperAdmin: View Task Report
```bash
GET http://127.0.0.1:8000/api/tasks/1/report/
Authorization: Bearer admin_or_superadmin_access_token_here
```

## Database Models

### CustomUser Model
- `username` - Unique username
- `email` - User email
- `role` - User role (superadmin, admin, user)
- `assigned_to_admin` - Foreign key to Admin (for regular users)
- Standard Django user fields (password, first_name, last_name, etc.)

### Task Model
- `title` - Task title
- `description` - Detailed task description
- `assigned_to` - Foreign key to User
- `created_by` - Foreign key to Admin/SuperAdmin who created the task
- `due_date` - Task deadline
- `status` - Current status (pending, in_progress, completed)
- `completion_report` - Text report submitted when completing task
- `worked_hours` - Hours worked on the task (decimal)
- `created_at` - Timestamp of task creation
- `updated_at` - Timestamp of last update

## Project Structure
```
taskkkk/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3 (created after migrations)
├── task_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tasks/
│   ├── __init__.py
│   ├── models.py
│   ├── admin.py
│   ├── apps.py
│   ├── serializers.py
│   ├── api_views.py
│   ├── api_urls.py
│   ├── panel_views.py
│   └── panel_urls.py
└── templates/
    └── panel/
        ├── base.html
        ├── login.html
        ├── superadmin/
        │   ├── dashboard.html
        │   ├── manage_admins.html
        │   ├── create_admin.html
        │   ├── delete_admin.html
        │   ├── manage_users.html
        │   ├── create_user.html
        │   ├── edit_user.html
        │   ├── delete_user.html
        │   ├── manage_tasks.html
        │   └── view_task_report.html
        └── admin/
            ├── dashboard.html
            ├── view_users.html
            ├── manage_tasks.html
            ├── create_task.html
            ├── edit_task.html
            ├── delete_task.html
            └── view_task_report.html
```

## Testing the Application

### Using Postman/Thunder Client/curl

1. **Get JWT Token**:
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

2. **Get User Tasks**:
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

3. **Complete a Task**:
```bash
curl -X PUT http://127.0.0.1:8000/api/tasks/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "completion_report": "Task completed with all requirements met.",
    "worked_hours": 5.5
  }'
```

## Security Features

- JWT-based authentication for API endpoints
- Role-based access control (RBAC)
- Session-based authentication for Admin Panel
- Password hashing using Django's built-in authentication
- CSRF protection for web forms
- Authorization checks at every endpoint

## Development Notes

- Database: SQLite (configured by default)
- Framework: Django 4.2.7
- API Framework: Django REST Framework 3.14.0
- Authentication: Simple JWT 5.3.0
- Frontend: Custom HTML/CSS templates (no external frameworks)

## Troubleshooting

### Issue: "No module named 'tasks'"
**Solution**: Make sure you're in the project root directory and have run migrations.

### Issue: Can't login to Admin Panel
**Solution**: Ensure user role is set correctly in the database. Only 'admin' and 'superadmin' roles can access the panel.

### Issue: JWT Token Invalid
**Solution**: Token may have expired. Request a new token using the `/api/token/` endpoint.

### Issue: Can't see completion report
**Solution**: Completion reports are only visible for tasks with status='completed'.




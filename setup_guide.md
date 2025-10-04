# Quick Setup Guide

## Step-by-Step Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Database Tables
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create SuperAdmin Account
```bash
python manage.py createsuperuser
```
- Enter username (e.g., `superadmin`)
- Enter email (e.g., `admin@example.com`)
- Enter password (at least 8 characters)

### 4. Set SuperAdmin Role
```bash
python manage.py shell
```

In the Python shell, run:
```python
from tasks.models import CustomUser
user = CustomUser.objects.get(username='superadmin')  # Replace with your username
user.role = 'superadmin'
user.save()
print(f"User {user.username} is now a SuperAdmin!")
exit()
```

### 5. Start the Server
```bash
python manage.py runserver
```

### 6. Access the Admin Panel
Open your browser and navigate to:
```
http://127.0.0.1:8000/panel/login/
```

Login with your superadmin credentials.

## Quick Test Flow

### SuperAdmin Actions:
1. Create an Admin user:
   - Go to "Manage Admins" → "Create New Admin"
   - Username: `admin1`, Password: `admin123456`

2. Create a regular User:
   - Go to "Manage Users" → "Create New User"
   - Username: `user1`, Password: `user123456`
   - Assign to `admin1`

### Admin Actions (Login as admin1):
1. Login to panel with admin1 credentials
2. Create a task for user1:
   - Go to "Manage Tasks" → "Create New Task"
   - Fill in task details
   - Assign to `user1`

### User Actions (API):

1. **Get JWT Token:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"user1\", \"password\": \"user123456\"}"
```

2. **View My Tasks:**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

3. **Complete a Task:**
```bash
curl -X PUT http://127.0.0.1:8000/api/tasks/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"status\": \"completed\", \"completion_report\": \"Task completed successfully\", \"worked_hours\": 5}"
```

### Admin Views Report:
1. Login as admin1
2. Go to "Manage Tasks"
3. Click "View Report" on the completed task

## Common Issues

**Q: "No such table: custom_user"**
A: Run migrations: `python manage.py makemigrations` then `python manage.py migrate`

**Q: Can't login to panel**
A: Make sure the user role is set to 'admin' or 'superadmin' in the database

**Q: API returns 401 Unauthorized**
A: Your JWT token may have expired. Get a new token using `/api/token/` endpoint

**Q: Can't create tasks**
A: Admins can only create tasks for users assigned to them. SuperAdmin must assign users to admins first.

## Default URLs

- **Admin Panel Login**: http://127.0.0.1:8000/panel/login/
- **API Token**: http://127.0.0.1:8000/api/token/
- **API Tasks**: http://127.0.0.1:8000/api/tasks/
- **Django Admin** (optional): http://127.0.0.1:8000/admin/

Enjoy using the Task Management Application!


# Task Management System - Setup Instructions

## Prerequisites
- Python 3.8 or higher
- pip package manager

## Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Admin Account**
   ```bash
   python manage.py createsuperuser
   ```

4. **Set Admin Role**
   ```bash
   python manage.py shell
   ```
   ```python
   from tasks.models import CustomUser
   user = CustomUser.objects.get(username='your_username')
   user.role = 'superadmin'
   user.save()
   exit()
   ```

5. **Start Server**
   ```bash
   python manage.py runserver
   ```

6. **Access Application**
   - Homepage: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/panel/login/

## Features
- Role-based access control (SuperAdmin, Admin, User)
- Task management with completion reports
- REST API with JWT authentication
- Modern web interface



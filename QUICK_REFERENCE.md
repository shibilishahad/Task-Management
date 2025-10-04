# Task Management System - Quick Reference

## 🔧 Setup Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Create database
python manage.py makemigrations
python manage.py migrate

# Create superadmin
python manage.py createsuperuser

# Set superadmin role
python manage.py shell
>>> from tasks.models import CustomUser
>>> user = CustomUser.objects.get(username='your_username')
>>> user.role = 'superadmin'
>>> user.save()
>>> exit()

# Create sample data (optional)
python create_sample_data.py

# Run server
python manage.py runserver
```

---

## 🌐 Important URLs

| Purpose | URL |
|---------|-----|
| Admin Panel Login | http://127.0.0.1:8000/panel/login/ |
| SuperAdmin Dashboard | http://127.0.0.1:8000/panel/superadmin/dashboard/ |
| Admin Dashboard | http://127.0.0.1:8000/panel/admin/dashboard/ |
| API Token | http://127.0.0.1:8000/api/token/ |
| API Tasks | http://127.0.0.1:8000/api/tasks/ |
| Django Admin (optional) | http://127.0.0.1:8000/admin/ |

---

## 🔐 Default Credentials (After Sample Data)

### SuperAdmin
```
Username: superadmin
Password: super123456
```

### Admins
```
Username: admin1 / admin2
Password: admin1123456 / admin2123456
```

### Users
```
Username: user1 / user2 / user3 / user4 / user5
Password: user1123456 / user2123456 / etc.
```

---

## 📡 API Quick Commands

### Get JWT Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "user1123456"}'
```

### Get My Tasks
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Complete Task
```bash
curl -X PUT http://127.0.0.1:8000/api/tasks/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "completion_report": "Task done",
    "worked_hours": 5
  }'
```

### View Task Report (Admin)
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/1/report/ \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

---

## 👥 User Roles & Permissions

| Role | Can Do |
|------|--------|
| **SuperAdmin** | • Manage admins<br>• Manage users<br>• View all tasks<br>• View all reports |
| **Admin** | • Create tasks<br>• Assign tasks to users<br>• View task reports<br>• Manage own users |
| **User** | • View own tasks (API)<br>• Update task status (API)<br>• Submit completion reports |

---

## 📋 Task Status Flow

```
Pending → In Progress → Completed
  ↓           ↓            ↓
 (Any)      (Any)    (Requires Report + Hours)
```

---

## 🗄️ Database Models

### CustomUser
- username, email, password
- role: `superadmin` | `admin` | `user`
- assigned_to_admin (for users)

### Task
- title, description
- assigned_to, created_by
- due_date, status
- completion_report, worked_hours
- created_at, updated_at

---

## ⚡ Common Commands

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Run server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Collect static files
python manage.py collectstatic
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "No such table" | Run migrations |
| Can't login to panel | Check user role |
| 401 Unauthorized | Token expired, get new one |
| 403 Forbidden | Wrong role for endpoint |
| Can't create task | User not assigned to admin |

---

## 📦 Required Packages
```
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
PyJWT==2.8.0
```

---

## 🎯 Testing Checklist

- [ ] SuperAdmin can login to panel
- [ ] SuperAdmin can create admins
- [ ] SuperAdmin can create users
- [ ] SuperAdmin can assign users to admins
- [ ] Admin can login to panel
- [ ] Admin can create tasks
- [ ] Admin can view assigned users
- [ ] User can get JWT token
- [ ] User can view tasks via API
- [ ] User can update task status
- [ ] User can complete task with report
- [ ] Admin can view completion report
- [ ] API returns correct error codes

---

## 📱 HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (no/invalid token) |
| 403 | Forbidden (wrong permissions) |
| 404 | Not Found |
| 500 | Server Error |

---

## 🔑 JWT Token Format

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

Token Lifetime:
- Access Token: 5 hours
- Refresh Token: 1 day

---

## 📄 File Structure

```
taskkkk/
├── manage.py
├── requirements.txt
├── README.md
├── task_management/
│   ├── settings.py
│   └── urls.py
├── tasks/
│   ├── models.py
│   ├── api_views.py
│   ├── panel_views.py
│   └── serializers.py
└── templates/
    └── panel/
        ├── superadmin/
        └── admin/
```

---

## 🎨 Task Status Badges

| Status | Color | Display |
|--------|-------|---------|
| Pending | Yellow | 🟡 Pending |
| In Progress | Blue | 🔵 In Progress |
| Completed | Green | 🟢 Completed |

---

## 💡 Pro Tips

1. **Use Postman collections** for easier API testing
2. **Save JWT tokens** in environment variables
3. **Test with multiple users** to verify permissions
4. **Check server logs** for debugging errors
5. **Use sample data script** for quick setup

---

## 📚 Documentation Files

1. **README.md** - Full documentation
2. **setup_guide.md** - Setup instructions
3. **API_TESTING_GUIDE.md** - API testing examples
4. **PROJECT_SUMMARY.md** - Project overview
5. **QUICK_REFERENCE.md** - This file

---

## 🚀 Production Deployment Notes

Before deploying:
- [ ] Change SECRET_KEY in settings.py
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up proper static file serving
- [ ] Configure HTTPS
- [ ] Set up environment variables
- [ ] Configure proper logging

---




# 🧪 API Testing Guide - Task Management Application

## 🎯 Quick Setup
1. **Start Server:** `python manage.py runserver`
2. **Create Sample Data:** `python create_sample_data.py`

**Base URL:** `http://127.0.0.1:8000`

---

## 👥 Test Users
| Username | Password | Role |
|----------|----------|------|
| `user1` | `user1123456` | User |
| `admin1` | `admin1123456` | Admin |
| `superadmin` | `super123456` | SuperAdmin |

---

## 🔑 Step 1: Get JWT Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d "{\"username\":\"user1\",\"password\":\"user1123456\"}"
```

**Expected:** Returns `access` and `refresh` tokens

---

## 📋 Step 2: Get User Tasks
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected:** Returns array of tasks assigned to the user

---

## ✏️ Step 3: Update Task
```bash
curl -X PUT http://127.0.0.1:8000/api/tasks/1/ -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d "{\"status\":\"completed\",\"completion_report\":\"Task completed\",\"worked_hours\":5}"
```

**Expected:** Returns success message with updated task

---

## 🔄 Step 4: Refresh Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ -H "Content-Type: application/json" -d "{\"refresh\":\"YOUR_REFRESH_TOKEN\"}"
```

**Expected:** Returns new `access` token

---

## 📊 Step 5: Get Task Report (Admin/SuperAdmin Only)
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/1/report/ -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

**Expected:** Returns detailed task information

---

## 🌐 Browser Tests (GET Only)
- **Homepage:** `http://127.0.0.1:8000/`
- **API Info:** `http://127.0.0.1:8000/api-info/`
- **Panel Login:** `http://127.0.0.1:8000/panel/login/`

**Note:** Protected endpoints (`/api/tasks/`, `/api/tasks/1/report/`) will return 401/403 errors in browser (expected)

---


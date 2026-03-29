# 🔧 Port Fix Commands - Quick Solutions

## 🚨 Port Already in Use? Here's the Fix:

### Option 1: Kill Existing Process (Recommended)
```bash
# Kill any Django server running
pkill -f "python manage.py runserver"

# Force kill port 8000 if still in use
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Start server again
source venv/bin/activate
python manage.py runserver 127.0.0.1:8000
```

### Option 2: Use Different Port
```bash
# Use port 8001 instead
source venv/bin/activate
python manage.py runserver 127.0.0.1:8001
```

### Option 3: One-Liner Fix
```bash
pkill -f "python manage.py runserver" && sleep 2 && source venv/bin/activate && python manage.py runserver 127.0.0.1:8000
```

---

## ✅ Current Status

**Server is now running successfully on:**
- 🌐 http://127.0.0.1:8000/
- 🔗 GraphQL: http://127.0.0.1:8000/graphql/

**All endpoints working:**
- ✅ API Root: http://127.0.0.1:8000/
- ✅ GraphQL: http://127.0.0.1:8000/graphql/
- ✅ AI Health: http://127.0.0.1:8000/api/ai/health/
- ✅ ERPNext Health: http://127.0.0.1:8000/api/erpnext/health/

---

## 🎯 Best Practice

Always use this sequence:
```bash
cd ~/Desktop/vynilart/backend

# 1. Kill any existing servers
pkill -f "python manage.py runserver"

# 2. Activate venv
source venv/bin/activate

# 3. Start server
python manage.py runserver 127.0.0.1:8000
```

**Problem solved!** 🎉

# Django Server Setup Guide

## 🚀 Quick Start

### Method 1: Using the Script (Recommended)
```bash
cd ~/Desktop/vynilart/backend
./runserver.sh
```

### Method 2: Manual Start
```bash
cd ~/Desktop/vynilart/backend
source venv/bin/activate
python manage.py runserver 8000
```

## 📦 Required Packages

The following packages are installed in the virtual environment:
- django (6.0.3)
- django-cors-headers (4.9.0)
- graphene-django (3.2.3)
- django-filter (25.2)
- Pillow (12.1.1)
- python-dotenv (1.2.2)

## 🔗 Available Endpoints

- **API Root**: http://localhost:8000/
- **GraphQL**: http://localhost:8000/graphql/
- **AI Health**: http://localhost:8000/api/ai/health/
- **ERPNext Health**: http://localhost:8000/api/erpnext/health/
- **Calculate Price**: http://localhost:8000/api/calculate-price/
- **Validate Coupon**: http://localhost:8000/api/validate-coupon/

## 🛠️ Common Issues

### ModuleNotFoundError: No module named 'corsheaders'
**Solution**: Make sure you're in the virtual environment:
```bash
source venv/bin/activate
python manage.py runserver 8000
```

### Port already in use
**Solution**: Kill existing server:
```bash
pkill -f "python manage.py runserver"
```

## 🌐 Frontend Integration

The server is configured to accept requests from:
- http://localhost:5173 (Vue.js default)
- http://127.0.0.1:5173
- http://localhost:8080 (Vite default)
- http://127.0.0.1:8080

## 📊 GraphQL

Access GraphiQL interface in development:
http://localhost:8000/graphql/

Example query:
```graphql
{
  __schema {
    types {
      name
    }
  }
}
```

#!/bin/bash

# Django Server Runner - Global Virtual Environment
# Uses global venv to avoid path issues

echo "🚀 Starting Django Server with Global Virtual Environment..."

# Navigate to backend directory
cd "$(dirname "$0")"

# Use global virtual environment
if [ -d "/home/ahmad/venv-django" ]; then
    echo "📦 Using global virtual environment..."
    source /home/ahmad/venv-django/bin/activate
else
    echo "❌ Global virtual environment not found!"
    exit 1
fi

# Copy project files to work in venv context
export DJANGO_SETTINGS_MODULE="paclos_backend.settings"

# Start Django server
echo "🌐 Starting Django development server..."
echo "📍 Server: http://localhost:8000"
echo "🔗 GraphQL: http://localhost:8000/graphql/"
echo "🛑 Press Ctrl+C to stop"
echo ""

python manage.py runserver 8000

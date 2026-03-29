#!/bin/bash

# Django Server Starter - Always uses Virtual Environment
# This script ensures you're always in the correct environment

echo "🚀 Starting Django Server with Virtual Environment..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found in $SCRIPT_DIR/venv"
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install django django-cors-headers graphene-django django-filter python-dotenv Pillow
else
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Verify packages are installed
echo "🔍 Checking required packages..."
python -c "import django, corsheaders, graphene_django" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing missing packages..."
    pip install django django-cors-headers graphene-django django-filter python-dotenv Pillow
fi

# Kill any existing Django server
echo "🛑 Stopping any existing Django server..."
pkill -f "python manage.py runserver" 2>/dev/null || true

# Start Django server
echo "🌐 Starting Django development server..."
echo "📍 Server will be available at: http://localhost:8000"
echo "🔗 GraphQL endpoint: http://localhost:8000/graphql/"
echo "🏥 Health checks: http://localhost:8000/api/ai/health/"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python manage.py runserver 8000

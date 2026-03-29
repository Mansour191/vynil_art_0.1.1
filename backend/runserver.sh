#!/bin/bash

# Django Server Runner with Virtual Environment
# Always run the server in the correct virtual environment

echo "🚀 Starting Django Server in Virtual Environment..."

# Navigate to backend directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    exit 1
fi

# Check if required packages are installed
echo "🔍 Checking required packages..."
python -c "import django, corsheaders, graphene_django" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing missing packages..."
    pip install django django-cors-headers graphene-django django-filter python-dotenv Pillow
fi

# Run Django server
echo "🌐 Starting Django development server on http://localhost:8000"
echo "📊 GraphQL endpoint: http://localhost:8000/graphql/"
echo "🔍 Health checks: http://localhost:8000/api/ai/health/"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python manage.py runserver 8000

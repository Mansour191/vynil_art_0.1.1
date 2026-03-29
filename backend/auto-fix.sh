#!/bin/bash

# Auto-Fix Django Environment Script
# Deep Debugging and Auto-Installation of Missing Packages

echo "🔍 Deep Debugging: Auto-Fixing Django Environment..."

# Navigate to backend directory
cd "$(dirname "$0")"

# Kill any existing Django server
echo "🛑 Stopping existing servers..."
pkill -f "python manage.py runserver" 2>/dev/null || true

# Function to install package if missing
install_if_missing() {
    local package=$1
    local import_name=${2:-$package}
    
    echo "🔍 Checking $package..."
    python3 -c "import $import_name" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "📦 Installing $package..."
        pip install $package
    else
        echo "✅ $package already installed"
    fi
}

# Function to check and install Django packages
check_django_packages() {
    echo "🐍 Checking Django ecosystem compatibility..."
    
    # Core Django packages
    install_if_missing "django>=6.0.3"
    install_if_missing "django-cors-headers"
    install_if_missing "graphene-django"
    install_if_missing "django-filter"
    install_if_missing "python-dotenv"
    install_if_missing "Pillow"
    
    # GraphQL ecosystem
    install_if_missing "graphene>=3.4.3"
    install_if_missing "graphql-core>=3.2.8"
    install_if_missing "graphql-relay>=3.2.0"
    
    # Additional dependencies
    install_if_missing "asgiref>=3.11.1"
    install_if_missing "text-unidecode"
    install_if_missing "typing-extensions>=4.15.0"
}

# Create/Update Virtual Environment
setup_environment() {
    echo "🏗️ Setting up Python 3.13 compatible environment..."
    
    # Use existing venv or create new one
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment for Python 3.13..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip in venv
    echo "⬆️ Upgrading pip..."
    pip install --upgrade pip
    
    # Install packages
    check_django_packages
}

# Clean settings.py
clean_settings() {
    echo "🧹 Cleaning settings.py from REST framework remnants..."
    
    # Backup original settings
    cp paclos_backend/settings.py paclos_backend/settings.py.backup
    
    # Remove any rest_framework references
    sed -i '/rest_framework/d' paclos_backend/settings.py
    sed -i '/djangorestframework/d' paclos_backend/settings.py
    sed -i '/REST_FRAMEWORK/d' paclos_backend/settings.py
    sed -i '/SIMPLE_JWT/d' paclos_backend/settings.py
    
    echo "✅ Settings cleaned from REST remnants"
}

# Configure CORS properly
configure_cors() {
    echo "🌐 Configuring CORS for frontend access..."
    
    # Ensure CORS settings exist
    if ! grep -q "CORS_ALLOWED_ORIGINS" paclos_backend/settings.py; then
        echo "📝 Adding CORS configuration..."
        cat >> paclos_backend/settings.py << 'EOF'

# CORS configuration for Vue.js frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080", 
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
EOF
    fi
    
    echo "✅ CORS configured"
}

# Test Django server
test_server() {
    echo "🧪 Testing Django server..."
    
    # Try to start server on port 8000
    echo "🚀 Starting Django server on http://127.0.0.1:8000"
    
    # Test if port is available
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️ Port 8000 in use, trying 8001..."
        python manage.py runserver 127.0.0.1:8001
    else
        python manage.py runserver 127.0.0.1:8000
    fi
}

# Generate requirements.txt
generate_requirements() {
    echo "📋 Generating requirements.txt..."
    
    source venv/bin/activate
    pip freeze > requirements.txt
    
    echo "✅ requirements.txt generated with current packages"
}

# Execute all steps
main() {
    setup_environment
    clean_settings
    configure_cors
    test_server
    generate_requirements
    
    echo "🎉 Auto-fix completed!"
    echo "📍 Server should be running on: http://127.0.0.1:8000"
    echo "🔗 GraphQL endpoint: http://127.0.0.1:8000/graphql/"
}

# Run main function
main

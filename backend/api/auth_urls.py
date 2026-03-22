from django.urls import path
from .auth import (
    login_view, register_view, change_password_view,
    reset_password_view, confirm_reset_password_view,
    profile_view, update_profile_view
)

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/change-password/', change_password_view, name='change_password'),
    path('auth/reset-password/', reset_password_view, name='reset_password'),
    path('auth/confirm-reset-password/', confirm_reset_password_view, name='confirm_reset_password'),
    
    # Profile endpoints
    path('auth/profile/', profile_view, name='profile'),
    path('auth/profile/update/', update_profile_view, name='update_profile'),
]

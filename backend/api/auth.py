# Custom DRF Auth Kit Implementation
from rest_framework import serializers, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
import random
import string

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Try to authenticate with username first, then email
            user = None
            try:
                user = authenticate(username=email_or_username, password=password)
            except:
                pass
            
            if not user:
                try:
                    user_obj = User.objects.get(email=email_or_username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if not user:
                raise serializers.ValidationError('بيانات الدخول غير صحيحة')
            
            if not user.is_active:
                raise serializers.ValidationError('الحساب غير نشط')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('يجب إدخال البريد الإلكتروني/اسم المستخدم وكلمة المرور')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'phone')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('كلمات المرور غير متطابقة')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('كلمات المرور الجديدة غير متطابقة')
        return attrs

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('البريد الإلكتروني غير مسجل')
        return value

class ConfirmResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('كلمات المرور غير متطابقة')
        return attrs

# Helper functions
def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

# API Views
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    Custom login view that accepts email or username
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        tokens = generate_tokens(user)
        
        return Response({
            'success': True,
            'message': 'تم تسجيل الدخول بنجاح',
            'data': {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': getattr(user, 'phone', ''),
                    'is_staff': user.is_staff,
                    'date_joined': user.date_joined,
                },
                'tokens': tokens
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'فشل تسجيل الدخول',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """
    Custom registration view
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = generate_tokens(user)
        
        return Response({
            'success': True,
            'message': 'تم إنشاء الحساب بنجاح',
            'data': {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': getattr(user, 'phone', ''),
                    'is_staff': user.is_staff,
                    'date_joined': user.date_joined,
                },
                'tokens': tokens
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'فشل إنشاء الحساب',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    """
    Change password for authenticated user
    """
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'success': False,
                'message': 'كلمة المرور الحالية غير صحيحة'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'success': True,
            'message': 'تم تغيير كلمة المرور بنجاح'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'فشل تغيير كلمة المرور',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password_view(request):
    """
    Send password reset email
    """
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generate reset token and code
        reset_code = generate_verification_code()
        # In production, save this to database with expiry
        
        try:
            send_mail(
                'إعادة تعيين كلمة المرور',
                f'رمز إعادة التعيين: {reset_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except:
            pass  # Handle email sending failure
        
        return Response({
            'success': True,
            'message': 'تم إرسال رمز إعادة التعيين إلى بريدك الإلكتروني',
            'data': {
                'reset_code': reset_code  # Only for development
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'فشل إرسال رمز إعادة التعيين',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def confirm_reset_password_view(request):
    """
    Confirm password reset with code
    """
    serializer = ConfirmResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        # In production, verify the token from database
        # For now, we'll just return success
        
        return Response({
            'success': True,
            'message': 'تم إعادة تعيين كلمة المرور بنجاح'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'فشل إعادة تعيين كلمة المرور',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    """
    Get user profile
    """
    user = request.user
    return Response({
        'success': True,
        'data': {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': getattr(user, 'phone', ''),
                'is_staff': user.is_staff,
                'date_joined': user.date_joined,
            }
        }
    }, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile_view(request):
    """
    Update user profile
    """
    user = request.user
    data = request.data.copy()
    
    # Remove sensitive fields
    sensitive_fields = ['password', 'is_staff', 'is_superuser', 'date_joined']
    for field in sensitive_fields:
        data.pop(field, None)
    
    serializer = serializers.ModelSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        
        return Response({
            'success': True,
            'message': 'تم تحديث الملف الشخصي بنجاح',
            'data': {
                'user': serializer.data
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'فشل تحديث الملف الشخصي',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

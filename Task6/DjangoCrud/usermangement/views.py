from django.contrib.auth import authenticate, login, logout  # Functions for user authentication and session management
from django.core.mail import send_mail  # Function to send emails
from django.conf import settings  # Access Django settings (e.g., EMAIL_HOST_USER)
from django.utils import timezone  # Import timezone for OTP timestamp
from rest_framework.decorators import api_view, permission_classes, parser_classes  # Decorators for API views and permission control
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser  # Permission classes for API endpoints
from rest_framework.response import Response  # Standard API response object
from rest_framework import status  # HTTP status codes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser  # Parsers for handling file uploads
from django.db import transaction  # For atomic database transactions
from rest_framework.authentication import TokenAuthentication  # Token-based authentication
from rest_framework.decorators import authentication_classes  # Token-based authentication
from rest_framework_simplejwt.tokens import RefreshToken  # JWT token management
import random
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from util.sent_otp import send_otp  # Utility function to send OTP emails
from util.responses import create_response  # Utility function to create standardized API responses

from datetime import timedelta
from .models import User, PasswordResetOTP, EmailVerificationOTP  # Import custom User model and OTP models
from .serializer import (
    UserSerializer, 
    RegistrationSerializer,
    UserProfileSerializer,
    EditProfileSerializer,
    VerifyEmailSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer, 
    ResetPasswordSerializer
)
from util.responses import APIResponse # Standardized API response utility




# Get all users (only authenticated users can access)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getusers(request):
    users = User.objects.all()  # Fetch all users
    serializer = UserSerializer(users, many=True)  # Serialize list of users
    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.USERS_LIST_RETRIEVED,
        data={'users': serializer.data},
        status_code=status.HTTP_200_OK
    )


# Add a new user (Admin only)
@api_view(['POST'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser, JSONParser])  # Support file uploads
@transaction.atomic
def adduser(request):

    serializer = RegistrationSerializer(data=request.data)  # Get user data with validation
    
    if not serializer.is_valid():
        return APIResponse.get_validation_error_response(
            return_code=APIResponse.Codes.VALIDATION_ERROR,
            serializer_errors=serializer.errors
        )
    
    user = serializer.save()  # Create user
    # Admin created users are automatically verified
    user.is_verified = True
    user.save()
    
    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.REGISTRATION_SUCCESS,
        data={'user': UserSerializer(user).data},
        status_code=status.HTTP_201_CREATED
    )


# Edit an existing user (Admin only)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser, JSONParser])  # Support file uploads
@transaction.atomic
def edituser(request, pk):


    try:
        user = User.objects.get(pk=pk)  # Find user by ID
    except User.DoesNotExist:
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.USER_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    # Partial update allowed
    serializer = UserSerializer(user, data=request.data, partial=True)
    
    if not serializer.is_valid():
        return APIResponse.get_validation_error_response(
            return_code=APIResponse.Codes.VALIDATION_ERROR,
            serializer_errors=serializer.errors
        )
    
    password = serializer.validated_data.pop('password', None)
    serializer.save()

    # If password is provided, update it separately
    if password:
        user.set_password(password)
        user.save()

    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.PROFILE_UPDATED,
        data={'user': UserSerializer(user).data},
        status_code=status.HTTP_200_OK
    )

# Update password (Admin only)
@api_view(['PUT'])
@permission_classes([IsAdminUser])
@transaction.atomic
def update_password(request, pk):

    
    try:
        user = User.objects.get(pk=pk)  # Get user
    except User.DoesNotExist:
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.USER_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND
        )


    new_password = request.data.get('new_password')

    # Validate new password is provided
    if not new_password:
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.PASSWORD_REQUIRED,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Hash and save the new password
    user.set_password(new_password)
    user.save()

    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.PASSWORD_CHANGE_SUCCESS,
        status_code=status.HTTP_200_OK
    )


# Delete user (Admin only)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@transaction.atomic
def del_user(request, pk):
    try:
        user = User.objects.get(pk=pk)  # Find user
    except User.DoesNotExist:
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.USER_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    user.delete()  # Delete user
    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.USER_DELETED_SUCCESS,
        status_code=status.HTTP_200_OK
    )


# User sign up (Registration with email verification)
@api_view(['POST'])
@permission_classes([AllowAny]) 
@parser_classes([MultiPartParser, FormParser, JSONParser])  # Support file uploads
@transaction.atomic
def sign_up(request):
    serializer = RegistrationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return APIResponse.get_validation_error_response(
            return_code=APIResponse.Codes.VALIDATION_ERROR,
            serializer_errors=serializer.errors
        )
    
    user = serializer.save()  # Create user (is_verified defaults to False)
    send_otp(user)
    
    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.REGISTRATION_SUCCESS,
        data={'user': UserSerializer(user).data},
        status_code=status.HTTP_201_CREATED
    )


# Email verification using OTP
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
@transaction.atomic
def verify_email(request):
    serializer = VerifyEmailSerializer(data=request.data)
    
    if not serializer.is_valid():
        return APIResponse.get_validation_error_response(
            return_code=APIResponse.Codes.VALIDATION_ERROR,
            serializer_errors=serializer.errors
        )
    
    email = serializer.validated_data['email']
    otp = serializer.validated_data['otp']
    
    # Check if user and OTP exist
    try:
        user = User.objects.get(email=email)
        otp_obj = EmailVerificationOTP.objects.get(user=user, otp=otp)
    except (User.DoesNotExist, EmailVerificationOTP.DoesNotExist):
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.OTP_INVALID,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if OTP is expired (10 minutes)
    if timezone.now() - otp_obj.created_at > timedelta(minutes=10):
        otp_obj.delete()
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.OTP_EXPIRED,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Mark user as verified
    user.is_verified = True
    user.save()
    
    # Delete OTP after successful verification
    otp_obj.delete()
    
    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.OTP_VERIFIED,
        data={'user': UserSerializer(user).data},
        status_code=status.HTTP_200_OK
    )


# User login
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def sign_in(request):
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return APIResponse.get_validation_error_response(
            return_code=APIResponse.Codes.VALIDATION_ERROR,
            serializer_errors=serializer.errors
        )
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    # Authenticate user
    user = authenticate(request, username=email, password=password)
    
    if user is None:
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.INVALID_CREDENTIALS,
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    # Check if user has verified their email
    if not user.is_verified:
        # Generate 6-digit OTP for email verification
        send_otp(user)
        
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.ACCOUNT_NOT_VERIFIED,
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    login(request, user)  # Login user
    
    role = "Superuser" if user.is_superuser else "User"
    
    
    refresh=RefreshToken.for_user(user)
    access_token=str(refresh.access_token)
    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.LOGIN_SUCCESS,
        data={'user': UserSerializer(user).data, 'access_token': str(access_token), 'refresh_token': str(refresh), 'role': role},
        status_code=status.HTTP_200_OK
    )


# Logout user
@api_view(['GET','POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def sign_out(request):
    logout(request)  # End session
    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.LOGOUT_SUCCESS,
        status_code=status.HTTP_200_OK
    )


# View user profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile(request):
    user = request.user
    serializer = UserProfileSerializer(user)
    
    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.PROFILE_RETRIEVED,
        data={'user': serializer.data},
        status_code=status.HTTP_200_OK
    )

# Edit user profile
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@transaction.atomic
def edit_profile(request):
    user = request.user
    serializer = EditProfileSerializer(user, data=request.data, partial=True)
    
    if not serializer.is_valid():
        return APIResponse.get_validation_error_response(
            return_code=APIResponse.Codes.VALIDATION_ERROR,
            serializer_errors=serializer.errors
        )
    
    updated_user = serializer.save()
    
    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.PROFILE_UPDATED,
        data={'user': UserProfileSerializer(updated_user).data},
        status_code=status.HTTP_200_OK
    )

# Change password (requires old password)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    
    if not serializer.is_valid():
        return APIResponse.get_validation_error_response(
            return_code=APIResponse.Codes.VALIDATION_ERROR,
            serializer_errors=serializer.errors
        )
    
    user = request.user
    old_password = serializer.validated_data['old_password']
    new_password = serializer.validated_data['new_password']
    
    # Verify old password
    if not user.check_password(old_password):
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.INVALID_CREDENTIALS,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if new password is same as old password
    if old_password == new_password:
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.PASSWORDS_DO_NOT_MATCH,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Update password
    user.set_password(new_password)
    user.save()
    
    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.PASSWORD_CHANGE_SUCCESS,
        status_code=status.HTTP_200_OK
    )


# Forgot password (send OTP)
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def forget_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.get_validation_error_response(
            return_code=APIResponse.Codes.VALIDATION_ERROR,
            serializer_errors=serializer.errors
        )
    
    email = serializer.validated_data['email']

    # Try to find user by email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Do not reveal if user exists (security best practice)
        return APIResponse.get_success_response(
            return_code=APIResponse.Codes.PASSWORD_RESET_EMAIL_SENT,
            status_code=status.HTTP_200_OK
        )

    # Generate 6-digit OTP and save
    otp = f"{random.randint(100000, 999999)}"
    PasswordResetOTP.objects.update_or_create(user=user, defaults={'otp': otp, 'created_at': timezone.now()})

    subject = "Password Reset OTP"
    message = f"Your password reset OTP is: {otp}. It is valid for 10 minutes."
    from_email = settings.EMAIL_HOST_USER
    
    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)  # Send email
    except Exception as e:
        return create_response(
            success=False,
            message='Failed to send OTP email',
            errors={'email_error': str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.PASSWORD_RESET_EMAIL_SENT,
        status_code=status.HTTP_200_OK
    )


# Reset password using OTP
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
@transaction.atomic
def reset_password(request):

    serializer = ResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.get_validation_error_response(
            return_code=APIResponse.Codes.VALIDATION_ERROR,
            serializer_errors=serializer.errors
        )
    
    email = serializer.validated_data['email']
    otp = serializer.validated_data['otp']
    new_password = serializer.validated_data['new_password']
    
    # Check OTP validity
    try:
        user = User.objects.get(email=email)
        otp_obj = PasswordResetOTP.objects.get(user=user, otp=otp)
    except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.OTP_INVALID,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if OTP is expired (10 minutes)
    if timezone.now() - otp_obj.created_at > timedelta(minutes=10):
        otp_obj.delete()
        return APIResponse.get_error_response(
            return_code=APIResponse.Codes.OTP_EXPIRED,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Update user's password
    user.set_password(new_password)
    user.save()

    # Delete OTP after use
    otp_obj.delete()
    
    return APIResponse.get_success_response(
        return_code=APIResponse.Codes.PASSWORD_CHANGE_SUCCESS,
        status_code=status.HTTP_200_OK
    )
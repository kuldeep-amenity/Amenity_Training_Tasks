from django.contrib.auth import authenticate, login, logout  # Functions for user authentication and session management
from django.contrib.auth.hashers import make_password       # Function to hash passwords
from django.core.mail import send_mail                      # Function to send emails
from django.conf import settings                             # Access Django settings (e.g., EMAIL_HOST_USER)
from rest_framework.decorators import api_view, permission_classes  # Decorators for API views and permission control
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser  # Permission classes for API endpoints
from rest_framework.response import Response                # Standard API response object
from rest_framework import status                            # HTTP status codes
from django.db import transaction                            # For atomic database transactions
from .models import User, PasswordResetToken                # Import custom User model and password reset token model
from .serializer import UserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer  # Import serializers for user and password operations


# Get all users (only authenticated users can access)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getusers(request):
    users = User.objects.all()  # Fetch all users
    serializer = UserSerializer(users, many=True)  # Serialize list of users
    return Response(serializer.data, status=status.HTTP_200_OK)


# Add a new user (Admin only)
@api_view(['POST'])
@permission_classes([IsAdminUser])
@transaction.atomic
def adduser(request):
    serializer = UserSerializer(data=request.data)  # Get user data
    if serializer.is_valid():
        user = serializer.save()  # Create user
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Edit an existing user (User themself or superuser)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def edituser(request, pk):
    try:
        user = User.objects.get(pk=pk)  # Find user by ID
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check permission (superuser OR editing own profile)
    if not (request.user.is_superuser or request.user.id == user.id):
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    # Partial update allowed
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        password = serializer.validated_data.pop('password', None)
        serializer.save()

        # If password is provided, update it separately
        if password:
            user.set_password(password)
            user.save()

        return Response(UserSerializer(user).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update password (User or Admin)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def update_password(request, pk):
    try:
        user = User.objects.get(pk=pk)  # Get user
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Only superuser or the user themself can update password
    if not request.user.is_superuser and request.user.id != user.id:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    current_password = request.data.get('password')
    new_password = request.data.get('new_password')

    if not new_password:
        return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Normal user must verify current password
    if not request.user.is_superuser:
        if not current_password:
            return Response({'error': 'Current password is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        if current_password == new_password:
            return Response({'error': 'New password cannot be the same as the current password'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)


# Delete user (Admin only)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@transaction.atomic
def del_user(request, pk):
    try:
        user = User.objects.get(pk=pk)  # Find user
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user.delete()  # Delete user
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# User sign up (Admin can create users)
@api_view(['POST'])
@permission_classes([IsAdminUser]) 
@transaction.atomic
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # Create user
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User login
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=email, password=password)  # Authenticate user
    
    if user is not None:
        login(request, user)  # Login user
        
        role = "Superuser" if user.is_superuser else "User"
        
        return Response({
            'user': UserSerializer(user).data,
            'message': f'{role} Login successful',
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


# Logout user
@api_view(['GET','POST'])
def sign_out(request):
    logout(request)  # End session
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


# Forgot password (send reset link)
@api_view(['POST'])
@permission_classes([AllowAny])
def forget_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']

    # Try to find user by email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Do not reveal if user exists (security)
        return Response({'message': 'If email exists, a reset link has been sent.'}, status=status.HTTP_200_OK)

    # Create or reuse existing token
    token_obj, created = PasswordResetToken.objects.get_or_create(user=user)
    reset_link = f"http://localhost:3000/resetpassword/{token_obj.token}/"
    
    subject = "Password Reset Request"
    message = f"Click the link to reset your password: {reset_link}"
    from_email = settings.EMAIL_HOST_USER
    
    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)  # Send email
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'Reset link sent to your email.'}, status=status.HTTP_200_OK)


# Reset password using token
@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    token = serializer.validated_data['token']
    new_password = serializer.validated_data['new_password']
    
    # Check token validity
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Update user's password
    user = reset_token.user
    user.set_password(new_password)
    user.save()

    # Delete token after use
    reset_token.delete()
    
    return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)

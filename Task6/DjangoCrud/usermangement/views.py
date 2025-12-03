from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import User, PasswordResetToken
from .serializer import UserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getusers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdminUser])
@transaction.atomic
def adduser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def edituser(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not request.user.is_superuser and request.user.id != user.id:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        if 'password' in serializer.validated_data:
            user.set_password(serializer.validated_data['password'])
            user.save()
    
            del serializer.validated_data['password'] 
        else:
             serializer.save()
             
        return Response(UserSerializer(user).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@transaction.atomic
def del_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user.delete()
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@permission_classes([IsAdminUser]) 
@transaction.atomic
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    user = authenticate(request, username=email, password=password)
    
    if user is not None:
        login(request, user)
        
        
        role = "Superuser" if user.is_superuser else "User"
        
        return Response({
            'user': UserSerializer(user).data,
            'message': f'{role} Login successful',
            'redirect_url': '/dashboard' 
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def sign_out(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([AllowAny])
def forget_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        
        return Response({'message': 'If email exists, a reset link has been sent.'}, status=status.HTTP_200_OK)

    token_obj, created = PasswordResetToken.objects.get_or_create(user=user)
    reset_link = f"http://localhost:3000/reset-password/{token_obj.token}/"
    
    subject = "Password Reset Request"
    message = f"Click the link to reset your password: {reset_link}"
    from_email = settings.EMAIL_HOST_USER
    
    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'Reset link sent to your email.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    token = serializer.validated_data['token']
    new_password = serializer.validated_data['new_password']
    
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = reset_token.user
    user.set_password(new_password) 
    user.save()
    reset_token.delete()
    
    return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
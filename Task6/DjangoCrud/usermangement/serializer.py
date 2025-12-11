from rest_framework import serializers  # Import DRF serializers for converting model instances to JSON and validating input
from .models import User    # Import the custom User model from current app
import re  # Regular expressions for password validation
from util.base_serializer import BaseModelSerializer, BaseSerializerSerializer


# Serializer for user model
class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User  # Use the custom User model
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'password', 'profile_picture', 'phone_number', 'is_verified']  # Fields to include in API
        extra_kwargs = {
            'password': {'write_only': True},  # Password should not be returned in responses
            'profile_picture': {'required': False, 'allow_null': True},  # Optional field
            'phone_number': {'required': False, 'allow_null': True},  # Optional field
            'is_verified': {'read_only': True}  # is_verified is read-only, set internally
        }

    # Override create method to ensure password is hashed using create_user()
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Use custom manager to create user
        return user


# Serializer for user registration with password confirmation and enhanced validation
class RegistrationSerializer(BaseModelSerializer):
    confirm_password = serializers.CharField(write_only=True)  # Field to confirm password match
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address', 'password', 'confirm_password', 'profile_picture', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},  # Password should not be returned in responses
            'profile_picture': {'required': False, 'allow_null': True},  # Optional field
            'phone_number': {'required': False, 'allow_null': True}  # Optional field
        }
    
    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value.lower()  # Convert email to lowercase for consistency
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if len(value) > 16:
            raise serializers.ValidationError("Password must not exceed 16 characters.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")
        return value
    
    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data
    
    def create(self, validated_data):

        validated_data.pop('confirm_password')  # Remove confirm_password before creating user
        user = User.objects.create_user(**validated_data)
        return user


# Serializer for viewing user profile (excludes password)
class UserProfileSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'profile_picture', 'phone_number', 'is_verified']
        read_only_fields = ['id', 'email', 'is_verified']  # These fields cannot be edited


# Serializer for editing user profile (only allowed fields)
class EditProfileSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','address', 'phone_number', 'profile_picture']
        extra_kwargs = {
            'profile_picture': {'required': False, 'allow_null': True},
            'phone_number': {'required': False, 'allow_null': True}
        }

# Serializer for email verification OTP
class VerifyEmailSerializer(BaseSerializerSerializer):
    email = serializers.EmailField()  # User's email
    otp = serializers.CharField(max_length=6)  # OTP sent to email


# Serializer for user login
class LoginSerializer(BaseSerializerSerializer):
    email = serializers.EmailField()  # User's email
    password = serializers.CharField(write_only=True)  # User's password


# Serializer for change password (requires old password)
class ChangePasswordSerializer(BaseSerializerSerializer):
    old_password = serializers.CharField(write_only=True)  # Current password for verification
    new_password = serializers.CharField(write_only=True)  # New password
    confirm_new_password = serializers.CharField(write_only=True)  # Confirmation of new password
    
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if len(value) > 16:
            raise serializers.ValidationError("Password must not exceed 16 characters.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")
        return value
    
    def validate(self, data):
        if data.get('new_password') != data.get('confirm_new_password'):
            raise serializers.ValidationError({"confirm_new_password": "Passwords do not match."})
        return data


# Serializer for forgot password request
class ForgotPasswordSerializer(BaseSerializerSerializer):
    email = serializers.EmailField()  # Only email is required


# Serializer for resetting password with OTP
class ResetPasswordSerializer(BaseSerializerSerializer):
    email = serializers.EmailField()  # User email
    otp = serializers.CharField(max_length=6)  # OTP from email
    new_password = serializers.CharField(min_length=8, write_only=True)  # New password
    confirm_new_password = serializers.CharField(write_only=True)  # Confirmation of new password
    
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if len(value) > 16:
            raise serializers.ValidationError("Password must not exceed 16 characters.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")
        return value
    
    def validate(self, data):
        if data.get('new_password') != data.get('confirm_new_password'):
            raise serializers.ValidationError({"confirm_new_password": "Passwords do not match."})
        return data
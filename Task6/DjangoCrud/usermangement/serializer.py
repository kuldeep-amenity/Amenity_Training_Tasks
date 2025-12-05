from rest_framework import serializers  # Import DRF serializers for converting model instances to JSON and validating input
from .models import User    # Import the custom User model from current app


# Serializer for user model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Use the custom User model
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'password', 'profile_picture', 'phone_number']  # Fields to include in API
        extra_kwargs = {
            'password': {'write_only': True},  # Password should not be returned in responses
            'profile_picture': {'required': False, 'allow_null': True},  # Optional field
            'phone_number': {'required': False, 'allow_null': True}  # Optional field
        }

    # Override create method to ensure password is hashed using create_user()
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Use custom manager to create user
        return user

# Serializer for forgot password request
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Only email is required

# Serializer for resetting password
class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField()  # Token sent to user
    new_password = serializers.CharField(min_length=6)  # New password with minimum length

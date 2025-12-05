from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'password', 'profile_picture', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}, 'profile_picture': {'required': False, 'allow_null': True}, 'phone_number': {'required': False, 'allow_null': True}}


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(min_length=6)
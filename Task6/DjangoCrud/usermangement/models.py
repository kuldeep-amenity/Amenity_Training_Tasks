from django.db import models  # Import Django's ORM models to define database tables
from django.contrib.auth.models import AbstractUser, BaseUserManager  # AbstractUser for custom user model, BaseUserManager to manage users
from phonenumber_field.modelfields import PhoneNumberField  # Custom field for storing phone numbers with validation
import uuid  # To generate unique identifiers (used for password reset tokens)

class CustomUserManager(BaseUserManager):
    # Custom method to create a regular user
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  # Normalize email format
        user = self.model(email=email, **extra_fields)  # Create user instance
        user.set_password(password)  # Hash and set password
        user.save(using=self._db)  # Save user to database
        return user

    # Custom method to create a superuser
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Mark as staff
        extra_fields.setdefault('is_superuser', True)  # Mark as superuser
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Remove default username field
    email = models.EmailField(unique=True)  # Unique email field
    first_name = models.CharField(max_length=30)  # User's first name
    last_name = models.CharField(max_length=30)  # User's last name
    address = models.CharField(max_length=255)  # User's address

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # Profile image
    phone_number = PhoneNumberField(blank=True, null=True)  # Optional phone number
    
    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Fields required for superuser creation

    objects = CustomUserManager()  # Attach the custom user manager

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"  # String representation


# class PasswordResetToken(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link token to user
#     token = models.UUIDField(default=uuid.uuid4, editable=False)  # Unique reset token
#     created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation

#     def __str__(self):
#         return f"Reset Token for {self.user.email}"  # String representation


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)  # 6-digit OTP
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.email}"

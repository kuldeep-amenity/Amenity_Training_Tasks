import random
from django.core.mail import send_mail
from django.utils import timezone
from usermangement.models import EmailVerificationOTP
from django.conf import settings
from .responses import create_response
from .responses import status

# Utility function to send OTP email beacuse it was used twice in main views.py so for code reusability i have added this in the util 
def send_otp(user):
    # Generate 6-digit OTP for email verification
    otp = f"{random.randint(100000, 999999)}"
    EmailVerificationOTP.objects.update_or_create(
        user=user, 
        defaults={'otp': otp, 'created_at': timezone.now()}
    )
    # Send OTP to user's email
    subject = "Email Verification OTP"
    message = f"Welcome {user.first_name}! Your email verification OTP is: {otp}. It is valid for 10 minutes."
    from_email = settings.EMAIL_HOST_USER
    
    try:
        send_mail(subject, message, from_email, [user.email], fail_silently=False)
    except Exception as e:
        # If email fails, delete the user and return error
        user.delete()
        return create_response(
            success=False,
            message='Failed to send verification email',
            errors={'email_error': str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
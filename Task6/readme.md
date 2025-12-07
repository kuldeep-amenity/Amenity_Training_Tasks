# Django User Management API

## Project Overview
A complete Django REST API for user management with authentication, authorization, email verification, and password reset functionality. Built using Django REST Framework with session-based authentication.

## Key Features
- Complete user CRUD operations with proper permissions
- User registration with email OTP verification
- Email verification system for new users
- Secure password reset flow with email OTP
- Role-based access control (Admin/User)
- Custom user model using email as primary identifier
- Transaction-safe database operations
- Profile picture upload support
- Phone number validation

## Tech Stack
- **Framework:** Django 5.2.9
- **API:** Django REST Framework
- **Database:** SQLite3
- **Authentication:** Session-based
- **Email:** Console backend (development)
- **Image Handling:** Pillow (for profile pictures)
- **Phone Number:** django-phonenumber-field

## Models

### User
- Custom user model extending AbstractUser
- Fields: email (unique), first_name, last_name, address, password, profile_picture, phone_number, is_verified
- Email used as username field
- Email verification required before login

### EmailVerificationOTP
- Links user to OTP for email verification during registration
- 6-digit OTP with timestamp
- Valid for 10 minutes

### PasswordResetOTP
- Links user to OTP for password resets
- 6-digit OTP with timestamp
- Valid for 10 minutes

## API Endpoints

### Admin APIs (Requires Admin Login)
- `GET /api/getusers/` - List all users
- `POST /api/adduser/` - Create user (auto-verified)
- `PUT/PATCH /api/edituser/<id>/` - Update user (admin or owner)
- `DELETE /api/deleteuser/<id>/` - Delete user
- `PUT /api/updatepassword/<id>/` - Change password (admin or owner)

### Authentication APIs (Public)
- `POST /api/signup/` - Register new user (sends verification OTP)
- `POST /api/verifyemail/` - Verify email with OTP
- `POST /api/signin/` - Login with email/password (requires verified email)
- `GET/POST /api/signout/` - Logout

### User Profile APIs (Requires Login)
- `GET /api/viewprofile/` - View own profile
- `PUT/PATCH /api/editprofile/` - Edit own profile

### Password Management APIs
- `POST /api/changepassword/` - Change password (requires old password, login required)
- `POST /api/forgetpassword/` - Request OTP via email (public)
- `POST /api/resetpassword/` - Reset password with OTP (public)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install django djangorestframework pillow django-phonenumber-field
```

### 2. Install from Requirements
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## Permission Requirements

| Endpoint | Permission Required | Notes |
|----------|-------------------|-------|
| GET /api/getusers/ | Authenticated user | Any logged-in user |
| POST /api/adduser/ | Admin only | Creates verified user |
| PUT /api/edituser/<id>/ | Owner or Admin | Update any field |
| DELETE /api/deleteuser/<id>/ | Admin only | Permanent deletion |
| PUT /api/updatepassword/<id>/ | Owner or Admin | Admin doesn't need old password |
| POST /api/signup/ | Public | Sends OTP to email |
| POST /api/verifyemail/ | Public | Validates OTP |
| POST /api/signin/ | Public | Requires verified email |
| GET/POST /api/signout/ | Public | Clears session |
| GET /api/viewprofile/ | Authenticated user | Own profile only |
| PUT /api/editprofile/ | Authenticated user | Own profile only |
| POST /api/changepassword/ | Authenticated user | Requires old password |
| POST /api/forgetpassword/ | Public | Sends OTP to email |
| POST /api/resetpassword/ | Public | Validates OTP |

## Password Requirements
- Minimum 8 characters, maximum 16 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)
- At least one special character (!@#$%^&*(),.?":{}|<>)

## API Request/Response Examples

### 1. Sign Up (Register User)
```json
POST /api/signup/
Content-Type: application/json

Request:
{
  "first_name": "Rahul",
  "last_name": "Sharma",
  "email": "rahul.sharma@gmail.com",
  "address": "123, MG Road, Connaught Place, New Delhi - 110001",
  "password": "Rahul@123",
  "confirm_password": "Rahul@123",
  "phone_number": "+919876543210"
}

Response (201 CREATED):
{
  "success": true,
  "message": "User registered successfully. Please verify your email with the OTP sent.",
  "data": {
    "user": {
      "id": 1,
      "first_name": "Rahul",
      "last_name": "Sharma",
      "email": "rahul.sharma@gmail.com",
      "address": "123, MG Road, Connaught Place, New Delhi - 110001",
      "profile_picture": null,
      "phone_number": "+919876543210",
      "is_verified": false
    }
  }
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "email": ["user with this email already exists."],
    "password": ["Password must be at least 8 characters long."]
  }
}
```

### 2. Verify Email (OTP)
```json
POST /api/verifyemail/
Content-Type: application/json

Request:
{
  "email": "rahul.sharma@gmail.com",
  "otp": "123456"
}

Response (200 OK):
{
  "success": true,
  "message": "Email verified successfully. You can now login.",
  "data": {
    "user": {
      "id": 1,
      "first_name": "Rahul",
      "last_name": "Sharma",
      "email": "rahul.sharma@gmail.com",
      "is_verified": true
    }
  }
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "message": "Invalid email or OTP"
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "message": "OTP has expired. Please request a new one."
}
```

### 3. Sign In (Login)
```json
POST /api/signin/
Content-Type: application/json

Request:
{
  "email": "rahul.sharma@gmail.com",
  "password": "Rahul@123"
}

Response (200 OK):
{
  "success": true,
  "message": "User login successful",
  "data": {
    "user": {
      "id": 1,
      "first_name": "Rahul",
      "last_name": "Sharma",
      "email": "rahul.sharma@gmail.com",
      "address": "123, MG Road, Connaught Place, New Delhi - 110001",
      "is_verified": true
    }
  }
}

Error Response (401 UNAUTHORIZED):
{
  "success": false,
  "message": "Invalid email or password"
}

Error Response (403 FORBIDDEN):
{
  "success": false,
  "message": "Please verify your email first. Check your inbox for the OTP."
}
```

### 4. Sign Out (Logout)
```json
GET /api/signout/
or
POST /api/signout/

Response (200 OK):
{
  "success": true,
  "message": "Logged out successfully"
}
```

### 5. View Profile
```json
GET /api/viewprofile/
Headers: Session cookie required

Response (200 OK):
{
  "success": true,
  "message": "Profile retrieved successfully",
  "data": {
    "user": {
      "id": 1,
      "first_name": "Rahul",
      "last_name": "Sharma",
      "email": "rahul.sharma@gmail.com",
      "address": "123, MG Road, Connaught Place, New Delhi - 110001",
      "profile_picture": "/media/profile_pics/rahul.jpg",
      "phone_number": "+919876543210",
      "is_verified": true
    }
  }
}
```

### 6. Edit Profile
```json
PUT /api/editprofile/
Headers: Session cookie required
Content-Type: application/json

Request:
{
  "first_name": "Rahul Kumar",
  "last_name": "Sharma",
  "phone_number": "+919876543211"
}

Response (200 OK):
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "user": {
      "id": 1,
      "first_name": "Rahul Kumar",
      "last_name": "Sharma",
      "email": "rahul.sharma@gmail.com",
      "address": "123, MG Road, Connaught Place, New Delhi - 110001",
      "profile_picture": null,
      "phone_number": "+919876543211",
      "is_verified": true
    }
  }
}
```

### 7. Change Password
```json
POST /api/changepassword/
Headers: Session cookie required
Content-Type: application/json

Request:
{
  "old_password": "Rahul@123",
  "new_password": "Rahul@456",
  "confirm_new_password": "Rahul@456"
}

Response (200 OK):
{
  "success": true,
  "message": "Password changed successfully"
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "message": "Old password is incorrect"
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "message": "New password cannot be the same as old password"
}
```

### 8. Forget Password
```json
POST /api/forgetpassword/
Content-Type: application/json

Request:
{
  "email": "rahul.sharma@gmail.com"
}

Response (200 OK):
{
  "success": true,
  "message": "OTP sent to your email."
}

Note: Same response even if email doesn't exist (security best practice)

Error Response (500 INTERNAL SERVER ERROR):
{
  "success": false,
  "message": "Failed to send OTP email",
  "errors": {
    "email_error": "SMTP connection error"
  }
}
```

### 9. Reset Password
```json
POST /api/resetpassword/
Content-Type: application/json

Request:
{
  "email": "rahul.sharma@gmail.com",
  "otp": "654321",
  "new_password": "Rahul@789",
  "confirm_new_password": "Rahul@789"
}

Response (200 OK):
{
  "success": true,
  "message": "Password has been reset successfully"
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "message": "Invalid email or OTP"
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "message": "OTP has expired"
}
```

### 10. Get All Users (Admin or Authenticated)
```json
GET /api/getusers/
Headers: Session cookie required

Response (200 OK):
{
  "success": true,
  "message": "Users retrieved successfully",
  "data": {
    "users": [
      {
        "id": 1,
        "first_name": "Rahul",
        "last_name": "Sharma",
        "email": "rahul.sharma@gmail.com",
        "address": "123, MG Road, New Delhi",
        "is_verified": true
      },
      {
        "id": 2,
        "first_name": "Priya",
        "last_name": "Patel",
        "email": "priya.patel@gmail.com",
        "address": "456, Satellite Road, Ahmedabad",
        "is_verified": true
      }
    ]
  }
}
```

### 11. Add User (Admin Only)
```json
POST /api/adduser/
Headers: Session cookie required (admin)
Content-Type: application/json

Request:
{
  "first_name": "Priya",
  "last_name": "Patel",
  "email": "priya.patel@gmail.com",
  "address": "456, Satellite Road, Ahmedabad, Gujarat - 380015",
  "password": "Priya@123",
  "confirm_password": "Priya@123",
  "phone_number": "+919123456789"
}

Response (201 CREATED):
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "user": {
      "id": 2,
      "first_name": "Priya",
      "last_name": "Patel",
      "email": "priya.patel@gmail.com",
      "is_verified": true
    }
  }
}

Note: Admin created users are automatically verified
```

### 12. Edit User (Admin or Owner)
```json
PUT /api/edituser/1/
Headers: Session cookie required
Content-Type: application/json

Request:
{
  "first_name": "Priya Devi",
  "last_name": "Patel",
  "address": "789, CG Road, Ahmedabad, Gujarat - 380009",
  "phone_number": "+919123456788"
}

Response (200 OK):
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "user": {
      "id": 1,
      "first_name": "Priya Devi",
      "last_name": "Patel",
      "email": "priya.patel@gmail.com",
      "address": "789, CG Road, Ahmedabad, Gujarat - 380009"
    }
  }
}

Error Response (403 FORBIDDEN):
{
  "success": false,
  "message": "Permission denied"
}

Error Response (404 NOT FOUND):
{
  "success": false,
  "message": "User not found"
}
```

### 13. Update Password (Admin or Owner)
```json
PUT /api/updatepassword/1/
Headers: Session cookie required
Content-Type: application/json

Normal User Request:
{
  "password": "Priya@123",
  "new_password": "Priya@456"
}

Admin Request (no current password needed):
{
  "new_password": "Priya@456"
}

Response (200 OK):
{
  "success": true,
  "message": "Password updated successfully"
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "message": "Current password is incorrect"
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "message": "New password cannot be the same as the current password"
}
```

### 14. Delete User (Admin Only)
```json
DELETE /api/deleteuser/1/
Headers: Session cookie required (admin)

Response (200 OK):
{
  "success": true,
  "message": "User deleted successfully"
}

Error Response (404 NOT FOUND):
{
  "success": false,
  "message": "User not found"
}
```

## Testing with Postman

### Setup Base URL
Set environment variable: `base_url = http://localhost:8000/api`

### Testing Flow
1. **Sign Up** → Register user, OTP sent to email (check console)
2. **Verify Email** → Use OTP from console to verify email
3. **Sign In** → Login with verified credentials
4. **View Profile** → Check user profile
5. **Edit Profile** → Update profile details
6. **Change Password** → Change password with old password
7. **Forget Password** → Request OTP for password reset
8. **Reset Password** → Reset password using OTP
9. **Sign In Again** → Login with new password

### Admin Testing
1. Create superuser via command line
2. Sign in as admin
3. Test admin-only endpoints (adduser, deleteuser)
4. Test editing other users

## Project Structure
```
DjangoCrud/
├── usermangement/              # Main app
│   ├── models.py              # User, EmailVerificationOTP, PasswordResetOTP models
│   ├── serializer.py          # DRF serializers with validation
│   ├── views.py               # API endpoints with transaction safety
│   ├── urls.py                # App URL routing
│   └── migrations/            # Database migrations
├── DjangoCrud/
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL config
│   └── wsgi.py                # WSGI config
├── media/
│   └── profile_pics/          # Uploaded profile pictures
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

## Configuration

### Email Settings (Development)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
OTPs will be printed in the console for testing.

### Email Settings (Production)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Media Files
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Security Notes

### For Production
- Set `DEBUG = False`
- Change `SECRET_KEY` to a secure random string
- Use proper email backend (SMTP)
- Configure ALLOWED_HOSTS
- Use HTTPS for all requests
- Set secure cookie flags:
  ```python
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  ```
- Implement rate limiting for OTP requests
- Add CORS headers if needed
- Use environment variables for sensitive data
- Set up proper file upload validation
- Configure max file upload size

### Current Setup
- Development mode (DEBUG=True)
- Session-based authentication
- SQLite database
- No rate limiting (add in production)

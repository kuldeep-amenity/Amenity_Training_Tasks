# Django User Management API

## Project Overview
A complete Django REST API for user management with JWT authentication, authorization, email verification, and password reset functionality. Built using Django REST Framework with JWT token-based authentication.

## Key Features
- Complete user CRUD operations with proper permissions
- User registration with email OTP verification
- Email verification system for new users
- Secure password reset flow with email OTP
- JWT token-based authentication (access & refresh tokens)
- Role-based access control (Admin/User)
- Custom user model using email as primary identifier
- Transaction-safe database operations
- Profile picture upload support
- Phone number validation
- Standardized API response format

## Tech Stack
- **Framework:** Django 5.2.9
- **API:** Django REST Framework
- **Database:** SQLite3
- **Authentication:** JWT (Simple JWT)
- **Email:** SMTP Live email backend 
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
- `PUT/PATCH /api/edituser/<id>/` - Update user details
- `DELETE /api/deleteuser/<id>/` - Delete user
- `PUT /api/updatepassword/<id>/` - Update user password

### Authentication APIs (Public)
- `POST /api/signup/` - Register new user (sends verification OTP)
- `POST /api/verifyemail/` - Verify email with OTP
- `POST /api/signin/` - Login with email/password (requires verified email, returns JWT tokens)
- `GET/POST /api/signout/` - Logout

### User Profile APIs (Requires Login)
- `GET /api/viewprofile/` - View own profile
- `PUT/PATCH /api/editprofile/` - Edit own profile

### Password Management APIs
- `POST /api/changepassword/` - Change password (requires old password, login required)
- `POST /api/forgetpassword/` - Request OTP via email (public)
- `POST /api/resetpassword/` - Reset password with OTP (public)

## Setup Instructions

### 1. Create Django Project and App
```bash
# Create Django project named 'DjangoCrud'
django-admin startproject DjangoCrud
cd DjangoCrud

# Create app named 'usermangement'
python manage.py startapp usermangement

# Create utility directory
mkdir util
touch util/__init__.py
```

### 2. Install Dependencies
```bash
pip install django djangorestframework djangorestframework-simplejwt pillow django-phonenumber-field
```

### 3. Install from Requirements
```bash
pip install -r requirements.txt
```

### 4. Configure Settings
Add to `DjangoCrud/settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'phonenumber_field',
    'usermangement',  # Your app
]

AUTH_USER_MODEL = 'usermangement.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 5. Configure URLs
Update `DjangoCrud/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usermangement.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
# Enter email, first name, last name, and password
```

### 8. Run Development Server
```bash
python manage.py runserver
```

## Authentication

### JWT Token Authentication
The API uses JWT (JSON Web Token) for authentication. After successful login, you receive:
- **Access Token**: Short-lived token for API requests (30 minutes)
- **Refresh Token**: Long-lived token to get new access tokens (7 days)

### Using JWT Tokens
Include the access token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## Permission Requirements

| Endpoint | Permission Required | Notes |
|----------|-------------------|-------|
| GET /api/getusers/ | Authenticated user | Any logged-in user |
| POST /api/adduser/ | Admin only | Creates verified user |
| PUT /api/edituser/<id>/ | Admin only | Update any user field |
| DELETE /api/deleteuser/<id>/ | Admin only | Permanent deletion |
| PUT /api/updatepassword/<id>/ | Admin only | Update any user's password |
| POST /api/signup/ | Public | Sends OTP to email |
| POST /api/verifyemail/ | Public | Validates OTP |
| POST /api/signin/ | Public | Requires verified email, returns JWT tokens |
| GET/POST /api/signout/ | Public | No server-side session to clear |
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

## API Response Format

All API responses follow a standardized format:

### Success Response
```json
{
  "success": true,
  "return_code": "OPERATION_CODE",
  "message": "Human-readable success message",
  "data": {
    // Response data here
  }
}
```

### Error Response
```json
{
  "success": false,
  "return_code": "ERROR_CODE",
  "message": "Human-readable error message"
}
```

### Validation Error Response
```json
{
  "success": false,
  "return_code": "VALIDATION_ERROR",
  "message": "Human-readable validation error message",
  "errors": {
    "field_name": ["error_code"]
  },
  "error_detail": "error_code"
}
```

## Return Codes

### Success Codes
- `REGISTRATION_SUCCESS` - User registered successfully
- `LOGIN_SUCCESS` - Login successful
- `OTP_VERIFIED` - OTP verified successfully
- `PASSWORD_RESET_EMAIL_SENT` - Password reset email sent
- `PASSWORD_CHANGE_SUCCESS` - Password changed successfully
- `LOGOUT_SUCCESS` - Logout successful
- `USER_DELETED_SUCCESS` - User deleted successfully
- `PROFILE_RETRIEVED` - Profile retrieved successfully
- `PROFILE_UPDATED` - Profile updated successfully
- `USERS_LIST_RETRIEVED` - Users list retrieved successfully

### Error Codes
- `VALIDATION_ERROR` - Validation failed
- `INVALID_CREDENTIALS` - Invalid email or password
- `ACCOUNT_NOT_VERIFIED` - Account not verified
- `USER_NOT_FOUND` - User does not exist
- `OTP_INVALID` - Invalid OTP
- `OTP_EXPIRED` - OTP has expired
- `PASSWORD_REQUIRED` - Password is required
- `PASSWORDS_DO_NOT_MATCH` - Passwords do not match

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
  "return_code": "REGISTRATION_SUCCESS",
  "message": "Registration successful. OTP sent.",
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
  "return_code": "VALIDATION_ERROR",
  "message": "Enter a valid email address.",
  "errors": {
    "email": ["email_invalid"]
  },
  "error_detail": "email_invalid"
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
  "return_code": "OTP_VERIFIED",
  "message": "OTP verified successfully.",
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
  "return_code": "OTP_INVALID",
  "message": "Invalid OTP."
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "return_code": "OTP_EXPIRED",
  "message": "OTP has expired."
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
  "return_code": "LOGIN_SUCCESS",
  "message": "Login successful.",
  "data": {
    "user": {
      "id": 1,
      "first_name": "Rahul",
      "last_name": "Sharma",
      "email": "rahul.sharma@gmail.com",
      "address": "123, MG Road, Connaught Place, New Delhi - 110001",
      "is_verified": true
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "role": "User"
  }
}

Error Response (401 UNAUTHORIZED):
{
  "success": false,
  "return_code": "INVALID_CREDENTIALS",
  "message": "Invalid email or password."
}

Error Response (403 FORBIDDEN):
{
  "success": false,
  "return_code": "ACCOUNT_NOT_VERIFIED",
  "message": "Please verify your account first."
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
  "return_code": "LOGOUT_SUCCESS",
  "message": "Logout successful.",
  "data": {}
}
```

### 5. View Profile
```json
GET /api/viewprofile/
Authorization: Bearer <access_token>

Response (200 OK):
{
  "success": true,
  "return_code": "PROFILE_RETRIEVED",
  "message": "Profile retrieved successfully.",
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
PATCH /api/editprofile/
Authorization: Bearer <access_token>
Content-Type: application/json

Request:
{
  "first_name": "Rahul Kumar",
  "address": "456, Nehru Place, New Delhi - 110019"
}

Response (200 OK):
{
  "success": true,
  "return_code": "PROFILE_UPDATED",
  "message": "Profile updated successfully.",
  "data": {
    "user": {
      "id": 1,
      "first_name": "Rahul Kumar",
      "last_name": "Sharma",
      "email": "rahul.sharma@gmail.com",
      "address": "456, Nehru Place, New Delhi - 110019",
      "profile_picture": null,
      "phone_number": "+919876543210",
      "is_verified": true
    }
  }
}
```

### 7. Change Password
```json
POST /api/changepassword/
Authorization: Bearer <access_token>
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
  "return_code": "PASSWORD_CHANGE_SUCCESS",
  "message": "Password changed successfully.",
  "data": {}
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "return_code": "INVALID_CREDENTIALS",
  "message": "Invalid email or password."
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "return_code": "PASSWORDS_DO_NOT_MATCH",
  "message": "Passwords do not match."
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
  "return_code": "PASSWORD_RESET_EMAIL_SENT",
  "message": "Password reset email sent.",
  "data": {}
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
  "return_code": "PASSWORD_CHANGE_SUCCESS",
  "message": "Password changed successfully.",
  "data": {}
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "return_code": "OTP_INVALID",
  "message": "Invalid OTP."
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "return_code": "OTP_EXPIRED",
  "message": "OTP has expired."
}
```

### 10. Get All Users (Authenticated)
```json
GET /api/getusers/
Authorization: Bearer <access_token>

Response (200 OK):
{
  "success": true,
  "return_code": "USERS_LIST_RETRIEVED",
  "message": "Users list retrieved successfully.",
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
Authorization: Bearer <admin_access_token>
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
  "return_code": "REGISTRATION_SUCCESS",
  "message": "Registration successful. OTP sent.",
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

### 12. Edit User (Admin Only)
```json
PATCH /api/edituser/2/
Authorization: Bearer <admin_access_token>
Content-Type: application/json

Request:
{
  "first_name": "Priya Devi",
  "address": "789, CG Road, Ahmedabad, Gujarat - 380009"
}

Response (200 OK):
{
  "success": true,
  "return_code": "PROFILE_UPDATED",
  "message": "Profile updated successfully.",
  "data": {
    "user": {
      "id": 2,
      "first_name": "Priya Devi",
      "last_name": "Patel",
      "email": "priya.patel@gmail.com",
      "address": "789, CG Road, Ahmedabad, Gujarat - 380009",
      "is_verified": true
    }
  }
}

Error Response (404 NOT FOUND):
{
  "success": false,
  "return_code": "USER_NOT_FOUND",
  "message": "User does not exist."
}
```

### 13. Update Password (Admin Only)
```json
PUT /api/updatepassword/2/
Authorization: Bearer <admin_access_token>
Content-Type: application/json

Request:
{
  "new_password": "Priya@456"
}

Response (200 OK):
{
  "success": true,
  "return_code": "PASSWORD_CHANGE_SUCCESS",
  "message": "Password changed successfully.",
  "data": {}
}

Error Response (400 BAD REQUEST):
{
  "success": false,
  "return_code": "PASSWORD_REQUIRED",
  "message": "Password is required."
}
```

### 14. Delete User (Admin Only)
```json
DELETE /api/deleteuser/2/
Authorization: Bearer <admin_access_token>

Response (200 OK):
{
  "success": true,
  "return_code": "USER_DELETED_SUCCESS",
  "message": "User account deleted successfully.",
  "data": {}
}

Error Response (404 NOT FOUND):
{
  "success": false,
  "return_code": "USER_NOT_FOUND",
  "message": "User does not exist."
}
```

## Testing with Postman

### Setup Environment
1. Create environment variable: `baseurll = http://localhost:8000/api/`
2. Create variable for access token: `token`

### Authentication Setup
1. In Postman collection, go to Authorization tab
2. Select Type: Bearer Token
3. Token: `{{token}}`
4. This will automatically add the token to all requests

### Testing Flow
1. **Sign Up** → Register user, OTP sent to email (check console)
2. **Verify Email** → Use OTP from console to verify email
3. **Sign In** → Login with verified credentials, save access_token to `{{token}}`
4. **View Profile** → Check user profile
5. **Edit Profile** → Update profile details
6. **Change Password** → Change password with old password
7. **Forget Password** → Request OTP for password reset
8. **Reset Password** → Reset password using OTP
9. **Sign In Again** → Login with new password

### Admin Testing
1. Create superuser via command line
2. Sign in as admin, save access_token
3. Test admin-only endpoints (adduser, edituser, deleteuser, updatepassword)


## Project Structure
```
DjangoCrud/
├── usermangement/              # Main app
│   ├── models.py              # User, EmailVerificationOTP, PasswordResetOTP models
│   ├── serializer.py          # DRF serializers with validation
│   ├── views.py               # API endpoints with transaction safety
│   ├── urls.py                # App URL routing
│   └── migrations/            # Database migrations
├── util/
│   ├── base_serializer.py     # Base serializer classes and error handling
│   ├── responses.py           # Standardized API response utilities
│   └── sent_otp.py            # OTP sending utility
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

### JWT Settings
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}
```


### Email Settings
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
- Rotate JWT secret keys periodically
- Implement token refresh mechanism
- Consider token blacklisting for logout

### Current Setup
- Development mode (DEBUG=True)
- JWT authentication with access & refresh tokens
- SQLite database
- No rate limiting (add in production)


## Error Handling

The API uses a standardized error handling approach with:
- Custom error codes for all scenarios
- Field-specific validation errors
- Prioritized error messages (e.g., confirm_password errors shown first)
- Detailed error information for debugging
- User-friendly error messages

## Utility Functions

### APIResponse Class
Standardized response creator with methods:
- `get_success_response()` - Success responses with data
- `get_error_response()` - Generic error responses
- `get_validation_error_response()` - Validation error responses with field details

### send_otp()
Reusable OTP sending function used for:
- Email verification during registration
- Account verification when unverified user tries to login

## Dependencies
```
Django==5.2.9
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
Pillow==10.0.0
django-phonenumber-field==7.1.0
phonenumbers==8.13.18
```

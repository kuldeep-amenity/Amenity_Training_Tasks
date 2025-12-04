# Django User Management API

## Project Overview
A complete Django REST API for user management with authentication, authorization, and password reset functionality. Built using Django REST Framework with session-based authentication.

## Key Features
- Complete user CRUD operations with proper permissions
- User registration and authentication system
- Secure password reset flow with email tokens
- Role-based access control (Admin/User)
- Custom user model using email as primary identifier
- Transaction-safe database operations

## Tech Stack
- **Framework:** Django 5.2.6
- **API:** Django REST Framework
- **Database:** SQLite3
- **Authentication:** Session-based
- **Email:** Console backend (development)

## Models

### User
- Custom user model extending AbstractUser
- Fields: email (unique), first_name, last_name, address, password
- Email used as username field

### PasswordResetToken
- Links user to UUID token for password resets
- Auto-generated token with timestamp

## API Endpoints

### User Management
- `GET /api/getusers/` - List all users (authenticated)
- `POST /api/adduser/` - Create user (admin only)
- `PUT /api/edituser/<id>/` - Update user (owner or admin)
- `DELETE /api/deleteuser/<id>/` - Delete user (admin only)
- `PUT /api/updatepassword/<id>/` - Change password (owner or admin)

### Authentication
- `POST /api/signup/` - Register new user (admin only)
- `POST /api/signin/` - Login with email/password
- `GET/POST /api/signout/` - Logout

### Password Reset
- `POST /api/forgetpassword/` - Request reset link via email
- `POST /api/resetpassword/` - Reset password with token

## Setup

1. Install dependencies:
```bash
pip install django djangorestframework
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py createsuperuser
```

4. Run server:
```bash
python manage.py runserver
```

## Permission Requirements

| Endpoint | Permission Required |
|----------|-------------------|
| GET /api/getusers/ | Authenticated user |
| POST /api/adduser/ | Admin only |
| PUT /api/edituser/<id>/ | Owner or Admin |
| DELETE /api/deleteuser/<id>/ | Admin only |
| PUT /api/updatepassword/<id>/ | Owner or Admin |
| POST /api/signup/ | Admin only |
| POST /api/signin/ | Public |
| GET/POST /api/signout/ | Public |
| POST /api/forgetpassword/ | Public |
| POST /api/resetpassword/ | Public |

## Project Structure
```
DjangoCrud/
├── usermangement/          # Main app
│   ├── models.py          # User & PasswordResetToken models
│   ├── serializer.py      # DRF serializers
│   ├── views.py           # API endpoints
│   └── urls.py            # App URL routing
├── DjangoCrud/
│   ├── settings.py        # Project settings
│   └── urls.py            # Main URL config
└── db.sqlite3             # Database
```

## Configuration
- **Debug mode:** ON (development)
- **Email backend:** Console (prints to terminal)
- **Authentication:** Session-based
- **Default permissions:** IsAuthenticated
- **Custom user model:** usermangement.User

## Request/Response Examples

### 1. Get All Users
```json
GET /api/getusers/
Headers: Session cookie required

Response (200 OK):
[
  {
    "id": 1,
    "first_name": "Raj",
    "last_name": "Patel",
    "email": "raj.patel@example.com",
    "address": "Kalawad Road, Rajkot"
  },
  {
    "id": 2,
    "first_name": "Priya",
    "last_name": "Shah",
    "email": "priya.shah@example.com",
    "address": "University Road, Rajkot"
  }
]
```

### 2. Add User (Admin Only)
```json
POST /api/adduser/
Headers: Session cookie required (admin)
{
  "first_name": "Amit",
  "last_name": "Mehta",
  "email": "amit.mehta@example.com",
  "address": "150 Feet Ring Road, Rajkot",
  "password": "password123"
}

Response (201 CREATED):
{
  "id": 1,
  "first_name": "Amit",
  "last_name": "Mehta",
  "email": "amit.mehta@example.com",
  "address": "150 Feet Ring Road, Rajkot"
}

Error Response (400 BAD REQUEST):
{
  "email": ["user with this email already exists."],
  "password": ["This field is required."]
}
```

### 3. Edit User
```json
PUT /api/edituser/1/
Headers: Session cookie required
{
  "first_name": "Rajesh",
  "last_name": "Patel",
  "address": "Trikon Baug, Rajkot"
}

Response (200 OK):
{
  "id": 1,
  "first_name": "Rajesh",
  "last_name": "Patel",
  "email": "raj.patel@example.com",
  "address": "Trikon Baug, Rajkot"
}

Error Response (404 NOT FOUND):
{
  "error": "User not found"
}

Error Response (403 FORBIDDEN):
{
  "error": "Permission denied"
}
```

### 4. Update Password
```json
PUT /api/updatepassword/1/
Headers: Session cookie required
{
  "password": "currentpassword123",
  "new_password": "newpassword456"
}

Response (200 OK):
{
  "message": "Password updated successfully"
}

Error Response (400 BAD REQUEST):
{
  "error": "Current password is incorrect"
}

Error Response (400 BAD REQUEST):
{
  "error": "New password cannot be the same as the current password"
}

Admin Request (no current password needed):
{
  "new_password": "newpassword456"
}
```

### 5. Delete User (Admin Only)
```json
DELETE /api/deleteuser/1/
Headers: Session cookie required (admin)

Response (204 NO CONTENT):
{
  "message": "User deleted successfully"
}

Error Response (404 NOT FOUND):
{
  "error": "User not found"
}
```

### 6. Sign Up (Admin Only)
```json
POST /api/signup/
Headers: Session cookie required (admin)
{
  "first_name": "Kavita",
  "last_name": "Joshi",
  "email": "kavita.joshi@example.com",
  "address": "Panchnath Plot, Rajkot",
  "password": "password123"
}

Response (201 CREATED):
{
  "user": {
    "id": 1,
    "first_name": "Kavita",
    "last_name": "Joshi",
    "email": "kavita.joshi@example.com",
    "address": "Panchnath Plot, Rajkot"
  },
  "message": "User registered successfully"
}
```

### 7. Sign In
```json
POST /api/signin/
{
  "email": "raj.patel@example.com",
  "password": "password123"
}

Response (200 OK):
{
  "user": {
    "id": 1,
    "first_name": "Raj",
    "last_name": "Patel",
    "email": "raj.patel@example.com",
    "address": "Kalawad Road, Rajkot"
  },
  "message": "User Login successful"
}

Superuser Response:
{
  "user": {...},
  "message": "Superuser Login successful"
}

Error Response (400 BAD REQUEST):
{
  "error": "Email and password required"
}

Error Response (401 UNAUTHORIZED):
{
  "error": "Invalid email or password"
}
```

### 8. Sign Out
```json
GET /api/signout/
or
POST /api/signout/

Response (200 OK):
{
  "message": "Logged out successfully"
}
```

### 9. Forget Password
```json
POST /api/forgetpassword/
{
  "email": "raj.patel@example.com"
}

Response (200 OK):
{
  "message": "Reset link sent to your email."
}

Note: Same response even if email doesn't exist (security)

Error Response (500 INTERNAL SERVER ERROR):
{
  "error": "Email sending error message"
}
```

### 10. Reset Password
```json
POST /api/resetpassword/
{
  "token": "550e8400-e29b-41d4-a716-446655440000",
  "new_password": "newpassword123"
}

Response (200 OK):
{
  "message": "Password has been reset successfully"
}

Error Response (400 BAD REQUEST):
{
  "error": "Invalid or expired token"
}

Error Response (400 BAD REQUEST):
{
  "token": ["This field is required."],
  "new_password": ["Ensure this field has at least 6 characters."]
}
```

## Security Notes
- Change SECRET_KEY in production
- Set DEBUG=False in production
- Use proper email backend for production
- Current setup suitable for development only
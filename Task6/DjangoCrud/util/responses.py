from rest_framework.response import Response
from rest_framework import status
from util.base_serializer import get_error_message


class APIResponse:
    class Codes:

        # -------------------------
        # SUCCESS CODES
        # -------------------------
        REGISTRATION_SUCCESS = "REGISTRATION_SUCCESS"
        LOGIN_SUCCESS = "LOGIN_SUCCESS"
        OTP_VERIFIED = "OTP_VERIFIED"
        OTP_RESENT = "OTP_RESENT"
        PASSWORD_RESET_EMAIL_SENT = "PASSWORD_RESET_EMAIL_SENT"
        PASSWORD_CHANGE_SUCCESS = "PASSWORD_CHANGE_SUCCESS"
        LOGOUT_SUCCESS = "LOGOUT_SUCCESS"
        USER_DELETED_SUCCESS = "USER_DELETED_SUCCESS"
        PROFILE_RETRIEVED = "PROFILE_RETRIEVED"
        PROFILE_UPDATED = "PROFILE_UPDATED"
        USERS_LIST_RETRIEVED = "USERS_LIST_RETRIEVED"

        # -------------------------
        # ERROR CODES
        # -------------------------
        VALIDATION_ERROR = "VALIDATION_ERROR"
        INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
        ACCOUNT_NOT_VERIFIED = "ACCOUNT_NOT_VERIFIED"
        ACCOUNT_INACTIVE = "ACCOUNT_INACTIVE"
        EMAIL_REQUIRED = "EMAIL_REQUIRED"
        USER_NOT_FOUND = "USER_NOT_FOUND"
        EMAIL_NOT_FOUND = "EMAIL_NOT_FOUND"
        EMAIL_OTP_REQUIRED = "EMAIL_OTP_REQUIRED"
        OTP_REQUIRED = "OTP_REQUIRED"
        OTP_INVALID = "OTP_INVALID"
        OTP_EXPIRED = "OTP_EXPIRED"
        PASSWORD_REQUIRED = "PASSWORD_REQUIRED"
        PASSWORDS_DO_NOT_MATCH = "PASSWORDS_DO_NOT_MATCH"
        TOKEN_INVALID = "TOKEN_INVALID"
        INVALID_LINK = "INVALID_LINK"
        LOGIN_CREDENTIAL_INVALID = "LOGIN_CREDENTIAL_INVALID"
        OTP_VERIFICATION_FAILED = "OTP_VERIFICATION_FAILED"
        USER_DELETED = "USER_DELETED"
        EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
        PASSWORD_LENGTH_INVALID = "PASSWORD_LENGTH_INVALID"

        # -------------------------
        # SUCCESS MESSAGES
        # -------------------------
        _success_messages = {
            REGISTRATION_SUCCESS: "Registration successful. OTP sent.",
            LOGIN_SUCCESS: "Login successful.",
            OTP_VERIFIED: "OTP verified successfully.",
            OTP_RESENT: "OTP resent successfully.",
            PASSWORD_RESET_EMAIL_SENT: "Password reset email sent.",
            PASSWORD_CHANGE_SUCCESS: "Password changed successfully.",
            LOGOUT_SUCCESS: "Logout successful.",
            USER_DELETED_SUCCESS: "User account deleted successfully.",
            PROFILE_RETRIEVED: "Profile retrieved successfully.",
            PROFILE_UPDATED: "Profile updated successfully.",
            USERS_LIST_RETRIEVED: "Users list retrieved successfully.",
        }

        # -------------------------
        # ERROR MESSAGES
        # -------------------------
        _error_messages = {
            VALIDATION_ERROR: "Validation failed.",
            INVALID_CREDENTIALS: "Invalid email or password.",
            ACCOUNT_NOT_VERIFIED: "Please verify your account first.",
            ACCOUNT_INACTIVE: "Account is inactive.",
            EMAIL_REQUIRED: "Email is required.",
            EMAIL_NOT_FOUND: "Email not found.",
            USER_NOT_FOUND: "User does not exist.",
            EMAIL_OTP_REQUIRED: "Email and OTP are required.",
            OTP_REQUIRED: "OTP is required.",
            OTP_INVALID: "Invalid OTP.",
            OTP_EXPIRED: "OTP has expired.",
            PASSWORD_REQUIRED: "Password is required.",
            PASSWORDS_DO_NOT_MATCH: "Passwords do not match.",
            TOKEN_INVALID: "Token is invalid or expired.",
            INVALID_LINK: "Invalid reset password link.",
            LOGIN_CREDENTIAL_INVALID: "Invalid login credentials.",
            OTP_VERIFICATION_FAILED: "OTP verification failed.",
            USER_DELETED: "User account deleted.",
            EMAIL_ALREADY_EXISTS: "Email already exists.",
            PASSWORD_LENGTH_INVALID: "Password must be 8-16 characters long and contain at least one number and one special character.",
        }

    # --------------------------------------------------------
    # SUCCESS RESPONSE
    # --------------------------------------------------------
    @staticmethod
    def get_success_response(return_code, data=None, status_code=status.HTTP_200_OK):
        message = APIResponse.Codes._success_messages.get(return_code, "Success")

        return Response(
            {
                "success": True,
                "return_code": return_code,
                "message": message,
                "data": data or {},
            },
            status=status_code,
        )

    # --------------------------------------------------------
    # GENERIC ERROR RESPONSE
    # --------------------------------------------------------
    @staticmethod
    def get_error_response(return_code, status_code=status.HTTP_400_BAD_REQUEST):
        message = APIResponse.Codes._error_messages.get(return_code, "Error")

        return Response(
            {
                "success": False,
                "return_code": return_code,
                "message": message,
            },
            status=status_code,
        )

    # --------------------------------------------------------
    # SERIALIZER ERROR RESPONSE
    # --------------------------------------------------------
    @staticmethod
    def get_serializer_error_response(return_code, serializer_errors):
        message = APIResponse.Codes._error_messages.get(return_code, "Validation error")

        return Response(
            {
                "success": False,
                "return_code": return_code,
                "message": message,
                "errors": serializer_errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def get_validation_error_response(return_code, serializer_errors, error_messages_dict=None):
        try:
            raw, friendly, field_name = get_error_message(
                serializer_errors, error_messages_dict or {}
            )
        except Exception:
            # Fallback to generic behavior
            friendly = APIResponse.Codes._error_messages.get(return_code, "Validation error")
            raw = None
            field_name = None

        # Build minimal errors payload with only the first field
        errors_payload = {}
        if field_name:
            errors_payload[field_name] = [raw]

        payload = {
            "success": False,
            "return_code": return_code,
            "message": friendly,
            "errors": errors_payload,
        }
        if raw:
            payload["error_detail"] = raw

        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

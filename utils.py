from enum import Enum

class ResponseCodes(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    REGISTRATION_FAILED = "REGISTRATION_FAILED"
    LOGIN_FAILED = "LOGIN_FAILED"
    AUTH_FAILED = "AUTH_FAILED"
    LOGOUT_FAILED = "LOGOUT_FAILED"
    PROFILE_RETRIEVE_FAILED = "PROFILE_RETRIEVE_FAILED"
    PROFILE_UPDATE_FAILED = "PROFILE_UPDATE_FAILED"
    ORDER_CREATION_FAILED = "ORDER_CREATION_FAILED"
    ORDER_COUNT_FAILED = "ORDER_COUNT_FAILED"


def create_response(status, code, success, data, error_code=None, message=None):
    response = {
        "status": status,
        "code": code,
        "success": success,
        "data": data,
        "error_code": error_code,
        "message": message,
    }
    return response

class BusinessException(Exception):
    """
    User defined function to handle 4xx response
    """
    def __init__(self, message):
        super().__init__(message)

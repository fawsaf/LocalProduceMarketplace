from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import service
from utils import *

@api_view(['POST'])
def register_user(request):
    try:
        user = service.register_user_service(**request.data)
        response = create_response(200, ResponseCodes.SUCCESS, True, {"user_id": user.id}, None, "User registered successfully.")
        return Response(response, status=200)
    except BusinessException as e:
        # Handle known business logic errors specifically
        response = create_response(400, ResponseCodes.REGISTRATION_FAILED, False, None, ResponseCodes.REGISTRATION_FAILED, str(e))
        return Response(response, status=400)
    except Exception as e:
        # Catch-all for unexpected errors
        response = create_response(500, ResponseCodes.ERROR, False, None, "UNKNOWN_ERROR", "An unexpected error occurred during registration.")
        return Response(response, status=500)


@api_view(['POST'])
def login_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        token = service.login_user_service(username, password)
        response = create_response(200, ResponseCodes.SUCCESS, True, {"token": token}, None, "Login successful.")
        return Response(response, status=200)
    except BusinessException as e:
        # Handling business logic errors specifically
        response = create_response(401, ResponseCodes.AUTH_FAILED, False, None, ResponseCodes.LOGIN_FAILED, str(e))
        return Response(response, status=401)
    except Exception as e:
        # Catch-all for other unexpected errors
        response = create_response(500, ResponseCodes.ERROR, False, None, "UNKNOWN_ERROR", "An unexpected error occurred.")
        return Response(response, status=500)

@api_view(['GET', 'PUT'])
def user_profile(request):
    try:
        if request.method == 'GET':
            profile_data = service.get_user_profile_service(request.user)
            response = create_response(200, ResponseCodes.SUCCESS, True, profile_data, None, "Profile data retrieved.")
        elif request.method == 'PUT':
            updated_profile = service.update_user_profile_service(request.user, **request.data)
            response = create_response(200, ResponseCodes.SUCCESS, True, updated_profile, None, "Profile updated successfully.")
    except BusinessException as e:
        # Handle known business logic errors specifically for profile actions
        response = create_response(400, ResponseCodes.PROFILE_UPDATE_FAILED, False, None, ResponseCodes.PROFILE_UPDATE_FAILED, str(e))
        return Response(response, status=400)
    except Exception as e:
        # Catch-all for unexpected errors
        response = create_response(500, ResponseCodes.ERROR, False, None, "UNKNOWN_ERROR", "An unexpected error occurred while managing the profile.")
        return Response(response, status=500)
    return Response(response, status=200)

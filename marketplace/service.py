from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from ..utils import *
from .serializers import UserSerializer
from .models import *

def register_user_service(username, email, password, **extra_fields):
    if User.objects.filter(email=email).exists():
        raise BusinessException(f"Username '{username}' is already taken.")
    user = User.objects.create_user(username=username, email=email, password=password, **extra_fields)
    return user

def login_user_service(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise BusinessException("Invalid username or password.")
    token, _ = Token.objects.get_or_create(user=user)
    update_last_login(None, user)  # Update last_login
    return token.key

def get_user_profile_service(user_id):
    try:
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user)
        return serializer.data
    except User.DoesNotExist:
        raise BusinessException(f"User with ID {user_id} not found.")

def update_user_profile_service(user_id, updated_data):
    try:
        # Retrieve the user instance
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise BusinessException(f"User with ID {user_id} not found.")
    
    # Define the allowed fields to update
    allowed_fields = ['email', 'first_name', 'last_name', 'phone_number']  # Customize as needed

    # Update only the allowed fields
    for field, value in updated_data.items():
        if field in allowed_fields:
            setattr(user, field, value)
        else:
            # If trying to update a field not in allowed_fields, raise an exception
            raise BusinessException(f"Field '{field}' not recognized or not allowed to be updated.")

    # Save the user object after making changes
    user.save()
    serializer = UserSerializer(user)
    
    # Return the serializer data
    return serializer.data
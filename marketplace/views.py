from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import service
from utils import *
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def register_user(request):
    try:
        user = service.register_user_service(**request.data)
        response = create_response(200, ResponseCodes.SUCCESS, True, user, None, "User registered successfully.")
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
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            response=create_response(200, "LOGIN_SUCCESS", True, {"token": token.key}, None, None)
            return Response(response, status=200)
        else:
            response=create_response(401, ResponseCodes.ERROR, False, {}, "Invalid Credentials", "Authentication failed")
            return Response(response, status=200)
    except Exception as e:
        response=create_response(500, ResponseCodes.ERROR, False, {}, "Error", str(e))
        return response

@api_view(['GET', 'PUT'])
def user_profile(request):
    try:
        if request.method == 'GET':
            user=request.user
            data=request.data
            profile_data = service.get_user_profile_service(user)
            response = create_response(200, ResponseCodes.SUCCESS, True, profile_data, None, "Profile data retrieved.")
        elif request.method == 'PUT':
            updated_profile = service.update_user_profile_service(user, **data)
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


@api_view(['POST'])
@login_required
def create_product(request):
    try:
        data=request.data
        user=request.user
        product = service.create_product_service(data, user)
        return Response(create_response(200, "PRODUCT_CREATED", True, product, None, "Product created successfully."))
    except BusinessException as e:
        # Handle validation errors
        return Response(create_response(400, "INVALID_DATA", False, {}, "Invalid Data", str(e)))
    except Exception as e:
        # Handle other exceptions
        return Response(create_response(500, "ERROR", False, {}, "Error", str(e)))

@api_view(['GET'])
def list_products(request):
    data=request.data
    try:
        products = service.list_products_service(**data)  # Assuming this service returns a QuerySet of products
        return Response(create_response(200, "PRODUCTS_LISTED", True, products, None, None))
    except BusinessException as e:
        # Handle validation errors
        return Response(create_response(400, "INVALID_DATA", False, {}, "Invalid Data", str(e)))
    except Exception as e:
        # Handle other exceptions
        return Response(create_response(500, "ERROR", False, {}, "Error", str(e)))

@api_view(['PUT', 'DELETE'])
@login_required
def update_product(request, pk):
    if request.method == 'PUT':
        try:
            data=request.data
            data.pop('quantity_available', None)
            product = service.update_product_service(pk, data, request.user)
            return Response(create_response(200, "PRODUCT_UPDATED", True, product, None, "Product updated successfully."))
        except BusinessException as e:
            return Response(create_response(400, "INVALID_DATA", False, {}, "Invalid Data", str(e)))
        except Exception as e:
            return Response(create_response(500, "ERROR", False, {}, "Error", str(e)))

    elif request.method == 'DELETE':
        try:
            user=request.user
            service.delete_product_service(pk, user)
            return Response(create_response(200, "PRODUCT_DELETED", True, {}, None, "Product deleted successfully."))
        except BusinessException as e:
            return Response(create_response(404, "PRODUCT_NOT_FOUND", False, {}, "Product not found", "The requested product does not exist or does not belong to you."))
        except Exception as e:
            return Response(create_response(500, "ERROR", False, {}, "Error", str(e)))

@api_view(['POST'])
@login_required
def create_order(request):
    try:
        data=request.data
        user=request.user
        order = service.create_order_service(data, user)
        return Response(create_response(200, "ORDER_PLACED", True, order, None, "Order placed successfully."))
    except BusinessException as e:
        return Response(create_response(400, "INVALID_ORDER_DATA", False, {}, "Invalid Order Data", str(e)))
    except Exception as e:
        return Response(create_response(500, "ERROR", False, {}, "Error", str(e)))

@api_view(['GET'])
@login_required
def list_orders(request):
    user=request.user
    orders = service.list_orders_service(user)  # Assuming this service returns a QuerySet of orders
    return Response(create_response(200, "ORDERS_LISTED", True, orders, None, None))

@api_view(['PATCH'])
@login_required
def update_stock_level(request, product_id):
    try:
        new_quantity = request.data.get('quantity_available')
        product = service.update_stock_level_service(product_id, request.user, new_quantity)
        return Response(create_response(200, ResponseCodes.SUCCESS, True, product, None, "Stock level updated successfully."))
    except PermissionError as e:
        return Response(create_response(403, "FORBIDDEN", False, {}, "Forbidden", str(e)))
    except BusinessException as e:
        return Response(create_response(400, "INVALID_QUANTITY", False, {}, "Invalid Quantity", str(e)))
    except Exception as e:
        return Response(create_response(500, "ERROR", False, {}, "Error", str(e)))
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review_or_comment(request, product_id):
    try:
        review = service.create_review_or_comment_service(user=request.user, product_id=product_id, data=request.data)
        return Response(create_response(200, ResponseCodes.SUCCESS, True, review, None, "Stock level updated successfully."))
    except BusinessException as e:
        return Response(create_response(400, "INVALID_QUANTITY", False, {}, "Invalid Quantity", str(e)))
    except Exception as e:
        # Catch-all for unexpected errors
        response = create_response(500, ResponseCodes.ERROR, False, None, "UNKNOWN_ERROR", "An unexpected error occurred during registration.")
        return Response(response, status=500)


@api_view(['GET'])
def list_reviews_with_comments(request, product_id):
    try:
        reviews = service.list_reviews_with_comments_service(product_id)
        # Note: You pass many=True to serialize a queryset or list of objects instead of a single object.
        return Response(create_response(200, ResponseCodes.SUCCESS, True, reviews, None, "Stock level updated successfully."))
    except BusinessException as e:
        return Response({"detail": str(e)}, status=400)
    except Exception as e:
        # Catch-all for unexpected errors
        response = create_response(500, ResponseCodes.ERROR, False, None, "UNKNOWN_ERROR", "An unexpected error occurred during registration.")
        return Response(response, status=500)

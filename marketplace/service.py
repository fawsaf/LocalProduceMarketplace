from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from utils import *
from .serializers import *
from .models import *
from django.db import transaction
import json
def register_user_service(username, email, password, is_farmer=False, is_consumer=False,**extra_fields):
    if User.objects.filter(email=email).exists():
        raise BusinessException(f"Username '{username}' is already taken.")
    user = User.objects.create_user(username=username, email=email, password=password, is_farmer=is_farmer, is_consumer=is_consumer,**extra_fields)
    serializer= UserSerializer(user)
    return serializer.data

def logout_user_service(user):
    try:
        token = Token.objects.get(user=user)
        token.delete()
    except Token.DoesNotExist:
        # Raise a BusinessException if the token does not exist
        raise BusinessException("Authentication token not found.")
    except Exception as e:
        # Raise a generic exception for any unexpected errors
        raise Exception(f"Unexpected error during logout: {str(e)}")

def get_user_profile_service(user_id):
    try:
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user)
        return serializer.data
    except User.DoesNotExist:
        raise BusinessException(f"User with ID {user_id} not found.")

def update_user_profile_service(user_id, updated_data):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise BusinessException(f"User with ID {user_id} not found.")
    
    # Define the allowed fields to update, possibly including role fields
    allowed_fields = ['email', 'phone_number', 'address', 'is_farmer', 'is_consumer']

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

def create_product_service(data, user):
    # Directly creating the product instance
    product = Product.objects.create(
        farmer=user,
        name=data['name'],
        category=data['category'],
        price=data['price'],
        quantity_available=data['quantity_available'],
        description=data['description'],  # Defaulting to empty string if no description is provided
        image_url=data['image_url']
    )
    serializer = ProductSerializer(product)
    return serializer.data  # Returning the product instance

def list_products_service(category=None, search_query=None):
    products = Product.objects.all()
    
    if category:
        products = products.filter(category=category)
        
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    return products

def update_product_service(product_id, data, user):
    product = Product.objects.get(pk=product_id, farmer=user)
    
    serializer = ProductSerializer(product, data=data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return serializer.data

def delete_product_service(product_id, user):
    product = Product.objects.get(pk=product_id, farmer=user)
    product.delete()

def create_order_service(data, user):
    # Assuming data validation is already handled by the view before calling this service
    order = Order.objects.create(
        consumer=user,
        total_price=data['total_price'],  # Assuming total_price is part of the data passed
        status=data.get('status', 'Placed')  # Defaulting to 'Placed' if no status is provided
    )

    # Handling Order Items if present in the data
    for item in data.get('items', []):
        OrderItem.objects.create(
            order=order,
            product_id=item['product'],  # Assuming product ID is passed directly
            quantity=item['quantity']
        )

    return order  # Returning the order instance

def list_orders_service(user):
    orders = Order.objects.filter(consumer=user)
    serializer = OrderSerializer(orders, many=True)
    return serializer.data



def create_review_or_reply_service(user, product_id, parent_id=None, rating=None, comment=None):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise BusinessException("Product not found.")

    # Optional: Validate the parent_id if provided
    parent = None
    if parent_id:
        try:
            parent = Review.objects.get(pk=parent_id, product=product)
        except Review.DoesNotExist:
            raise BusinessException("Parent review not found.")

    review = Review.objects.create(
        product=product,
        author=user,
        parent=parent,
        rating=rating,
        comment=comment
    )

    return review

def list_reviews_with_replies_service(product_id):
    try:
        # This fetches only top-level reviews
        reviews = Review.objects.filter(product_id=product_id, parent__isnull=True)
        return reviews
    except Review.DoesNotExist:
        raise BusinessException("Product not found.")

def create_review_or_comment_service(user, product_id, data):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise BusinessException("Product not found.")

    parent_id = data.get('parent')
    parent_review = None
    if parent_id:
        try:
            parent_review = Review.objects.get(id=parent_id, product=product)
        except Review.DoesNotExist:
            raise BusinessException("Parent review does not exist.")
    
    review = Review(
        product=product,
        author=user,
        parent=parent_review,
        rating=data.get('rating'),
        comment=data.get('comment')
    )
    review.save()
    serializer = ReviewSerializer(review)
    return serializer.data

def list_reviews_with_comments_service(product_id):
    # Fetches only top-level reviews; their comments are accessible via the related name 'comments'
    reviews = Review.objects.filter(product_id=product_id, parent__isnull=True).prefetch_related('comments')
    serializer = ReviewSerializer(reviews, many=True)
    return serializer.data

def create_bulk_products_service(products_data,farmer):
    # Assuming products_data is a list of dictionaries with product information
    if not isinstance(products_data, list):
        raise ValueError("Expected a list of product data.")

    # Prepare a list to hold Product instances
    products_to_create = []

    for product_data in products_data:
        # Perform necessary validation on product_data here
        # For simplicity, this example assumes product_data is valid and complete
        
        # Create a Product instance for each product (without saving to the database)
        product_instance = Product(
            name=product_data['name'],
            description=product_data.get('description', ''),
            price=product_data['price'],
            quantity_available=product_data.get('quantity_available', 0),
            image_url=product_data.get('image_url', ''),  # Assuming these keys exist in your product_data
            farmer=farmer
        )
        products_to_create.append(product_instance)

    # Use Django's bulk_create to insert all products at once
    # The use of transaction.atomic() ensures that all products are created successfully
    # or none at all if any error occurs, maintaining database integrity
    with transaction.atomic():
        created_products = Product.objects.bulk_create(products_to_create)
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid
class User(AbstractUser):
    # Add related_name to groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="marketplace_user_set",  # Unique related_name
        related_query_name="marketplace_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="marketplace_user_permission_set",  # Unique related_name
        related_query_name="marketplace_user_permission",
    )
    # Directly available fields from AbstractUser (no need to redefine these in the model):
    # - username (String): A unique identifier for the user.
    # - first_name (String): The user's first name.
    # - last_name (String): The user's last name.
    # - email (String): The user's email address.
    # - password (String): Hashed password for the user.
    # - is_staff (Boolean): Designates whether the user can log into the admin site.
    # - is_active (Boolean): Determines whether this user should be treated as active.
    # - is_superuser (Boolean): Designates that this user has all permissions without explicitly assigning them.
    # - last_login (DateTime): A timestamp of the user's last login.
    # - date_joined (DateTime): When the user account was created.
    
    # Additional custom fields for the marketplace:
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    email = models.EmailField(null=False, blank=False)
    is_farmer = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    # Consider adding an image field and more metadata as needed.

class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    consumer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Placed')  # E.g., Placed, Shipped, Delivered, Cancelled

class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Review(models.Model):
    product = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    '''
class FarmingData(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farming_data')
    crop_type = models.CharField(max_length=255)
    soil_type = models.CharField(max_length=255)
    weather_condition = models.CharField(max_length=255)
    pest_disease_incident = models.CharField(max_length=255)
    irrigation_method = models.CharField(max_length=255)
    fertilizer_use = models.CharField(max_length=255)
    planting_date = models.DateField()
    harvest_date = models.DateField()
    yield_per_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class FarmingRecommendation(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommended_product = models.CharField(max_length=255)
    reasons = models.TextField()  # E.g., "High demand in upcoming season", "Suitable weather forecast"
    season = models.CharField(max_length=100)
    # You might also store weather conditions, soil type, etc., if relevant for generating recommendations.
'''

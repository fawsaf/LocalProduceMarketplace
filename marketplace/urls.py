from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('user/register_user/', views.register_user, name='register_user'),
    path('user/login_user/', views.login_user, name='login_user'),
    path('user/user_profile/', views.user_profile, name='user_profile'),
    
    # Product Management URLs
    path('products/create/', views.create_product, name='create_product'),
    path('products/', views.list_products, name='list_products'),
    path('products/update/<uuid:pk>/', views.update_product, name='manage_product'),
    path('products/<int:product_id>/update-stock/', views.update_stock_level, name='update_stock_level'),
    path('products/<int:product_id>/reviews/', views.create_review_or_comment, name='create_review_or_comment'),
    path('products/<int:product_id>/reviews/comments/', views.list_reviews_with_comments, name='list_reviews_with_comments'),

    # Order Management URLs
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/', views.list_orders, name='list_orders'),
    # Add more paths as needed
    
    
]

from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('user_profile/', views.user_profile, name='user_profile'),
    
    # Product Management URLs
    path('create_product/', views.create_product, name='create_product'),
    path('list_products/', views.list_products, name='list_products'),
    path('update_product/<id>/', views.update_product, name='manage_product'),
    path('create_review_or_comment/product_id>/', views.create_review_or_comment, name='create_review_or_comment'),
    path('list_reviews_with_comments/<product_id>/', views.list_reviews_with_comments, name='list_reviews_with_comments'),
    path('bulk_create_products/', views.bulk_create_products, name='bulk_create_products'),
    # Order Management URLs
    path('create_order/', views.create_order, name='create_order'),
    path('list_orders/', views.list_orders, name='list_orders'),
    # Add more paths as needed
    
]

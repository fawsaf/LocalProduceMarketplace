from django.urls import path
from . import views

urlpatterns = [
    # Define your marketplace app's URLs here
    path('user/register_user/', views.register_user, name='products'),
    path('user/login_user/', views.login_user, name='products'),
    path('user/user_profile/', views.user_profile, name='user_profile'),
    # Add more paths as needed
]

from django.contrib.auth import get_user_model
from rest_framework import serializers
from marketplace.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']  # Assuming you don't want these to be updated

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image_url','quantity_available']
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'consumer', 'total_price', 'created_at', 'status', 'items']

class ReviewSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'product', 'author', 'parent', 'rating', 'comment', 'created_at', 'comments']
        read_only_fields = ['id', 'author', 'created_at', 'comments']

    def get_comments(self, obj):
        # Fetch comments related to the review
        comments = obj.comments.all()
        # Serialize the comments using a simplified structure
        return CommentSerializer(comments, many=True, read_only=True).data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'author', 'comment', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

from rest_framework import serializers
from .models import Wishlist

class WishlistSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="product.title")
    price = serializers.ReadOnlyField(source="product.price")
    img = serializers.ReadOnlyField(source="product.img")
    category = serializers.ReadOnlyField(source="product.category.name")

    class Meta:
        model = Wishlist
        fields = ["id", "product", "title", "price", "img", "category"]

class WishlistCreateSerializer(serializers.Serializer):
    product = serializers.IntegerField()
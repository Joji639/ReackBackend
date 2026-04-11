

from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="product.title")
    price = serializers.ReadOnlyField(source="product.price")
    img = serializers.ReadOnlyField(source="product.img")
    category = serializers.ReadOnlyField(source="product.category.name")

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "product",
            "title",
            "price",
            "img",
            "category",
            "quantity",
            "total_price"
        ]

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price


class CartCreateSerializer(serializers.Serializer):
    product = serializers.IntegerField()

class CartUpdateSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=["increase", "decrease"],
        required=True
    )
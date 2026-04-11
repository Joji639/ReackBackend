from rest_framework import serializers
from allproducts.models import Products, Category
from User.models import UserModel
from paymentpage.models import Order, OrderItem



class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "username", "email", "role", "status"]



class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"



class AdminOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.title")
    img = serializers.ReadOnlyField(source="product.img")

    class Meta:
        model = OrderItem
        fields = ["product", "product_name","img", "quantity", "price"]



class AdminOrderSerializer(serializers.ModelSerializer):
    items = AdminOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

class UpdateUserStatusSerializer(serializers.Serializer):
    pass  


class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=["pending", "confirmed", "shipped", "delivered"]
    )
from rest_framework import serializers
from .models import Order, OrderItem
from allproducts.models import Products
from cart.models import Cart


class OrderItemSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="product.title")
    img = serializers.ReadOnlyField(source="product.img")

    class Meta:
        model = OrderItem
        fields = ["product", "title", "img", "quantity", "price"]


class PaymentSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["user"] 

    def validate(self, data):
        if not data.get("full_name") or len(data["full_name"].strip()) < 3:
            raise serializers.ValidationError({"full_name": "Name must be at least 3 characters"})

        if not data.get("phone") or not data["phone"].isdigit() or len(data["phone"]) != 10:
            raise serializers.ValidationError({"phone": "Phone must be 10 digits"})

        if not data.get("address"):
            raise serializers.ValidationError({"address": "Address is required"})

        if data.get("payment_method") not in ["upi", "card", "cod"]:
            raise serializers.ValidationError({"payment_method": "Invalid payment method"})

        return data


class PaymentRequestSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["cart", "single"])
    full_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    address = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=["upi", "card", "cod"])

    # only for single order
    product = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False)
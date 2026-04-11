from rest_framework import serializers


class OrderCardSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()

    product_name = serializers.CharField()
    image = serializers.CharField(allow_null=True)
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
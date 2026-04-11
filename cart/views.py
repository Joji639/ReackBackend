from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Cart
from .serializers import CartSerializer,CartCreateSerializer,CartUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CartListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CartCreateSerializer)
    def post(self, request):
        product_id = request.data.get("product")

        if not product_id:
            return Response({"error": "Product ID is required"}, status=400)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product_id=product_id
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response(CartSerializer(cart_item).data, status=201)

class CartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CartUpdateSerializer)
    def patch(self, request, product_id):
        action = request.data.get("action")

        if action not in ["increase", "decrease"]:
            return Response({"error": "Invalid action"}, status=400)

        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)

            if action == "increase":
                cart_item.quantity += 1
            else:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                else:
                    return Response({"error": "Minimum quantity is 1"}, status=400)

            cart_item.save()
            return Response(CartSerializer(cart_item).data)

        except Cart.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

    def delete(self, request, product_id):
        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)
            cart_item.delete()
            return Response(status=204)

        except Cart.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)
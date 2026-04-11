from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Order, OrderItem
from .serializers import PaymentSerializer,PaymentRequestSerializer
from cart.models import Cart
from allproducts.models import Products
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        try:
            orders = Order.objects.filter(user=request.user).order_by("-id")
            serializer = PaymentSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception:
            return Response(
                {"error": "Failed to fetch orders"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(request_body=PaymentRequestSerializer)
    def post(self, request):
        try:
            data = request.data
            order_type = data.get("type")

        
            serializer = PaymentSerializer(data={
                "full_name": data.get("full_name"),
                "email": data.get("email"),
                "phone": data.get("phone"),
                "address": data.get("address"),
                "payment_method": data.get("payment_method"),
                "total_price": 0
            })

            serializer.is_valid(raise_exception=True)

            
            if order_type == "cart":
                cart_items = Cart.objects.filter(user=request.user)

                if not cart_items.exists():
                    return Response({"error": "Cart is empty"}, status=400)

                total_price = 0

                order = serializer.save(user=request.user)

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                    total_price += item.quantity * item.product.price

                order.total_price = total_price
                order.save()

            
                cart_items.delete()

                return Response(
                    {"message": "Order placed successfully"},
                    status=status.HTTP_201_CREATED
                )

            
            elif order_type == "single":
                product_id = data.get("product")
                quantity = data.get("quantity", 1)

                if not product_id:
                    return Response({"error": "Product required"}, status=400)

                product = Products.objects.get(id=product_id)

                order = serializer.save(user=request.user)

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )

                order.total_price = product.price * quantity
                order.save()

                return Response(
                    {"message": "Order placed successfully"},
                    status=status.HTTP_201_CREATED
                )

            else:
                return Response({"error": "Invalid order type"}, status=400)

        except Products.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )